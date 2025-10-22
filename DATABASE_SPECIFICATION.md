# LawMate 데이터베이스 명세서

## 📋 개요
이 문서는 현재 프론트엔드에서 사용 중인 더미 데이터를 바탕으로 실제 데이터베이스 구조와 API 엔드포인트를 정의합니다.

**작성일**: 2025년 10월 22일  
**버전**: 1.4 (사용자 요구사항 반영: 기본이미지 설정, 카테고리 제거, 익명기능 제거, AI상담 로직 개선)  
**대상**: 백엔드 개발자, DB 설계자

---

## 🏗️ 전체 시스템 아키텍처

### 데이터베이스 설계 원칙
- **3-Tier Architecture**: Router → Service → Repository
- **RESTful API**: 표준 HTTP 메서드 사용
- **정규화**: 3NF까지 정규화
- **외래키 제약**: 데이터 무결성 보장
- **인덱싱**: 검색 성능 최적화

---

## 📊 엔티티 관계도 (ERD)

### 주요 엔티티 관계
```
Users (일반회원)
   ↓ 1:N
Community_Posts (커뮤니티 게시글)
   ↓ 1:N
Community_Comments (댓글)

Users (일반회원)
   ↓ 1:N
AI_Consultations (AI 상담 기록)

Lawyer_Users (변호사회원)
   ↓ 1:1
Lawyer_Profiles (변호사 프로필)

Users (일반회원)
   ↓ M:N
Lawyer_Users (변호사회원) - Lawyer_Favorites (즐겨찾기)

독립적 엔티티:
- Case_Laws (판례)
- Legal_Dictionaries (법률사전)
- Notices (공지사항)
- Search_Logs (검색 기록)
```

---

## 📝 테이블 정의

### 1. 사용자 관리

#### 1.1 Users (일반 사용자)
```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '사용자 이름',
    email VARCHAR(255) NOT NULL UNIQUE COMMENT '이메일 (로그인 ID)',
    password_hash VARCHAR(255) NOT NULL COMMENT '암호화된 비밀번호',
    nickname VARCHAR(50) UNIQUE COMMENT '닉네임',
    address TEXT COMMENT '주소',
    profile_image VARCHAR(500) DEFAULT '/assets/Login_Image.png' COMMENT '프로필 이미지 URL (기본값: 기본 이미지)',
    is_active BOOLEAN DEFAULT TRUE COMMENT '계정 활성화 상태',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_nickname (nickname),
    INDEX idx_created_at (created_at)
) COMMENT='일반 사용자';
```

**샘플 데이터**:
```json
{
    "id": 1,
    "name": "홍길동",
    "email": "gildong@gmail.com",
    "password_hash": "$2b$12$...", 
    "nickname": "GilD",
    "address": "충청북도 충주시 충열 4길",
    "profile_image": "/assets/Login_Image.png",
    "is_active": true,
    "created_at": "2024-02-15T00:00:00Z",
    "updated_at": "2024-02-15T00:00:00Z"
}
```

#### 1.2 Lawyer_Users (변호사 사용자)
```sql
CREATE TABLE lawyer_users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '변호사 이름',
    email VARCHAR(255) NOT NULL UNIQUE COMMENT '이메일 (로그인 ID)',
    password_hash VARCHAR(255) NOT NULL COMMENT '암호화된 비밀번호',
    nickname VARCHAR(50) UNIQUE COMMENT '닉네임',
    phone VARCHAR(20) COMMENT '전화번호',
    law_firm VARCHAR(200) COMMENT '소속 법무법인',
    lawyer_registration_number VARCHAR(50) UNIQUE COMMENT '변호사 등록번호',
    address TEXT COMMENT '사무실 주소',
    certificate_file VARCHAR(500) COMMENT '변호사 자격증 파일 경로',
    is_verified BOOLEAN DEFAULT FALSE COMMENT '변호사 인증 상태',
    is_active BOOLEAN DEFAULT TRUE COMMENT '계정 활성화 상태',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_lawyer_reg_num (lawyer_registration_number),
    INDEX idx_verification (is_verified),
    INDEX idx_created_at (created_at)
) COMMENT='변호사 사용자';
```

