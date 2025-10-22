# 사용자 관리 API 엔드포인트 문서

## 기본 정보
- **기능명**: 사용자 관리 (User Management)
- **Base URL**: `/api/v1/users`
- **작성일**: 2025-10-08
- **버전**: 1.0

---

## 1. 사용자 생성

### 엔드포인트
```
POST /api/v1/users
```

### 설명
새로운 사용자를 생성합니다. 이메일 중복 검증이 수행됩니다.

### Request Headers
```
Content-Type: application/json
```

### Request Body
```json
{
  "email": "user@example.com",
  "name": "홍길동",
  "age": 25,
  "is_active": true
}
```

#### 필드 설명
| 필드명 | 타입 | 필수 | 설명 | 제약조건 |
|--------|------|------|------|----------|
| email | string | O | 사용자 이메일 | 유효한 이메일 형식, 최대 255자, 중복 불가 |
| name | string | O | 사용자 이름 | 1자 이상 100자 이하 |
| age | integer | X | 나이 | 0 이상 150 이하 |
| is_active | boolean | X | 활성화 상태 | 기본값: true |

### Response

#### 성공 (201 Created)
```json
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

#### 실패
- **400 Bad Request**: 잘못된 요청 데이터
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

- **409 Conflict**: 이메일 중복
```json
{
  "detail": "Email already exists"
}
```

### 예제
```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "홍길동",
    "age": 25
  }'
```

---

## 2. 사용자 목록 조회

### 엔드포인트
```
GET /api/v1/users
```

### 설명
등록된 사용자 목록을 조회합니다. 페이지네이션을 지원합니다.

### Query Parameters
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| skip | integer | X | 0 | 건너뛸 항목 수 (offset) |
| limit | integer | X | 100 | 조회할 최대 항목 수 |

### Response

#### 성공 (200 OK)
```json
[
  {
    "id": 1,
    "email": "user1@example.com",
    "name": "홍길동",
    "age": 25,
    "is_active": true,
    "created_at": "2025-10-08T12:00:00",
    "updated_at": "2025-10-08T12:00:00"
  },
  {
    "id": 2,
    "email": "user2@example.com",
    "name": "김철수",
    "age": 30,
    "is_active": true,
    "created_at": "2025-10-08T13:00:00",
    "updated_at": "2025-10-08T13:00:00"
  }
]
```

### 예제
```bash
# 첫 10개 조회
curl -X GET "http://localhost:8000/api/v1/users?skip=0&limit=10"

# 11번째부터 20개 조회
curl -X GET "http://localhost:8000/api/v1/users?skip=10&limit=20"
```

---

## 3. 사용자 단건 조회

### 엔드포인트
```
GET /api/v1/users/{id}
```

### 설명
특정 사용자의 정보를 조회합니다.

### Path Parameters
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| id | integer | O | 사용자 ID |

### Response

#### 성공 (200 OK)
```json
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

#### 실패
- **404 Not Found**: 사용자를 찾을 수 없음
```json
{
  "detail": "User not found"
}
```

### 예제
```bash
curl -X GET "http://localhost:8000/api/v1/users/1"
```

---

## 4. 사용자 정보 수정

### 엔드포인트
```
PUT /api/v1/users/{id}
```

### 설명
사용자 정보를 수정합니다. 제공된 필드만 업데이트됩니다.

### Path Parameters
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| id | integer | O | 사용자 ID |

### Request Body
```json
{
  "name": "홍길동_수정",
  "age": 26
}
```

#### 필드 설명
| 필드명 | 타입 | 필수 | 설명 | 제약조건 |
|--------|------|------|------|----------|
| email | string | X | 사용자 이메일 | 유효한 이메일 형식, 최대 255자, 중복 불가 |
| name | string | X | 사용자 이름 | 1자 이상 100자 이하 |
| age | integer | X | 나이 | 0 이상 150 이하 |
| is_active | boolean | X | 활성화 상태 | - |

### Response

#### 성공 (200 OK)
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "홍길동_수정",
  "age": 26,
  "is_active": true,
  "created_at": "2025-10-08T12:00:00",
  "updated_at": "2025-10-08T14:00:00"
}
```

#### 실패
- **404 Not Found**: 사용자를 찾을 수 없음
- **400 Bad Request**: 잘못된 요청 데이터
- **409 Conflict**: 이메일 중복 (이메일 수정 시)

### 예제
```bash
curl -X PUT "http://localhost:8000/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "홍길동_수정",
    "age": 26
  }'
```

---

## 5. 사용자 삭제

### 엔드포인트
```
DELETE /api/v1/users/{id}
```

### 설명
사용자를 삭제합니다. 물리적 삭제가 수행됩니다.

### Path Parameters
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| id | integer | O | 사용자 ID |

### Response

#### 성공 (204 No Content)
본문 없음

#### 실패
- **404 Not Found**: 사용자를 찾을 수 없음
```json
{
  "detail": "User not found"
}
```

### 예제
```bash
curl -X DELETE "http://localhost:8000/api/v1/users/1"
```

---

## 공통 에러 응답

### 422 Unprocessable Entity
요청 형식은 올바르나 데이터 검증 실패
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "ensure this value is less than or equal to 150",
      "type": "value_error.number.not_le"
    }
  ]
}
```

### 500 Internal Server Error
서버 내부 오류
```json
{
  "detail": "Internal server error"
}
```

## 테스트 체크리스트
- [x] 사용자 생성 API 정상 동작 확인
- [x] 중복 이메일로 생성 시 409 에러 확인
- [x] 사용자 목록 조회 API 정상 동작 확인
- [x] 페이지네이션 동작 확인 (skip, limit)
- [x] 사용자 단건 조회 API 정상 동작 확인
- [x] 존재하지 않는 사용자 조회 시 404 확인
- [x] 사용자 수정 API 정상 동작 확인
- [x] 부분 수정 동작 확인
- [x] 사용자 삭제 API 정상 동작 확인
- [x] 잘못된 이메일 형식 시 400/422 에러 확인
- [x] 나이 범위 초과 시 400/422 에러 확인
- [x] 빈 이름 입력 시 400/422 에러 확인
