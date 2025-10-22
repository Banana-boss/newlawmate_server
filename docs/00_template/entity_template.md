# [엔티티명] 엔티티 문서

## 기본 정보
- **엔티티명**: [엔티티 이름]
- **테이블명**: `[table_name]`
- **작성일**: [YYYY-MM-DD]
- **버전**: 1.0

## 개요
[엔티티에 대한 설명]

## 필드 정의

| 필드명 | 타입 | Null 허용 | 기본값 | 설명 | 제약조건 |
|--------|------|-----------|--------|------|----------|
| id | Integer | No | AUTO | 기본키 | Primary Key, Auto Increment |
| field1 | String(100) | No | - | [설명] | Unique, Index |
| field2 | Integer | No | - | [설명] | - |
| field3 | String(255) | Yes | NULL | [설명] | - |
| field4 | Boolean | No | False | [설명] | - |
| created_at | DateTime | No | now() | 생성 시각 | - |
| updated_at | DateTime | No | now() | 수정 시각 | On Update |

## 인덱스

| 인덱스명 | 컬럼 | 타입 | 설명 |
|----------|------|------|------|
| pk_[table]_id | id | Primary Key | 기본키 |
| uk_[table]_field1 | field1 | Unique | [설명] |
| idx_[table]_field2 | field2 | Index | [설명] |

## 관계 (Relationships)

### One-to-Many
```
[부모 엔티티] 1 --- N [자식 엔티티]
```
- **설명**: [관계 설명]
- **외래키**: `[foreign_key_field]`

### Many-to-One
```
[엔티티] N --- 1 [부모 엔티티]
```
- **설명**: [관계 설명]
- **외래키**: `[foreign_key_field]`

### Many-to-Many
```
[엔티티A] N --- N [엔티티B]
```
- **중간 테이블**: `[junction_table_name]`
- **설명**: [관계 설명]

## ORM 모델 정의

### SQLAlchemy 모델
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class [Entity](Base):
    __tablename__ = "[table_name]"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    field1 = Column(String(100), unique=True, index=True, nullable=False)
    field2 = Column(Integer, nullable=False)
    field3 = Column(String(255), nullable=True)
    field4 = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
```

## Pydantic 스키마

### Base Schema
```python
from pydantic import BaseModel, Field
from datetime import datetime

class [Entity]Base(BaseModel):
    field1: str = Field(..., max_length=100)
    field2: int
    field3: str | None = Field(None, max_length=255)
    field4: bool = False
```

### Create Schema
```python
class [Entity]Create([Entity]Base):
    pass
```

### Update Schema
```python
class [Entity]Update(BaseModel):
    field1: str | None = Field(None, max_length=100)
    field2: int | None = None
    field3: str | None = Field(None, max_length=255)
    field4: bool | None = None
```

### Response Schema
```python
class [Entity]Response([Entity]Base):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

## 비즈니스 규칙

### 생성 규칙
1. [규칙 1]
2. [규칙 2]

### 수정 규칙
1. [규칙 1]
2. [규칙 2]

### 삭제 규칙
1. [규칙 1]
2. [규칙 2]

## 검증 규칙

### 필드 검증
- **field1**: [검증 규칙]
- **field2**: [검증 규칙]
- **field3**: [검증 규칙]

### 중복 검증
- [중복 검증 규칙]

## 데이터 예시

### 샘플 데이터
```json
{
  "id": 1,
  "field1": "sample_value",
  "field2": 100,
  "field3": "optional_value",
  "field4": true,
  "created_at": "2025-10-08T12:00:00+00:00",
  "updated_at": "2025-10-08T12:00:00+00:00"
}
```

## 마이그레이션

### 생성 마이그레이션
```bash
alembic revision --autogenerate -m "Create [entity] table"
alembic upgrade head
```

### 테이블 생성 SQL (참고용)
```sql
CREATE TABLE [table_name] (
    id INT AUTO_INCREMENT PRIMARY KEY,
    field1 VARCHAR(100) NOT NULL UNIQUE,
    field2 INT NOT NULL,
    field3 VARCHAR(255),
    field4 BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_[table]_field1 (field1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## 관련 문서
- [설계 문서](design_[기능명].md)
- [API 문서](endpoint_[기능명].md)