#### 1.3 Lawyer_Profiles (변호사 프로필)
```sql
CREATE TABLE lawyer_profiles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    lawyer_user_id BIGINT NOT NULL,
    profile_image VARCHAR(500) DEFAULT '/assets/lawyer-pic.png' COMMENT '프로필 이미지 URL (기본값: 기본 변호사 이미지)',
    introduction LONGTEXT COMMENT '변호사 자기소개 (상담 가능 시간 포함)',
    specialties JSON COMMENT '전문 분야 배열',
    education JSON COMMENT '학력 사항 배열',
    career JSON COMMENT '경력 사항 배열 (experience → career로 변경)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (lawyer_user_id) REFERENCES lawyer_users(id) ON DELETE CASCADE,
    INDEX idx_lawyer_user_id (lawyer_user_id),
    FULLTEXT idx_introduction (introduction),
    FULLTEXT idx_specialties (specialties)
) COMMENT='변호사 프로필 상세정보 - 기본 프로필 이미지 설정';
```

#### 1.4 Lawyer_Favorites (변호사 즐겨찾기)
```sql
CREATE TABLE lawyer_favorites (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    lawyer_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lawyer_id) REFERENCES lawyer_users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_lawyer (user_id, lawyer_id),
    INDEX idx_user_id (user_id),
    INDEX idx_lawyer_id (lawyer_id)
) COMMENT='사용자의 변호사 즐겨찾기';
```

### 2. 콘텐츠 관리

#### 2.1 Notices (공지사항)
```sql
CREATE TABLE notices (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '제목',
    content TEXT NOT NULL COMMENT '내용 요약',
    full_content LONGTEXT COMMENT '전체 내용',
    author VARCHAR(100) DEFAULT '관리자' COMMENT '작성자',
    views INT DEFAULT 0 COMMENT '조회수',
    is_pinned BOOLEAN DEFAULT FALSE COMMENT '상단 고정 여부',
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '게시일',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_published_at (published_at),
    INDEX idx_pinned (is_pinned),
    FULLTEXT idx_search (title, content)
) COMMENT='공지사항';
```

#### 2.2 Community_Posts (커뮤니티 게시글)
```sql
CREATE TABLE community_posts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    category VARCHAR(50) COMMENT '카테고리 (잡담, 고민/상담, 후기 등)',
    title VARCHAR(200) NOT NULL COMMENT '제목',
    content LONGTEXT COMMENT '내용',
    views INT DEFAULT 0 COMMENT '조회수',
    comment_count INT DEFAULT 0 COMMENT '댓글 수',
    is_notice BOOLEAN DEFAULT FALSE COMMENT '공지글 여부',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_category (category),
    INDEX idx_created_at (created_at),
    INDEX idx_notice (is_notice),
    FULLTEXT idx_search (title, content)
) COMMENT='커뮤니티 게시글';
```

#### 2.3 Community_Comments (커뮤니티 댓글)
```sql
CREATE TABLE community_comments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT NOT NULL,
    user_id BIGINT,
    parent_comment_id BIGINT COMMENT '대댓글인 경우 부모 댓글 ID',
    content TEXT NOT NULL COMMENT '댓글 내용',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (post_id) REFERENCES community_posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (parent_comment_id) REFERENCES community_comments(id) ON DELETE CASCADE,
    INDEX idx_post_id (post_id),
    INDEX idx_user_id (user_id),
    INDEX idx_parent_comment (parent_comment_id),
    INDEX idx_created_at (created_at)
) COMMENT='커뮤니티 댓글';
```

### 3. 법률 정보

