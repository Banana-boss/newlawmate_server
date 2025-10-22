# 아키텍처 설명

FastAPI 서버 템플릿의 3-tier 아키텍처 구조 및 설계 원칙을 설명합니다.

## 목차
1. [전체 아키텍처](#전체-아키텍처)
2. [3-Tier 아키텍처](#3-tier-아키텍처)
3. [디렉토리 구조](#디렉토리-구조)
4. [계층 간 데이터 흐름](#계층-간-데이터-흐름)
5. [의존성 관리](#의존성-관리)
6. [데이터베이스 설계](#데이터베이스-설계)

---

## 전체 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                      Client Layer                        │
│              (Browser, Mobile App, etc.)                 │
└─────────────────────────────────────────────────────────┘
                           │
                           │ HTTP/HTTPS
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   Presentation Layer                     │
│                    (FastAPI Router)                      │
│  - HTTP 요청/응답 처리                                     │
│  - 요청 데이터 검증 (Pydantic)                             │
│  - API 문서 자동 생성                                      │
└─────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   Business Logic Layer                  │
│                     (Service Layer)                      │
│  - 비즈니스 로직 구현                                       │
│  - 데이터 검증 및 가공                                      │
│  - 예외 처리                                              │
│  - 트랜잭션 관리                                           │
└─────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   Data Access Layer                     │
│                   (Repository Layer)                     │
│  - 데이터베이스 CRUD 작업                                  │
│  - 쿼리 실행                                              │
│  - ORM 작업 (SQLAlchemy)                                 │
└─────────────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────┐
│                     Database Layer                       │
│                        (MySQL)                           │
│  - 데이터 저장                                            │
│  - 트랜잭션 관리                                           │
│  - 인덱싱 및 최적화                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 3-Tier 아키텍처

### Tier 1: Presentation Layer (Router)

**역할**: HTTP 요청/응답 처리

```python
# app/features/user/router/user_router.py

@router.post("/api/v1/users", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)
```

**책임**:
- API 엔드포인트 정의
- HTTP 메서드 및 경로 매핑
- 요청 데이터 Pydantic 검증
- 응답 데이터 직렬화
- HTTP 상태 코드 반환

**규칙**:
- ❌ 비즈니스 로직 포함 금지
- ❌ 데이터베이스 직접 접근 금지
- ✅ Service 계층만 호출
- ✅ 얇은(Thin) 계층 유지

### Tier 2: Business Logic Layer (Service)

**역할**: 비즈니스 로직 및 데이터 검증

```python
# app/features/user/service/user_service.py

def create_user(self, db: Session, user_data: UserCreate) -> UserResponse:
    # 비즈니스 규칙: 이메일 중복 검증
    if self.repository.get_by_email(db, user_data.email):
        raise HTTPException(status_code=409, detail="Email already exists")

    # Repository 호출
    db_user = self.repository.create(db, user_data)
    return UserResponse.model_validate(db_user)
```

**책임**:
- 비즈니스 로직 구현
- 데이터 검증 (중복, 존재 여부 등)
- 데이터 가공 및 변환
- 예외 처리 (HTTPException)
- Repository 계층 호출
- 트랜잭션 조율

**규칙**:
- ❌ HTTP 요청/응답 처리 금지
- ❌ SQL 쿼리 직접 작성 금지
- ✅ 비즈니스 로직 집중
- ✅ Repository 계층만 호출

### Tier 3: Data Access Layer (Repository)

**역할**: 데이터베이스 CRUD 작업

```python
# app/features/user/repository/user_repository.py

@staticmethod
def create(db: Session, user_data: UserCreate) -> User:
    db_user = User(
        email=user_data.email.lower(),
        name=user_data.name,
        age=user_data.age,
        is_active=user_data.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

**책임**:
- 데이터베이스 CRUD 작업
- SQLAlchemy 쿼리 실행
- ORM 엔티티 변환
- 순수 데이터 접근 로직

**규칙**:
- ❌ 비즈니스 로직 포함 금지
- ❌ HTTPException 발생 금지
- ✅ 순수 데이터 작업만
- ✅ @staticmethod 사용 권장

---

## 디렉토리 구조

```
server_templete/
├── app/
│   ├── core/                           # 핵심 인프라
│   │   ├── __init__.py
│   │   ├── config.py                  # 설정 관리 (환경 변수)
│   │   ├── database.py                # DB 연결 및 세션
│   │   ├── dependencies.py            # 의존성 주입
│   │   └── init_db.py                 # DB 초기화
│   │
│   ├── features/                       # 기능 단위 모듈
│   │   └── user/                      # User 기능 예시
│   │       ├── entity/                # ORM 모델
│   │       │   ├── __init__.py
│   │       │   └── user.py           # User 엔티티
│   │       │
│   │       ├── schema/                # Pydantic 스키마
│   │       │   ├── __init__.py
│   │       │   └── user_schema.py    # Create, Update, Response
│   │       │
│   │       ├── repository/            # 데이터 접근 계층
│   │       │   ├── __init__.py
│   │       │   └── user_repository.py
│   │       │
│   │       ├── service/               # 비즈니스 로직 계층
│   │       │   ├── __init__.py
│   │       │   └── user_service.py
│   │       │
│   │       └── router/                # API 엔드포인트 계층
│   │           ├── __init__.py
│   │           └── user_router.py
│   │
│   ├── __init__.py
│   └── main.py                        # FastAPI 앱 진입점
│
├── tests/                              # 테스트 코드
│   ├── conftest.py                    # pytest 설정
│   └── features/
│       └── user/
│           └── test_user_router.py
│
├── docs/                               # 문서
│   ├── 00_template/                   # 문서 템플릿
│   │   ├── request_template.md
│   │   ├── design_template.md
│   │   ├── endpoint_template.md
│   │   └── entity_template.md
│   │
│   ├── example/                       # 예시 문서
│   │   ├── user_request.md
│   │   ├── user_design.md
│   │   ├── user_endpoint.md
│   │   └── user_entity.md
│   │
│   ├── workflow_guide.md              # 개발 워크플로우 가이드
│   └── architecture.md                # 이 문서
│
├── docker-compose.yml                  # Docker Compose 설정
├── Dockerfile                          # Docker 이미지 빌드
├── deploy.sh                           # 배포 스크립트
├── requirements.txt                    # Python 의존성
├── pytest.ini                          # pytest 설정
├── .env.example                        # 환경 변수 예시
├── .gitignore
├── README.md
├── DEVELOPMENT_RULES.md                # 개발 필수 규칙
└── CLAUDE.MD                           # Claude AI 지시사항
```

---

## 계층 간 데이터 흐름

### 사용자 생성 플로우 예시

```
1. Client Request
   POST /api/v1/users
   {
     "email": "user@example.com",
     "name": "홍길동",
     "age": 25
   }

   ↓

2. Router Layer (user_router.py)
   - Pydantic UserCreate 스키마로 자동 검증
   - user_service.create_user() 호출

   ↓

3. Service Layer (user_service.py)
   - 비즈니스 로직: 이메일 중복 검증
   - repository.get_by_email() 호출로 중복 확인
   - 중복이면 HTTPException(409) 발생
   - repository.create() 호출

   ↓

4. Repository Layer (user_repository.py)
   - User ORM 엔티티 생성
   - db.add(), db.commit(), db.refresh()
   - User 엔티티 반환

   ↓

5. Database (MySQL)
   - INSERT INTO users ...
   - 트랜잭션 커밋

   ↓

6. Repository → Service
   - User 엔티티 반환

   ↓

7. Service → Router
   - UserResponse 스키마로 변환
   - Pydantic 직렬화

   ↓

8. Client Response (201 Created)
   {
     "id": 1,
     "email": "user@example.com",
     "name": "홍길동",
     "age": 25,
     "is_active": true,
     "created_at": "2025-10-08T12:00:00",
     "updated_at": "2025-10-08T12:00:00"
   }
```

---

## 의존성 관리

### FastAPI Depends 사용

```python
# app/core/dependencies.py
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# Router에서 사용
@router.post("/api/v1/users")
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)  # 의존성 주입
):
    return user_service.create_user(db, user_data)
```

### 의존성 주입 장점

1. **테스트 용이성**: Mock 객체로 쉽게 교체 가능
2. **코드 재사용**: 공통 로직을 한 곳에 정의
3. **관심사 분리**: 비즈니스 로직과 인프라 분리

---

## 데이터베이스 설계

### ORM 사용 (SQLAlchemy)

```python
# app/features/user/entity/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(100), nullable=False)
    # ...
```

### 마이그레이션

서버 시작 시 자동으로 테이블을 생성합니다:

```python
# app/core/init_db.py
def init_database():
    Base.metadata.create_all(bind=engine)
```

**운영 환경에서는 Alembic 사용 권장**:
```bash
alembic revision --autogenerate -m "Create users table"
alembic upgrade head
```

### 인덱스 전략

- **Primary Key**: 자동 인덱싱 (O(1) 조회)
- **Unique Index**: 중복 검증 및 빠른 검색 (email)
- **Index**: 자주 조회되는 필드

---

## 설계 원칙

### 1. 관심사 분리 (Separation of Concerns)

각 계층은 명확한 책임을 가지며, 다른 계층의 세부사항을 알 필요가 없습니다.

### 2. 의존성 역전 원칙 (Dependency Inversion)

상위 계층(Service)이 하위 계층(Repository)에 의존하지만, 인터페이스를 통해 느슨한 결합을 유지합니다.

### 3. 단일 책임 원칙 (Single Responsibility)

각 클래스/모듈은 하나의 책임만 가집니다.

### 4. 개방-폐쇄 원칙 (Open-Closed)

새로운 기능 추가 시 기존 코드를 수정하지 않고 확장할 수 있습니다.

---

## 확장성

### 새 기능 추가

1. `app/features/[새기능]/` 디렉토리 생성
2. Entity, Schema, Repository, Service, Router 순서로 구현
3. `app/main.py`에 라우터 등록
4. 테스트 코드 작성

### 공통 기능 추가

- **미들웨어**: `app/middleware/`
- **유틸리티**: `app/utils/`
- **예외 처리**: `app/exceptions/`
- **인증/인가**: `app/auth/`

---

## 참고 문서

- [개발 필수 규칙](../DEVELOPMENT_RULES.md)
- [개발 워크플로우 가이드](workflow_guide.md)
- [README](../README.md)
