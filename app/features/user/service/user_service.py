"""
User Service

비즈니스 로직을 담당하는 Service 계층입니다.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.features.user.repository import UserRepository
from app.features.user.schema import UserCreate, UserUpdate, UserResponse
from app.features.user.entity import User


class UserService:
    """사용자 비즈니스 로직 계층"""

    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, db: Session, user_data: UserCreate) -> UserResponse:
        """
        사용자 생성

        Args:
            db: 데이터베이스 세션
            user_data: 사용자 생성 데이터

        Returns:
            생성된 사용자 응답

        Raises:
            HTTPException: 이메일 중복 시 409
        """
        # 이메일 중복 검증
        existing_user = self.repository.get_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
            )

        # 사용자 생성
        db_user = self.repository.create(db, user_data)
        return UserResponse.model_validate(db_user)

    def get_user_by_id(self, db: Session, user_id: int) -> UserResponse:
        """
        ID로 사용자 조회

        Args:
            db: 데이터베이스 세션
            user_id: 사용자 ID

        Returns:
            사용자 응답

        Raises:
            HTTPException: 사용자를 찾을 수 없으면 404
        """
        db_user = self.repository.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return UserResponse.model_validate(db_user)

    def get_all_users(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> list[UserResponse]:
        """
        사용자 목록 조회

        Args:
            db: 데이터베이스 세션
            skip: 건너뛸 항목 수
            limit: 조회할 최대 항목 수

        Returns:
            사용자 응답 리스트
        """
        db_users = self.repository.get_all(db, skip, limit)
        return [UserResponse.model_validate(user) for user in db_users]

    def update_user(
        self, db: Session, user_id: int, user_data: UserUpdate
    ) -> UserResponse:
        """
        사용자 정보 수정

        Args:
            db: 데이터베이스 세션
            user_id: 사용자 ID
            user_data: 수정할 데이터

        Returns:
            수정된 사용자 응답

        Raises:
            HTTPException: 사용자를 찾을 수 없으면 404, 이메일 중복 시 409
        """
        # 사용자 존재 여부 확인
        existing_user = self.repository.get_by_id(db, user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # 이메일 변경 시 중복 검증
        if user_data.email:
            email_user = self.repository.get_by_email(db, user_data.email)
            if email_user and email_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
                )

        # 사용자 수정
        updated_user = self.repository.update(db, user_id, user_data)
        return UserResponse.model_validate(updated_user)

    def delete_user(self, db: Session, user_id: int) -> None:
        """
        사용자 삭제

        Args:
            db: 데이터베이스 세션
            user_id: 사용자 ID

        Raises:
            HTTPException: 사용자를 찾을 수 없으면 404
        """
        success = self.repository.delete(db, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