#### 3.1 Case_Laws (판례)
```sql
CREATE TABLE case_laws (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(500) NOT NULL COMMENT '사건명 (예: 대법원 2018. 1. 25. 선고 2015다24904 판결)',
    subtitle VARCHAR(500) COMMENT '부제목',
    court VARCHAR(100) COMMENT '법원명',
    case_number VARCHAR(100) COMMENT '사건번호',
    judgment_date DATE COMMENT '선고일',
    case_type VARCHAR(100) COMMENT '사건 유형',
    summary TEXT COMMENT '사건 요약',
    판시사항 LONGTEXT COMMENT '판시사항 전문',
    판결요지 LONGTEXT COMMENT '판결요지 전문',
    참조조문 LONGTEXT COMMENT '참조조문',
    참조판례 LONGTEXT COMMENT '참조판례',
    전문 LONGTEXT COMMENT '판례 전문',
    views INT DEFAULT 0 COMMENT '조회수',
    highlighted BOOLEAN DEFAULT FALSE COMMENT '하이라이트 여부',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_court (court),
    INDEX idx_case_number (case_number),
    INDEX idx_judgment_date (judgment_date),
    INDEX idx_case_type (case_type),
    INDEX idx_views (views),
    FULLTEXT idx_search (title, subtitle, summary, 판시사항, 판결요지)
) COMMENT='판례 정보';
```

#### 3.2 Legal_Dictionaries (법률 용어 사전)
```sql
CREATE TABLE legal_dictionaries (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    term VARCHAR(200) NOT NULL UNIQUE COMMENT '법률 용어',
    definition LONGTEXT NOT NULL COMMENT '용어 정의',
    first_consonant CHAR(1) COMMENT '초성 (ㄱ, ㄴ, ㄷ 등) - 초성별 필터링용',
    related_terms JSON COMMENT '관련 용어 배열',
    examples TEXT COMMENT '사용 예시',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_term (term),
    INDEX idx_first_consonant (first_consonant),
    FULLTEXT idx_search (term, definition)
) COMMENT='법률 용어 사전 - 초성별 필터링 및 키워드 검색 지원';
```

### 4. AI 상담 및 검색

#### 4.1 AI_Consultations (AI 상담 기록)
```sql
CREATE TABLE ai_consultations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    session_id VARCHAR(100) COMMENT '세션 ID',
    question LONGTEXT NOT NULL COMMENT '사용자 질문',
    ai_response LONGTEXT COMMENT 'AI 답변',
    legal_category VARCHAR(100) COMMENT '법률 분야 분류 (임금체불, 계약분쟁 등)',
    related_case_laws JSON COMMENT '관련 판례 ID 배열',
    consultation_keywords JSON COMMENT '상담 관련 키워드 배열 (변호사 검색용)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_legal_category (legal_category),
    INDEX idx_created_at (created_at),
    FULLTEXT idx_search (question, ai_response),
    FULLTEXT idx_keywords (consultation_keywords)
) COMMENT='AI 상담 기록 - 키워드 기반 변호사 추천';
```

#### 4.2 Search_Logs (검색 기록)
```sql
CREATE TABLE search_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    search_keyword VARCHAR(500) NOT NULL COMMENT '검색 키워드',
    search_type ENUM('case_law', 'dictionary', 'lawyer', 'general') COMMENT '검색 유형',
    result_count INT DEFAULT 0 COMMENT '검색 결과 수',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_search_type (search_type),
    INDEX idx_created_at (created_at),
    FULLTEXT idx_keyword (search_keyword)
) COMMENT='검색 기록';
```

---

## 🔗 API 엔드포인트 명세

### 1. 인증 관리

#### 1.1 사용자 회원가입
```http
POST /api/v1/users/register
```

**Request Body**:
```json
{
    "name": "홍길동",
    "email": "gildong@gmail.com",
    "password": "rlfehd123!",
    "nickname": "GilD",
    "address": "충청북도 충주시 충열 4길"
}
```

**Response (201 Created)**:
```json
{
    "id": 1,
    "name": "홍길동",
    "email": "gildong@gmail.com",
    "nickname": "GilD",
    "address": "충청북도 충주시 충열 4길",
    "profile_image": null,
    "is_active": true,
    "created_at": "2025-10-22T12:00:00Z",
    "updated_at": "2025-10-22T12:00:00Z"
}
```

#### 1.2 변호사 회원가입
```http
POST /api/v1/lawyers/register
```

**Request Body**:
```json
{
    "name": "김이박",
    "email": "klp123@gmail.com",
    "password": "rladlqkr123!",
    "nickname": "KimLP",
    "phone": "010-1234-5678",
    "law_firm": "법무법인 정의",
    "lawyer_registration_number": "20241234",
    "address": "서울특별시 서초구 서초중앙로 157 법조타운",
    "certificate_file": "lawyer_certificate_kim.pdf"
}
```

