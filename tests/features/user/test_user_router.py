"""
User Router 테스트

사용자 관리 API 엔드포인트에 대한 통합 테스트입니다.
"""

import pytest
from fastapi import status


class TestUserCreate:
    """사용자 생성 API 테스트"""

    def test_create_user_success(self, client):
        """정상적인 사용자 생성"""
        response = client.post(
            "/api/v1/users",
            json={
                "email": "test@example.com",
                "name": "홍길동",
                "age": 25,
                "is_active": True,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "홍길동"
        assert data["age"] == 25
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_user_without_age(self, client):
        """나이 없이 사용자 생성 (선택 필드)"""
        response = client.post(
            "/api/v1/users",
            json={"email": "test2@example.com", "name": "김철수"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["age"] is None

    def test_create_user_duplicate_email(self, client):
        """중복 이메일로 사용자 생성 시도"""
        # 첫 번째 사용자 생성
        client.post(
            "/api/v1/users",
            json={"email": "duplicate@example.com", "name": "사용자1"},
        )
        # 중복 이메일로 두 번째 사용자 생성 시도
        response = client.post(
            "/api/v1/users",
            json={"email": "duplicate@example.com", "name": "사용자2"},
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in response.json()["detail"].lower()

    def test_create_user_invalid_email(self, client):
        """잘못된 이메일 형식"""
        response = client.post(
            "/api/v1/users",
            json={"email": "invalid-email", "name": "홍길동"},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_empty_name(self, client):
        """빈 이름"""
        response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": ""},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_age_out_of_range(self, client):
        """나이 범위 초과"""
        response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "홍길동", "age": 200},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_negative_age(self, client):
        """음수 나이"""
        response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "홍길동", "age": -5},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUserList:
    """사용자 목록 조회 API 테스트"""

    def test_get_users_empty(self, client):
        """빈 목록 조회"""
        response = client.get("/api/v1/users")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_users(self, client):
        """사용자 목록 조회"""
        # 사용자 3명 생성
        for i in range(3):
            client.post(
                "/api/v1/users",
                json={"email": f"user{i}@example.com", "name": f"사용자{i}"},
            )

        response = client.get("/api/v1/users")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3

    def test_get_users_with_pagination(self, client):
        """페이지네이션 테스트"""
        # 사용자 5명 생성
        for i in range(5):
            client.post(
                "/api/v1/users",
                json={"email": f"user{i}@example.com", "name": f"사용자{i}"},
            )

        # skip=0, limit=2
        response = client.get("/api/v1/users?skip=0&limit=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

        # skip=2, limit=2
        response = client.get("/api/v1/users?skip=2&limit=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

        # skip=4, limit=2
        response = client.get("/api/v1/users?skip=4&limit=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1


class TestUserGet:
    """사용자 단건 조회 API 테스트"""

    def test_get_user_success(self, client):
        """정상적인 사용자 조회"""
        # 사용자 생성
        create_response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "홍길동"},
        )
        user_id = create_response.json()["id"]

        # 사용자 조회
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == "test@example.com"
        assert data["name"] == "홍길동"

    def test_get_user_not_found(self, client):
        """존재하지 않는 사용자 조회"""
        response = client.get("/api/v1/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUserUpdate:
    """사용자 수정 API 테스트"""

    def test_update_user_success(self, client):
        """정상적인 사용자 수정"""
        # 사용자 생성
        create_response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "홍길동", "age": 25},
        )
        user_id = create_response.json()["id"]

        # 사용자 수정
        response = client.put(
            f"/api/v1/users/{user_id}",
            json={"name": "홍길동_수정", "age": 26},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "홍길동_수정"
        assert data["age"] == 26
        assert data["email"] == "test@example.com"  # 변경되지 않음

    def test_update_user_partial(self, client):
        """부분 수정"""
        # 사용자 생성
        create_response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "홍길동", "age": 25},
        )
        user_id = create_response.json()["id"]

        # 이름만 수정
        response = client.put(
            f"/api/v1/users/{user_id}",
            json={"name": "김철수"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "김철수"
        assert data["age"] == 25  # 변경되지 않음

    def test_update_user_email_duplicate(self, client):
        """이메일 중복으로 수정 시도"""
        # 사용자 2명 생성
        client.post(
            "/api/v1/users",
            json={"email": "user1@example.com", "name": "사용자1"},
        )
        create_response = client.post(
            "/api/v1/users",
            json={"email": "user2@example.com", "name": "사용자2"},
        )
        user2_id = create_response.json()["id"]

        # user2의 이메일을 user1의 이메일로 변경 시도
        response = client.put(
            f"/api/v1/users/{user2_id}",
            json={"email": "user1@example.com"},
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_update_user_not_found(self, client):
        """존재하지 않는 사용자 수정"""
        response = client.put(
            "/api/v1/users/999",
            json={"name": "홍길동"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUserDelete:
    """사용자 삭제 API 테스트"""

    def test_delete_user_success(self, client):
        """정상적인 사용자 삭제"""
        # 사용자 생성
        create_response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "홍길동"},
        )
        user_id = create_response.json()["id"]

        # 사용자 삭제
        response = client.delete(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # 삭제 확인
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_not_found(self, client):
        """존재하지 않는 사용자 삭제"""
        response = client.delete("/api/v1/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUserEdgeCases:
    """경계값 및 특수 케이스 테스트"""

    def test_create_user_age_boundary(self, client):
        """나이 경계값 테스트"""
        # 나이 0
        response = client.post(
            "/api/v1/users",
            json={"email": "user0@example.com", "name": "사용자", "age": 0},
        )
        assert response.status_code == status.HTTP_201_CREATED

        # 나이 150
        response = client.post(
            "/api/v1/users",
            json={"email": "user150@example.com", "name": "사용자", "age": 150},
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_user_name_length(self, client):
        """이름 길이 테스트"""
        # 이름 1자
        response = client.post(
            "/api/v1/users",
            json={"email": "user1@example.com", "name": "A"},
        )
        assert response.status_code == status.HTTP_201_CREATED

        # 이름 100자
        long_name = "A" * 100
        response = client.post(
            "/api/v1/users",
            json={"email": "user2@example.com", "name": long_name},
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_email_case_insensitive(self, client):
        """이메일 대소문자 구분 없이 중복 검증"""
        # 소문자 이메일로 생성
        client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "사용자1"},
        )

        # 대문자 이메일로 생성 시도
        response = client.post(
            "/api/v1/users",
            json={"email": "TEST@EXAMPLE.COM", "name": "사용자2"},
        )
        assert response.status_code == status.HTTP_409_CONFLICT
