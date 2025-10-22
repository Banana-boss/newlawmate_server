# [기능명] 설계 문서

## 기본 정보
- **기능명**: [기능 이름]
- **작성일**: [YYYY-MM-DD]
- **관련 요청 문서**: [request_[기능명].md]
- **버전**: 1.0

## 아키텍처 설계

### 계층별 책임

#### 1. Router Layer (API 엔드포인트)
**파일**: `app/features/[기능명]/router/[기능명]_router.py`

**책임**:
- HTTP 요청/응답 처리
- 요청 데이터 검증 (Pydantic)
- Service Layer 호출
- HTTP 상태 코드 반환

**주요 엔드포인트**:
- `POST /api/v1/[resource]` - [설명]
- `GET /api/v1/[resource]` - [설명]
- `GET /api/v1/[resource]/{id}` - [설명]
- `PUT /api/v1/[resource]/{id}` - [설명]
- `DELETE /api/v1/[resource]/{id}` - [설명]

#### 2. Service Layer (비즈니스 로직)
**파일**: `app/features/[기능명]/service/[기능명]_service.py`

**책임**:
- 비즈니스 로직 구현
- 데이터 검증 및 가공
- Repository Layer 호출
- 트랜잭션 관리

**주요 메서드**:
- `create_[entity](data)` - [설명]
- `get_[entity]_by_id(id)` - [설명]
- `get_all_[entities]()` - [설명]
- `update_[entity](id, data)` - [설명]
- `delete_[entity](id)` - [설명]

#### 3. Repository Layer (데이터 접근)
**파일**: `app/features/[기능명]/repository/[기능명]_repository.py`

**책임**:
- 데이터베이스 CRUD 작업
- 쿼리 실행
- ORM 작업

**주요 메서드**:
- `create(db, entity)` - DB에 엔티티 저장
- `get_by_id(db, id)` - ID로 조회
- `get_all(db, skip, limit)` - 목록 조회
- `update(db, id, entity)` - 엔티티 수정
- `delete(db, id)` - 엔티티 삭제

## 데이터 흐름

```
Client Request
    ↓
Router (요청 검증, 스키마 변환)
    ↓
Service (비즈니스 로직)
    ↓
Repository (DB 작업)
    ↓
Database
    ↓
Repository (Entity 반환)
    ↓
Service (데이터 가공)
    ↓
Router (응답 스키마 변환)
    ↓
Client Response
```

## 스키마 설계

### Request 스키마
```python
class [Entity]Create(BaseModel):
    field1: [타입]
    field2: [타입]
```

### Response 스키마
```python
class [Entity]Response(BaseModel):
    id: int
    field1: [타입]
    field2: [타입]
    created_at: datetime
    updated_at: datetime
```

### Update 스키마
```python
class [Entity]Update(BaseModel):
    field1: Optional[[타입]]
    field2: Optional[[타입]]
```

## 에러 처리

| 상황 | HTTP 상태 코드 | 메시지 |
|------|----------------|--------|
| [에러 상황 1] | 400 | [에러 메시지] |
| [에러 상황 2] | 404 | [에러 메시지] |
| [에러 상황 3] | 409 | [에러 메시지] |
| [에러 상황 4] | 500 | [에러 메시지] |

## 검증 규칙

### 입력 검증
- field1: [검증 규칙]
- field2: [검증 규칙]

### 비즈니스 규칙
1. [규칙 1]
2. [규칙 2]

## 성능 고려사항
- [고려사항 1]
- [고려사항 2]

## 보안 고려사항
- [보안 사항 1]
- [보안 사항 2]

## 테스트 시나리오
1. [시나리오 1]
2. [시나리오 2]
3. [시나리오 3]

## 구현 체크리스트
- [ ] Entity 정의
- [ ] Repository 구현
- [ ] Service 구현
- [ ] Router 구현
- [ ] Schema 정의
- [ ] 테스트 코드 작성
- [ ] API 문서 업데이트