#### 1.3 로그인
```http
POST /api/v1/auth/login
```

**Request Body**:
```json
{
    "email": "gildong@gmail.com",
    "password": "rlfehd123!",
    "user_type": "user" // or "lawyer"
}
```

**Response (200 OK)**:
```json
{
    "access_token": "eyJhbGciOiJIUzI1...",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
        "id": 1,
        "name": "홍길동",
        "email": "gildong@gmail.com",
        "user_type": "user"
    }
}
```

### 2. 공지사항 관리

#### 2.1 공지사항 목록 조회
```http
GET /api/v1/notices?page=1&limit=10
```

**Response (200 OK)**:
```json
{
    "items": [
        {
            "id": 1,
            "title": "웹 사이트 점검 안내",
            "content": "2025년 11월 6일 오후 3시~오후 6시 동안 웹 사이트 점검을 실시할 예정입니다.",
            "author": "관리자",
            "views": 32,
            "published_at": "2025-11-06T00:00:00Z",
            "created_at": "2025-11-06T00:00:00Z"
        }
    ],
    "total": 4,
    "page": 1,
    "per_page": 10,
    "total_pages": 1
}
```

#### 2.2 공지사항 상세 조회
```http
GET /api/v1/notices/{id}
```

**Response (200 OK)**:
```json
{
    "id": 1,
    "title": "웹 사이트 점검 안내",
    "content": "2025년 11월 6일 오후 3시~오후 6시 동안...",
    "full_content": "안녕하세요, 고객 여러분...",
    "author": "관리자",
    "views": 33,
    "is_pinned": false,
    "published_at": "2025-11-06T00:00:00Z",
    "created_at": "2025-11-06T00:00:00Z",
    "updated_at": "2025-11-06T00:00:00Z"
}
```

### 3. 커뮤니티 관리

#### 3.1 커뮤니티 게시글 목록 조회
```http
GET /api/v1/community/posts?page=1&limit=20&category=전체
```

**Response (200 OK)**:
```json
{
    "items": [
        {
            "id": 123455,
            "category": "잡담",
            "title": "점매추~~~!!!",
            "date": "01:01",
            "views": 3,
            "comment_count": 0,
            "is_notice": false,
            "created_at": "2025-10-22T01:01:00Z"
        }
    ],
    "total": 20,
    "page": 1,
    "per_page": 20,
    "total_pages": 1
}
```

#### 3.2 커뮤니티 게시글 작성
```http
POST /api/v1/community/posts
```

**Request Body**:
```json
{
    "category": "고민/상담",
    "title": "법률 상담 받고 싶어요",
    "content": "상세한 상담 내용..."
}
```

### 4. 변호사 프로필 관리

#### 4.1 변호사 목록 조회
```http
GET /api/v1/lawyers?page=1&limit=10&specialty=민사소송&region=서울
```

**Response (200 OK)**:
```json
{
    "items": [
        {
            "id": 1,
            "name": "김이박",
            "image": "/assets/haein.png",
            "introduction": "14년차 변호사 김이박입니다. 민사분야에 특화된 변호사로서...",
            "specialties": ["민사소송", "손해배상", "계약법"],
            "specialtyCount": 5,
            "experience": [
                "서울중앙지방법원 국선변호인",
                "대형로펌 파트너 변호사 출신"
            ],
            "experienceCount": 5,
            "region": "서울·경기·온라인 상담 가능"
        }
    ],
    "total": 6,
    "page": 1,
    "per_page": 9,
    "total_pages": 1
}
```

#### 4.2 변호사 프로필 상세 조회
```http
GET /api/v1/lawyers/{id}/profile
```

