# [기능명] API 엔드포인트 문서

## 기본 정보
- **기능명**: [기능 이름]
- **Base URL**: `/api/v1/[resource]`
- **작성일**: [YYYY-MM-DD]
- **버전**: 1.0

---

## 1. [리소스] 생성

### 엔드포인트
```
POST /api/v1/[resource]
```

### 설명
[엔드포인트 설명]

### Request Headers
```
Content-Type: application/json
```

### Request Body
```json
{
  "field1": "값1",
  "field2": "값2",
  "field3": "값3"
}
```

#### 필드 설명
| 필드명 | 타입 | 필수 | 설명 | 제약조건 |
|--------|------|------|------|----------|
| field1 | string | O | [설명] | [제약조건] |
| field2 | integer | O | [설명] | [제약조건] |
| field3 | string | X | [설명] | [제약조건] |

### Response

#### 성공 (201 Created)
```json
{
  "id": 1,
  "field1": "값1",
  "field2": "값2",
  "field3": "값3",
  "created_at": "2025-10-08T12:00:00",
  "updated_at": "2025-10-08T12:00:00"
}
```

#### 실패
- **400 Bad Request**: 잘못된 요청 데이터
```json
{
  "detail": "Validation error: field1 is required"
}
```

- **409 Conflict**: 중복된 데이터
```json
{
  "detail": "[Resource] already exists"
}
```

### 예제
```bash
curl -X POST "http://localhost:8000/api/v1/[resource]" \
  -H "Content-Type: application/json" \
  -d '{
    "field1": "값1",
    "field2": "값2"
  }'
```

---

## 2. [리소스] 목록 조회

### 엔드포인트
```
GET /api/v1/[resource]
```

### 설명
[엔드포인트 설명]

### Query Parameters
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| skip | integer | X | 0 | 건너뛸 항목 수 |
| limit | integer | X | 100 | 조회할 최대 항목 수 |

### Response

#### 성공 (200 OK)
```json
[
  {
    "id": 1,
    "field1": "값1",
    "field2": "값2",
    "created_at": "2025-10-08T12:00:00",
    "updated_at": "2025-10-08T12:00:00"
  },
  {
    "id": 2,
    "field1": "값3",
    "field2": "값4",
    "created_at": "2025-10-08T13:00:00",
    "updated_at": "2025-10-08T13:00:00"
  }
]
```

### 예제
```bash
curl -X GET "http://localhost:8000/api/v1/[resource]?skip=0&limit=10"
```

---

## 3. [리소스] 단건 조회

### 엔드포인트
```
GET /api/v1/[resource]/{id}
```

### 설명
[엔드포인트 설명]

### Path Parameters
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| id | integer | O | [리소스] ID |

### Response

#### 성공 (200 OK)
```json
{
  "id": 1,
  "field1": "값1",
  "field2": "값2",
  "created_at": "2025-10-08T12:00:00",
  "updated_at": "2025-10-08T12:00:00"
}
```

#### 실패
- **404 Not Found**: 리소스를 찾을 수 없음
```json
{
  "detail": "[Resource] not found"
}
```

### 예제
```bash
curl -X GET "http://localhost:8000/api/v1/[resource]/1"
```

---

## 4. [리소스] 수정

### 엔드포인트
```
PUT /api/v1/[resource]/{id}
```

### 설명
[엔드포인트 설명]

### Path Parameters
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| id | integer | O | [리소스] ID |

### Request Body
```json
{
  "field1": "수정된 값1",
  "field2": "수정된 값2"
}
```

### Response

#### 성공 (200 OK)
```json
{
  "id": 1,
  "field1": "수정된 값1",
  "field2": "수정된 값2",
  "created_at": "2025-10-08T12:00:00",
  "updated_at": "2025-10-08T14:00:00"
}
```

#### 실패
- **404 Not Found**: 리소스를 찾을 수 없음
- **400 Bad Request**: 잘못된 요청 데이터

### 예제
```bash
curl -X PUT "http://localhost:8000/api/v1/[resource]/1" \
  -H "Content-Type: application/json" \
  -d '{
    "field1": "수정된 값1"
  }'
```

---

## 5. [리소스] 삭제

### 엔드포인트
```
DELETE /api/v1/[resource]/{id}
```

### 설명
[엔드포인트 설명]

### Path Parameters
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| id | integer | O | [리소스] ID |

### Response

#### 성공 (204 No Content)
본문 없음

#### 실패
- **404 Not Found**: 리소스를 찾을 수 없음

### 예제
```bash
curl -X DELETE "http://localhost:8000/api/v1/[resource]/1"
```

---

## 공통 에러 응답

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## 테스트 체크리스트
- [ ] 생성 API 정상 동작 확인
- [ ] 목록 조회 API 정상 동작 확인
- [ ] 단건 조회 API 정상 동작 확인
- [ ] 수정 API 정상 동작 확인
- [ ] 삭제 API 정상 동작 확인
- [ ] 400 에러 처리 확인
- [ ] 404 에러 처리 확인
- [ ] 409 에러 처리 확인
- [ ] 페이지네이션 동작 확인
