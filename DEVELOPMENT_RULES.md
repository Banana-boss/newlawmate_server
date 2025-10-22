# 개발 필수 규칙

이 문서는 FastAPI 서버 템플릿에서 **새로운 기능을 추가하거나 수정할 때 반드시 따라야 하는 규칙**을 정의합니다.

## 📋 목차
1. [개발 워크플로우](#개발-워크플로우)
2. [문서 작성 규칙](#문서-작성-규칙)
3. [코드 작성 규칙](#코드-작성-규칙)
4. [테스트 작성 규칙](#테스트-작성-규칙)
5. [배포 규칙](#배포-규칙)

---

## 개발 워크플로우

### 필수 단계

모든 기능 개발은 **반드시 다음 순서**로 진행해야 합니다:

```
1. 요청 문서 작성
   ↓
2. 설계 문서 작성
   ↓
3. 엔드포인트 문서 작성
   ↓
4. 엔티티 문서 작성
   ↓
5. 코드 구현 (Entity → Repository → Service → Router)
   ↓
6. 테스트 코드 작성
   ↓
7. 모든 테스트 통과 확인
   ↓
8. 배포
```

### 🚫 절대 금지 사항
- 문서 없이 코드를 먼저 작성하는 것
- 테스트 코드 없이 배포하는 것
- 테스트가 실패한 상태로 배포하는 것

---

## 문서 작성 규칙

### 1. 요청 문서 (`docs/[기능명]_request.md`)

**템플릿**: `docs/00_template/request_template.md`

새로운 기능 개발 시 **가장 먼저 작성**해야 하는 문서입니다.

**필수 포함 내용**:
- 기능명, 요청일, 담당자, 우선순위
- 요청 배경 및 문제 정의
- 기능 설명 및 주요 요구사항
- 예상 엔드포인트 목록
- 데이터 모델 초안
- 비즈니스 로직
- 제약사항 및 성공 기준

**예시**: `docs/example/user_request.md`

### 2. 설계 문서 (`docs/[기능명]_design.md`)

**템플릿**: `docs/00_template/design_template.md`

요청 문서가 승인되면 작성하는 상세 설계 문서입니다.

**필수 포함 내용**:
- 3-tier 아키텍처 계층별 책임 정의
- Router, Service, Repository 주요 메서드 정의
- 데이터 흐름 다이어그램
- 스키마 설계 (Create, Update, Response)
- 에러 처리 전략
- 검증 규칙
- 성능 및 보안 고려사항
- 테스트 시나리오

**예시**: `docs/example/user_design.md`

### 3. 엔드포인트 문서 (`docs/[기능명]_endpoint.md`)

**템플릿**: `docs/00_template/endpoint_template.md`

API 엔드포인트의 상세 스펙을 정의하는 문서입니다.

**필수 포함 내용**:
- 모든 엔드포인트의 HTTP 메서드, 경로, 설명
- Request/Response 예시 (JSON)
- 필드별 타입, 필수 여부, 제약조건
- 성공/실패 응답 코드 및 예시
- curl 예제
- 테스트 체크리스트

**예시**: `docs/example/user_endpoint.md`

### 4. 엔티티 문서 (`docs/[기능명]_entity.md`)

**템플릿**: `docs/00_template/entity_template.md`

데이터베이스 엔티티의 상세 스펙을 정의하는 문서입니다.

**필수 포함 내용**:
- 엔티티명, 테이블명
- 모든 필드의 타입, Null 허용 여부, 기본값, 제약조건
- 인덱스 정의
- 관계(Relationships) 정의
- ORM 모델 코드
- Pydantic 스키마 코드
- 비즈니스 규칙 및 검증 규칙
- 샘플 데이터

**예시**: `docs/example/user_entity.md`

---

## 코드 작성 규칙

### 1. 디렉토리 구조

모든 기능은 **3-tier 아키텍처**를 따라 다음 구조로 작성합니다:

```
app/features/[기능명]/
├── entity/          # ORM 모델
│   ├── __init__.py
│   └── [entity명].py
├── repository/      # 데이터 접근 계층
│   ├── __init__.py
│   └── [entity명]_repository.py
├── service/         # 비즈니스 로직 계층
│   ├── __init__.py
│   └── [entity명]_service.py
├── router/          # API 엔드포인트 계층
│   ├── __init__.py
│   └── [entity명]_router.py
└── schema/          # Pydantic 스키마
    ├── __init__.py
    └── [entity명]_schema.py
```

### 2. 구현 순서

**반드시 다음 순서로 구현**해야 합니다:

1. **Entity (ORM 모델)**: 데이터베이스 테이블 정의
2. **Schema (Pydantic)**: 요청/응답 데이터 검증
3. **Repository**: 데이터베이스 CRUD 작업
4. **Service**: 비즈니스 로직 및 검증
5. **Router**: API 엔드포인트

### 3. 계층별 책임

#### Entity Layer
```python
# app/features/[기능명]/entity/[entity명].py

- SQLAlchemy Base 상속
- 테이블명, 컬럼, 인덱스 정의
- 관계(Relationships) 정의
- 순수 데이터 모델 (로직 없음)
```

#### Schema Layer
```python
# app/features/[기능명]/schema/[entity명]_schema.py

- Pydantic BaseModel 상속
- Create, Update, Response 스키마 정의
- Field 검증 규칙 (min_length, max_length, ge, le 등)
- 타입 힌팅 필수
```

#### Repository Layer
```python
# app/features/[기능명]/repository/[entity명]_repository.py

- 순수 데이터 접근 로직만 담당
- 비즈니스 로직 금지
- CRUD 메서드 구현 (create, get_by_id, get_all, update, delete)
- @staticmethod 사용 권장
```

#### Service Layer
```python
# app/features/[기능명]/service/[entity명]_service.py

- 비즈니스 로직 구현
- 데이터 검증 (중복 검증, 존재 여부 확인 등)
- HTTPException 발생
- Repository 호출
- 트랜잭션 관리
```

#### Router Layer
```python
# app/features/[기능명]/router/[entity명]_router.py

- HTTP 요청/응답 처리
- APIRouter 사용
- Pydantic 스키마로 자동 검증
- Service 호출
- 상태 코드 반환
- API 문서화 (summary, description)
```

### 4. 코딩 컨벤션

```python
# 파일 상단에 docstring 필수
"""
모듈 설명

상세 설명
"""

# 타입 힌팅 필수
def create_user(db: Session, user_data: UserCreate) -> UserResponse:
    pass

# HTTPException 사용
from fastapi import HTTPException, status

raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

# 이메일 등 대소문자 구분이 필요한 경우 정규화
email = email.lower()
```

---

## 테스트 작성 규칙

### 1. 테스트 디렉토리 구조

```
tests/
├── conftest.py                    # pytest 설정 및 fixture
├── features/
│   └── [기능명]/
│       ├── __init__.py
│       └── test_[entity명]_router.py
```

### 2. 테스트 작성 필수 사항

**모든 엔드포인트는 다음 테스트를 포함해야 합니다**:

#### 정상 시나리오
- 생성 성공
- 조회 성공 (목록, 단건)
- 수정 성공
- 삭제 성공

#### 예외 시나리오
- 중복 데이터 생성 시도 → 409
- 존재하지 않는 데이터 조회 → 404
- 잘못된 입력 데이터 → 400/422
- 필수 필드 누락 → 422

#### 경계값 테스트
- 최소값, 최대값
- 빈 문자열, NULL
- 페이지네이션 경계값

### 3. 테스트 코드 예시

```python
class TestUserCreate:
    """사용자 생성 API 테스트"""

    def test_create_user_success(self, client):
        """정상적인 사용자 생성"""
        response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "홍길동"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == "test@example.com"

    def test_create_user_duplicate_email(self, client):
        """중복 이메일로 생성 시도"""
        client.post("/api/v1/users", json={"email": "dup@example.com", "name": "사용자1"})
        response = client.post("/api/v1/users", json={"email": "dup@example.com", "name": "사용자2"})
        assert response.status_code == status.HTTP_409_CONFLICT
```

### 4. 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 특정 테스트만 실행
pytest tests/features/user/

# 커버리지 포함
pytest --cov=app tests/
```

**배포 전 모든 테스트가 통과해야 합니다!**

---

## 배포 규칙

### 1. 배포 전 체크리스트

- [ ] 모든 문서 작성 완료 (요청, 설계, 엔드포인트, 엔티티)
- [ ] 코드 구현 완료 (Entity, Repository, Service, Router, Schema)
- [ ] 테스트 코드 작성 완료
- [ ] **모든 테스트 통과** (`pytest`)
- [ ] API 문서 확인 (Swagger: http://localhost:8000/docs)
- [ ] `.env` 파일 설정 확인

### 2. 배포 명령어

```bash
# 배포 스크립트 실행
./deploy.sh
```

**배포 스크립트는 다음 순서로 동작합니다**:

1. 환경 변수 로드
2. 의존성 확인
3. **테스트 실행** ← 실패 시 배포 중단!
4. Docker 이미지 빌드
5. 컨테이너 재시작
6. 헬스 체크
7. 배포 완료

### 3. 배포 롤백

테스트 실패 시 자동으로 배포가 중단됩니다.

수동 롤백이 필요한 경우:
```bash
# 컨테이너 중단
docker-compose down

# 이전 버전으로 복구
git checkout [이전 커밋]

# 재배포
./deploy.sh
```

---

## 📝 요약

### 문서 → 코드 → 테스트 → 배포

1. **문서 먼저**: 요청 → 설계 → 엔드포인트 → 엔티티
2. **코드 구현**: Entity → Repository → Service → Router
3. **테스트 작성**: 모든 엔드포인트 + 예외 + 경계값
4. **배포 실행**: `./deploy.sh` (테스트 통과 필수)

### 핵심 원칙

✅ **문서 기반 개발**: 코드보다 문서가 먼저
✅ **3-tier 아키텍처**: 계층별 책임 명확히
✅ **테스트 필수**: 모든 엔드포인트 테스트 작성
✅ **안전한 배포**: 테스트 통과 후에만 배포

---

더 자세한 내용은 다음 문서를 참고하세요:
- [개발 워크플로우 가이드](docs/workflow_guide.md)
- [아키텍처 설명](docs/architecture.md)
- [README](README.md)