**Response (200 OK)**:
```json
{
    "id": 1,
    "name": "홍길동",
    "image": "/assets/lawyer-pic.png",
    "introduction": "상담 가능 시간: 평일 09:30 ~ 17:30 / 점심시간 12:30 ~ 13:30 제외\n토요일 오전 10시 ~ 12시 (사전 예약 시)\n※ 공휴일 및 일요일은 상담이 어렵습니다.\n\n민사소송, 계약 분쟁, 임대차 문제 등 실생활과 밀접한 법률 문제를 중심으로 약 8년간 다양한 사건을 수행해 왔습니다...",
    "contact": {
        "name": "홍길동",
        "phone": "02-1234-1121",
        "email": "hahaha@kku.ac.kr",
        "address": "서울특별시 서초구 서초대로 219 유진빌딩 3층 306호"
    },
    "specialties": [
        "회사/창업", "민사/소송", "형사/소송", "사기/공갈",
        "음주/무면허", "임대차", "가압류/가처분", "횡령/배임"
    ],
    "education": [
        "이화여자대학교 법과대학 법학과 졸업",
        "이화여자대학교 법학전문대학원 전문석사 졸업"
    ],
    "career": [
        "변호사, 변리사, 세무사 자격증",
        "대한변호사협회 대의원",
        "대법원 국선변호사"
    ]
}
```

#### 4.3 변호사 즐겨찾기 추가/제거
```http
POST /api/v1/lawyers/{lawyer_id}/favorite
DELETE /api/v1/lawyers/{lawyer_id}/favorite
```

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Response (200 OK)**:
```json
{
    "success": true,
    "is_favorited": true,
    "message": "즐겨찾기에 추가되었습니다"
}
```

#### 4.4 내 즐겨찾기 변호사 목록
```http
GET /api/v1/lawyers/favorites?page=1&limit=10
```

**Response (200 OK)**:
```json
{
    "items": [
        {
            "id": 1,
            "name": "김이박",
            "image": "/assets/haein.png",
            "specialties": ["민사소송", "손해배상", "계약법"],
            "region": "서울·경기·온라인 상담 가능",
            "favorited_at": "2025-10-22T10:30:00Z"
        }
    ],
    "total": 3,
    "page": 1,
    "per_page": 10,
    "total_pages": 1
}
```

### 5. 판례 관리

#### 5.1 판례 검색
```http
GET /api/v1/case-laws/search?q=임대차&page=1&limit=10&court=대법원
```

**Response (200 OK)**:
```json
{
    "items": [
        {
            "id": 1,
            "title": "대법원 2021.04.01 선고 2020다286102 판결 [건물명도(인도)ㆍ보증금반환]",
            "court": "대법원",
            "case_number": "2020다286102",
            "judgment_date": "2021-04-01",
            "summary": "[1] 임대차계약이 종료된 후 임대차보증금이 반환되지 않은 상태에서...",
            "case_type": "민사",
            "views": 156
        }
    ],
    "total": 6,
    "page": 1,
    "per_page": 10,
    "total_pages": 1
}
```

#### 5.2 판례 상세 조회
```http
GET /api/v1/case-laws/{id}
```

**Response (200 OK)**:
```json
{
    "id": 1,
    "title": "대법원 2018. 1. 25. 선고 2015다24904, 24911, 24928, 24935 판결",
    "subtitle": "[ 손해배상(기)·손해배상(기)·손해배상(기)·손해배상(기) ] 〈네이트·싸이월드 회원들의 개인정보 유출로 인한 손해배상 청구사건〉[공2018상,491]",
    "court": "대법원",
    "case_number": "2015다24904",
    "judgment_date": "2018-01-25",
    "판시사항": "【판시사항】\n[1] 정보통신서비스 제공자가 구 정보통신망 이용촉진 및 정보보호 등에 관한 법률...",
    "판결요지": "【판결요지】\n[1] 구 정보통신망 이용촉진 및 정보보호 등에 관한 법률...",
    "참조조문": "【참조조문】\n[1] 구 정보통신망 이용촉진 및 정보보호 등에 관한 법률...",
    "참조판례": "【참조판례】\n[1][2] 대법원 2015. 2. 12. 선고 2013다43994, 44003 판결...",
    "전문": "【전 문】\n【원고(선정당사자), 상고인】 원고(선정당사자) 1 외 3인...",
    "views": 156
}
```
```json
{
    "id": 1,
    "title": "대법원 2018. 1. 25. 선고 2015다24904 판결",
    "subtitle": "손해배상(기) 〈네이트·싸이월드 회원들의 개인정보 유출로 인한 손해배상 청구사건〉",
    "court": "대법원",
    "case_number": "2015다24904",
    "judgment_date": "2018-01-25",
    "judgment_summary": "【판시사항】...",
    "judgment_points": "【판결요지】...",
    "referenced_laws": "【참조조문】...",
    "referenced_cases": "【참조판례】...",
    "full_content": "【전 문】...",
    "views": 157,
    "created_at": "2025-10-22T12:00:00Z"
}
```

