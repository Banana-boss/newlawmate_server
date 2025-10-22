# User 엔티티 문서

## 기본 정보
- **엔티티명**: User
- **테이블명**: `users`
- **작성일**: 2025-10-08
- **버전**: 1.0

## 개요
사용자의 기본 정보를 저장하는 엔티티입니다. 이메일, 이름, 나이, 활성화 상태 등의 정보를 관리합니다.

## 필드 정의

| 필드명 | 타입 | Null 허용 | 기본값 | 설명 | 제약조건 |
|--------|------|-----------|--------|------|----------|
| id | Integer | No | AUTO | 기본키 | Primary Key, Auto Increment |
| email | String(255) | No | - | 사용자 이메일 | Unique, Index |
| name | String(100) | No | - | 사용자 이름 | - |
| age | Integer | Yes | NULL | 나이 | - |
| is_active | Boolean | No | True | 활성화 상태 | - |
| created_at | DateTime | No | now() | 생성 시각 | - |
| updated_at | DateTime | No | now() | 수정 시각 | On Update |

## 인덱스

| 인덱스명 | 컬럼 | 타입 | 설명 |
|----------|------|------|------|
| pk_users_id | id | Primary Key | 기본키 |
| uk_users_email | email | Unique | 이메일 중복 방지 |
| idx_users_email | email | Index | 이메일 검색 성능 향상 |

## 관계 (Relationships)

현재 User 엔티티는 독립적으로 존재하며 다른 엔티티와의 관계는 없습니다.

향후 확장 가능한 관계:
- **One-to-Many**: User → Posts (사용자가 작성한 게시글)
- **One-to-Many**: User → Comments (사용자가 작성한 댓글)
- **Many-to-Many**: User ↔ Roles (사용자 권한)

## ORM 모델 정의

### SQLAlchemy 모델
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
```

## Pydantic 스키마

### Base Schema
```python
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=255, description="사용자 이메일")
    name: str = Field(..., min_length=1, max_length=100, description="사용자 이름")
    age: int | None = Field(None, ge=0, le=150, description="나이")
    is_active: bool = Field(True, description="활성화 상태")
```

### Create Schema
```python
class UserCreate(UserBase):
    """사용자 생성 스키마"""
    pass
```

### Update Schema
```python
class UserUpdate(BaseModel):
    """사용자 수정 스키마 (부분 수정 지원)"""
    email: EmailStr | None = Field(None, max_length=255)
    name: str | None = Field(None, min_length=1, max_length=100)
    age: int | None = Field(None, ge=0, le=150)
    is_active: bool | None = None
```

### Response Schema
```python
class UserResponse(UserBase):
    """사용자 응답 스키마"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ORM 모델 → Pydantic 변환 허용
```

## 비즈니스 규칙

### 생성 규칙
1. 이메일은 유효한 형식이어야 함
2. 이메일은 중복될 수 없음 (대소문자 구분 없음)
3. 이름은 1자 이상 100자 이하
4. 나이는 0 이상 150 이하 (선택 필드)
5. is_active는 기본값 True로 설정

### 수정 규칙
1. 이메일 변경 시 중복 검증 수행
2. 제공된 필드만 수정 (부분 수정 지원)
3. updated_at은 자동으로 현재 시각으로 갱신

### 삭제 규칙
1. 물리적 삭제 수행 (Soft Delete 아님)
2. 삭제 전 관련 데이터 확인 필요 (향후 관계가 추가될 경우)

## 검증 규칙

### 필드 검증
- **email**:
  - 유효한 이메일 형식 (RFC 5322)
  - 최대 255자
  - 중복 불가
  - 소문자 정규화 권장

- **name**:
  - 1자 이상 100자 이하
  - 빈 문자열 불가

- **age**:
  - 0 이상 150 이하
  - NULL 허용 (선택 필드)

- **is_active**:
  - Boolean 타입
  - 기본값 True

### 중복 검증
- 이메일 중복 검증은 대소문자 구분 없이 수행
- 예: `user@example.com`과 `USER@EXAMPLE.COM`은 중복으로 간주

## 데이터 예시

### 샘플 데이터 1
```json
{
  "id": 1,
  "email": "hong@example.com",
  "name": "홍길동",
  "age": 25,
  "is_active": true,
  "created_at": "2025-10-08T12:00:00+00:00",
  "updated_at": "2025-10-08T12:00:00+00:00"
}
```

### 샘플 데이터 2 (나이 미입력)
```json
{
  "id": 2,
  "email": "kim@example.com",
  "name": "김철수",
  "age": null,
  "is_active": true,
  "created_at": "2025-10-08T13:00:00+00:00",
  "updated_at": "2025-10-08T13:00:00+00:00"
}
```

### 샘플 데이터 3 (비활성 사용자)
```json
{
  "id": 3,
  "email": "park@example.com",
  "name": "박영희",
  "age": 30,
  "is_active": false,
  "created_at": "2025-10-08T14:00:00+00:00",
  "updated_at": "2025-10-08T15:00:00+00:00"
}
```

## 마이그레이션

### 테이블 생성 SQL (참고용)
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    age INT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Alembic 마이그레이션
```bash
# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Create users table"

# 마이그레이션 적용
alembic upgrade head
```

## 성능 최적화

### 인덱스 전략
- `id`: Primary Key (자동 인덱싱)
- `email`: Unique Index (중복 검증 및 검색 성능)

### 쿼리 최적화
- 이메일 조회: O(log n) - Unique Index 활용
- ID 조회: O(1) - Primary Key 활용
- 목록 조회: LIMIT/OFFSET 사용으로 메모리 효율성 확보

## 관련 문서
- [사용자 관리 요청 문서](user_request.md)
- [사용자 관리 설계 문서](user_design.md)
- [사용자 관리 API 문서](user_endpoint.md)
