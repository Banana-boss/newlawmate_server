# 사용자 관리 설계 문서

## 기본 정보
- **기능명**: 사용자 관리 (User Management)
- **작성일**: 2025-10-08
- **관련 요청 문서**: [user_request.md](user_request.md)
- **버전**: 1.0

## 아키텍처 설계

### 계층별 책임

#### 1. Router Layer (API 엔드포인트)
**파일**: `app/features/user/router/user_router.py`

**책임**:
- HTTP 요청/응답 처리
- 요청 데이터 검증 (Pydantic 스키마 사용)
- UserService 호출
- HTTP 상태 코드 반환

**주요 엔드포인트**:
- `POST /api/v1/users` - 사용자 생성 (201 Created)
- `GET /api/v1/users` - 사용자 목록 조회 (200 OK)
- `GET /api/v1/users/{id}` - 사용자 단건 조회 (200 OK)
- `PUT /api/v1/users/{id}` - 사용자 정보 수정 (200 OK)
- `DELETE /api/v1/users/{id}` - 사용자 삭제 (204 No Content)

#### 2. Service Layer (비즈니스 로직)
**파일**: `app/features/user/service/user_service.py`

**책임**:
- 비즈니스 로직 구현
- 데이터 검증 (이메일 중복 검증 등)
- UserRepository 호출
- 예외 처리 및 에러 발생

**주요 메서드**:
- `create_user(db, user_data)` - 사용자 생성 (이메일 중복 검증)
- `get_user_by_id(db, user_id)` - ID로 사용자 조회
- `get_all_users(db, skip, limit)` - 사용자 목록 조회
- `update_user(db, user_id, user_data)` - 사용자 정보 수정
- `delete_user(db, user_id)` - 사용자 삭제

#### 3. Repository Layer (데이터 접근)
**파일**: `app/features/user/repository/user_repository.py`

**책임**:
- 데이터베이스 CRUD 작업
- SQLAlchemy 쿼리 실행
- 순수 데이터 접근 로직

**주요 메서드**:
- `create(db, user)` - DB에 사용자 저장
- `get_by_id(db, user_id)` - ID로 사용자 조회
- `get_by_email(db, email)` - 이메일로 사용자 조회
- `get_all(db, skip, limit)` - 사용자 목록 조회
- `update(db, user_id, user_data)` - 사용자 정보 수정
- `delete(db, user_id)` - 사용자 삭제

## 데이터 흐름

### 사용자 생성 플로우
```
Client Request (POST /api/v1/users)
    ↓
Router: UserCreate 스키마로 요청 검증
    ↓
Service: 이메일 중복 검증
    ↓
Repository: DB에 사용자 저장
    ↓
Database: INSERT
    ↓
Repository: User 엔티티 반환
    ↓
Service: 비즈니스 로직 처리 (필요시)
    ↓
Router: UserResponse 스키마로 변환
    ↓
Client Response (201 Created)
```

### 사용자 조회 플로우
```
Client Request (GET /api/v1/users/{id})
    ↓
Router: Path Parameter 검증
    ↓
Service: get_user_by_id 호출
    ↓
Repository: SELECT 쿼리 실행
    ↓
Database: 데이터 조회
    ↓
Repository: User 엔티티 반환 (또는 None)
    ↓
Service: 존재 여부 검증 (없으면 404 예외)
    ↓
Router: UserResponse 스키마로 변환
    ↓
Client Response (200 OK)
```

## 스키마 설계

### Base 스키마
```python
class UserBase(BaseModel):
    email: str = Field(..., max_length=255)
    name: str = Field(..., min_length=1, max_length=100)
    age: int | None = Field(None, ge=0, le=150)
    is_active: bool = True
```

### Create 스키마
```python
class UserCreate(UserBase):
    pass
```

### Update 스키마
```python
class UserUpdate(BaseModel):
    email: str | None = Field(None, max_length=255)
    name: str | None = Field(None, min_length=1, max_length=100)
    age: int | None = Field(None, ge=0, le=150)
    is_active: bool | None = None
```

### Response 스키마
```python
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

## 에러 처리

| 상황 | HTTP 상태 코드 | 메시지 |
|------|----------------|--------|
| 잘못된 요청 데이터 | 400 | Validation error: {detail} |
| 사용자를 찾을 수 없음 | 404 | User not found |
| 이메일 중복 | 409 | Email already exists |
| 서버 내부 오류 | 500 | Internal server error |

## 검증 규칙

### 입력 검증 (Pydantic)
- **email**: 이메일 형식, 최대 255자
- **name**: 1자 이상 100자 이하
- **age**: 0 이상 150 이하 (선택)
- **is_active**: Boolean (기본값 True)

### 비즈니스 규칙 (Service Layer)
1. 이메일 중복 검증: 생성/수정 시 중복 이메일 확인
2. 존재 여부 검증: 조회/수정/삭제 시 사용자 존재 확인
3. 이메일 정규화: 소문자 변환 후 저장

## 성능 고려사항
- 이메일 필드에 UNIQUE INDEX 생성으로 중복 검증 성능 향상
- 목록 조회 시 기본 limit=100으로 과도한 데이터 조회 방지
- ID 필드에 INDEX 적용 (Primary Key로 자동 생성)

## 보안 고려사항
- 이메일 정규화로 대소문자 우회 중복 가입 방지
- SQL Injection 방지: SQLAlchemy ORM 사용
- XSS 방지: 입력 데이터 검증 및 이스케이프 (FastAPI 자동 처리)

## 테스트 시나리오
1. **정상 시나리오**
   - 사용자 생성 성공
   - 사용자 목록 조회 성공
   - 사용자 단건 조회 성공
   - 사용자 수정 성공
   - 사용자 삭제 성공

2. **예외 시나리오**
   - 중복 이메일로 생성 시도 → 409
   - 존재하지 않는 사용자 조회 → 404
   - 잘못된 이메일 형식 → 400
   - 나이 범위 초과 → 400
   - 빈 이름 입력 → 400

3. **경계값 테스트**
   - 이름 1자, 100자
   - 나이 0, 150
   - limit 0, 1, 100, 1000

## 구현 체크리스트
- [x] User Entity 정의
- [x] UserRepository 구현
- [x] UserService 구현
- [x] UserRouter 구현
- [x] User 스키마 정의 (Create, Update, Response)
- [x] 단위 테스트 작성
- [x] 통합 테스트 작성
- [x] API 문서 확인 (Swagger)