### 6. 법률 사전 관리

#### 6.1 법률 용어 검색
```http
GET /api/v1/dictionary/search?q=민&consonant=ㅁ&page=1&limit=15
```

**쿼리 파라미터**:
- `q`: 검색 키워드 (선택사항) - 예: "민" 입력시 "민사", "민법", "민형사상" 등 검색
- `consonant`: 초성 필터 (ㄱ, ㄴ, ㄷ, ㄹ, ㅁ, ㅂ, ㅅ, ㅇ, ㅈ, ㅊ, ㅋ, ㅌ, ㅍ, ㅎ) - 기본값: "전체"
- `page`: 페이지 번호
- `limit`: 페이지당 항목 수

**Response (200 OK)**:
```json
{
    "items": [
        {
            "id": 1,
            "term": "민사",
            "definition": "개인과 개인 사이의 사법상 법률관계에 관한 사건을 다루는 법률 분야로..."
        },
        {
            "id": 2,
            "term": "민법",
            "definition": "사인간의 재산관계와 가족관계를 규율하는 기본법으로..."
        },
        {
            "id": 3,
            "term": "민형사상",
            "definition": "민사사건과 형사사건이 함께 관련된 법적 상황을..."
        }
    ],
    "total": 15,
    "page": 1,
    "per_page": 15,
    "total_pages": 1
}
```

#### 6.2 법률 용어 상세 조회
```http
GET /api/v1/dictionary/{term}
```

**Response (200 OK)**:
```json
{
    "id": 1,
    "term": "공법",
    "definition": "공법(公法, 영어: public law)은 국가의 조직이나 공공단체 상호간 또는 이들과 개인의 관계를 규정하는 법률로...",
    "related_terms": ["사법", "헌법", "행정법"],
    "examples": "헌법·행정법·형법·소송법·국제법 등이 이 법에 해당한다."
}
```

### 7. AI 상담 관리

#### 7.1 AI 상담 요청
```http
POST /api/v1/ai/consultation
```

**Request Body**:
```json
{
    "question": "3달 전에 일했던 가게에서 사장님이 알바비를 3달째 안주고있어 어떻게 해야하나요?",
    "session_id": "session_123456"
}
```

**Response (200 OK)**:
```json
{
    "ai_response": {
        "highlight": "3달 전에 일했던 가게에서 사장님이 알바비를 3달째 안 주고 있어 어떻게 해야하나요?",
        "description": "사장님이 알바비를 고의로 주지 않는 것이라면, 근로기준법 위반으로 처벌을 받을 수 있습니다..."
    },
    "law_category": {
        "title": "근로기준법 위반 (구 노사)",
        "description": "사업주는 근로자가 일한 것은 반환할 경우 그 대가를 제때 지급해야 하며..."
    },
    "related_precedents": [
        {
            "id": 1,
            "court": "대법원",
            "case_number": "1994.10.28. 선고 94다26015 판결",
            "summary": "근로기준법 위반상에 해당될 경우 및 기숙사수..."
        }
    ],
    "consultation_keywords": ["임금체불", "근로기준법", "노동법"],
    "recommended_lawyers_preview": [
        {
            "id": 1,
            "name": "김이박",
            "specialties": ["손해배상", "노동법"],
            "contact_phone": "02-555-1234",
            "contact_email": "kim@lawfirm.com",
            "region": "서울·경기"
        }
    ],
    "more_lawyers_url": "/api/v1/lawyers/search?keywords=임금체불,근로기준법,노동법"
}
```

#### 7.2 키워드 기반 변호사 검색 (AI 상담 관련)
```http
GET /api/v1/lawyers/search?keywords=임금체불,근로기준법,노동법&page=1&limit=10
```

**쿼리 파라미터**:
- `keywords`: 쉼표로 구분된 키워드 배열
- `page`: 페이지 번호  
- `limit`: 페이지당 항목 수

**Response (200 OK)**:
```json
{
    "items": [
        {
            "id": 1,
            "name": "김이박", 
            "image": "/assets/haein.png",
            "specialties": ["손해배상", "노동법", "임금체불"],
            "experience": ["노동법 전문변호사", "임금체불 전담팀"],
            "region": "서울·경기·온라인 상담 가능",
            "contact": {
                "phone": "02-555-1234",
                "email": "kim@lawfirm.com"
            }
        }
    ],
    "total": 5,
    "page": 1,  
    "per_page": 10,
    "total_pages": 1,
    "search_keywords": ["임금체불", "근로기준법", "노동법"]
}
```

---

## 🔒 보안 및 인증

### JWT 토큰 기반 인증
- **Access Token**: 1시간 유효
- **Refresh Token**: 7일 유효
- **토큰 갱신**: `/api/v1/auth/refresh` 엔드포인트

### 데이터 보안
- **비밀번호**: bcrypt 해시 (salt rounds: 12)
- **개인정보 암호화**: AES-256 사용
- **HTTPS 강제**: 모든 API 통신
- **CORS 설정**: 허용된 도메인만 접근

### 접근 권한 관리
- **일반 사용자**: 기본 조회, 커뮤니티 참여
- **변호사**: 프로필 관리, 상담 응답
- **관리자**: 모든 데이터 관리

---

## 📈 성능 최적화

### 인덱싱 전략
- **Primary Key**: 모든 테이블에 Auto Increment
- **Foreign Key**: 관계 테이블 조인 최적화
- **Full-text Index**: 검색 기능 성능 향상
- **Composite Index**: 복합 조건 검색 최적화

### 캐싱 전략
- **Redis 캐시**: 자주 조회되는 데이터 (공지사항, 판례)
- **Query Result Cache**: 복잡한 검색 결과
- **Session Cache**: 사용자 세션 정보

### 페이징 및 제한
- **기본 페이지 크기**: 10-20개
- **최대 페이지 크기**: 100개
- **커서 기반 페이징**: 대용량 데이터 처리

---

## 🔄 데이터 마이그레이션

### 더미 데이터 → 실제 DB 이관 계획
1. **사용자 데이터**: 테스트 계정 생성
2. **공지사항**: 현재 더미 데이터 이관
3. **판례 데이터**: 실제 대법원 판례 연동
4. **법률 사전**: 법제처 용어집 연동
5. **FAQ**: 초기 데이터 입력

### 데이터 검증 규칙
- **이메일 형식**: RFC 5322 준수
- **전화번호**: 한국 전화번호 형식
- **비밀번호**: 최소 8자, 영문+숫자+특수문자
- **파일 업로드**: 이미지 10MB, 문서 50MB 제한

---

## 📋 개발 우선순위

### Phase 1 (필수 기능)
1. **사용자 인증**: 회원가입, 로그인, JWT
2. **공지사항**: CRUD + 관리자 기능
3. **기본 검색**: 판례, 법률사전 검색
4. **변호사 프로필**: 조회 기능

### Phase 2 (핵심 기능)
1. **커뮤니티**: 게시글, 댓글 시스템
2. **AI 상담**: OpenAI API 연동
3. **변호사 상담**: 예약 및 상담 시스템

### Phase 3 (고도화)
1. **실시간 알림**: WebSocket 연동
2. **결제 시스템**: 상담료 결제
3. **통계 대시보드**: 관리자 페이지
4. **모바일 최적화**: 반응형 API

---

## 📞 기술 지원

### API 문서
- **Swagger UI**: `/docs` 엔드포인트에서 확인
- **ReDoc**: `/redoc` 엔드포인트에서 확인

### 개발 환경
- **언어**: Python 3.11+
- **프레임워크**: FastAPI
- **데이터베이스**: MySQL 8.0+
- **캐시**: Redis 7.0+
- **배포**: Docker + Docker Compose

### 연락처
- **백엔드 개발**: backend-team@lawmate.com
- **데이터베이스**: db-admin@lawmate.com
- **기술 지원**: support@lawmate.com

---

**📅 최종 업데이트**: 2025년 10월 22일  
**📝 문서 버전**: 1.0  
**✅ 검토자**: 백엔드 개발팀