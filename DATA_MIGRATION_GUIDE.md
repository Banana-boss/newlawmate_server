# LawMate 데이터 마이그레이션 가이드

## 📋 개요
현재 프론트엔드에서 사용 중인 더미 데이터(`demoData.js`)를 실제 데이터베이스로 이관하는 단계별 가이드입니다.

**작성일**: 2025년 10월 22일  
**대상**: 백엔드 개발자, DB 관리자  
**예상 소요시간**: 2-3주

---

## 🗂️ 현재 더미 데이터 현황

### 1. 데이터 파일 위치
```
src/data/demoData.js
```

### 2. 포함된 데이터 유형
- **공지사항**: 4개 항목
- **커뮤니티 게시글**: 20개 항목  
- **변호사 목록**: 3개 기본 + 6개 상세 프로필
- **일반 사용자**: 1개 계정
- **변호사 사용자**: 1개 계정
- **판례 데이터**: 6개 판례 목록 (각 판례 클릭 시 상세 내용 표시, 1개 상세 판례 샘플)
- **법률 사전**: 15개 용어 목록 (각 용어 클릭 시 상세 정의 표시, 4개 상세 정의 샘플)
- **AI 상담 응답**: 샘플 응답 구조

---

## 🔄 마이그레이션 단계

### Phase 1: 기본 데이터 구조 생성 (1주차)

#### 1.1 데이터베이스 스키마 생성
```sql
-- 1. 사용자 관련 테이블
CREATE TABLE users (...);
CREATE TABLE lawyer_users (...);
CREATE TABLE lawyer_profiles (...);

-- 2. 콘텐츠 관련 테이블
CREATE TABLE notices (...);
CREATE TABLE community_posts (...);
CREATE TABLE community_comments (...);

-- 3. 법률 정보 관련 테이블
CREATE TABLE case_laws (...);
CREATE TABLE legal_dictionaries (...);

-- 4. 상담 관련 테이블
CREATE TABLE consultations (...);

-- 5. AI 상담 관련 테이블
CREATE TABLE ai_consultations (...);
CREATE TABLE search_logs (...);
```

#### 1.2 기본 인덱스 생성
```sql
-- 검색 성능 최적화를 위한 인덱스
CREATE INDEX idx_notices_category ON notices(category);
CREATE INDEX idx_notices_published_at ON notices(published_at);
CREATE FULLTEXT INDEX idx_notices_search ON notices(title, content);

CREATE INDEX idx_community_posts_category ON community_posts(category);
CREATE INDEX idx_community_posts_created_at ON community_posts(created_at);
CREATE FULLTEXT INDEX idx_community_posts_search ON community_posts(title, content);

CREATE INDEX idx_case_laws_court ON case_laws(court);
CREATE INDEX idx_case_laws_judgment_date ON case_laws(judgment_date);
CREATE FULLTEXT INDEX idx_case_laws_search ON case_laws(title, summary, content);

CREATE INDEX idx_legal_dictionaries_term ON legal_dictionaries(term);
CREATE FULLTEXT INDEX idx_legal_dictionaries_search ON legal_dictionaries(term, definition);
```

### Phase 2: 더미 데이터 변환 및 삽입 (2주차)

#### 2.1 공지사항 데이터 이관
```javascript
// demoData.js의 demoNotices 배열을 SQL INSERT문으로 변환
const demoNotices = [
  {
    id: 1,
    category: '공지사항',
    title: '웹 사이트 점검 안내',
    content: '2025년 11월 6일 오후 3시~오후 6시 동안 웹 사이트 점검을 실시할 예정입니다.',
    date: '2025-11-6',
    views: 32,
    author: '관리자',
    fullContent: `안녕하세요, 고객 여러분...`
  }
  // ... 나머지 데이터
];
```

**변환된 SQL**:
```sql
INSERT INTO notices (category, title, content, full_content, author, views, published_at, created_at) VALUES
('공지사항', '웹 사이트 점검 안내', '2025년 11월 6일 오후 3시~오후 6시 동안 웹 사이트 점검을 실시할 예정입니다.', 
 '안녕하세요, 고객 여러분.\n더 나은 서비스 제공을 위한 시스템 점검이 예정되어...', 
 '관리자', 32, '2025-11-06', NOW()),
('이벤트', '11월 로우메이트(Lawmate) 이벤트 개최', '새 달을 맞이하여 로우메이트(Lawmate)가 새로운 이벤트를 개최하였습니다!',
 '새 달을 맞이하여 로우메이트(Lawmate)가 새로운 이벤트를 개최하였습니다!...', 
 '마케팅팀', 32, '2025-11-01', NOW()),
-- ... 나머지 데이터
;
```

#### 2.2 사용자 데이터 이관
```javascript
// demoUsers와 demoLawyerUsers 데이터 변환
const demoUsers = [{
  id: 1,
  name: '홍길동',
  email: 'gildong@gmail.com',
  password: 'rlfehd123!', // 해시화 필요
  nickname: 'GilD',
  address: '충청북도 충주시 충열 4길',
  createdAt: '2024-02-15',
  isLawyer: false
}];
```

**변환된 SQL**:
```sql
-- 일반 사용자
INSERT INTO users (name, email, password_hash, nickname, address, created_at) VALUES
('홍길동', 'gildong@gmail.com', '$2b$12$hash...', 'GilD', '충청북도 충주시 충열 4길', '2024-02-15');

-- 변호사 사용자
INSERT INTO lawyer_users (name, email, password_hash, nickname, phone, law_firm, lawyer_registration_number, address, is_verified, created_at) VALUES
('김이박', 'klp123@gmail.com', '$2b$12$hash...', 'KimLP', '010-1234-5678', '법무법인 정의', '20241234', '서울특별시 서초구 서초중앙로 157 법조타운', TRUE, '2025-01-10');

-- 변호사 프로필
INSERT INTO lawyer_profiles (lawyer_user_id, profile_image, introduction, specialties, experience, consultation_fee, rating, total_consultations, total_reviews) VALUES
(1, '/assets/haein.png', '14년차 변호사 김이박입니다...', 
 JSON_ARRAY('민사소송', '손해배상', '계약법'), 
 JSON_ARRAY('서울중앙지방법원 국선변호인', '대형로펌 파트너 변호사 출신'), 
 200000, 4.8, 1304, 127);
```

#### 2.3 커뮤니티 데이터 이관
```sql
-- 커뮤니티 게시글
INSERT INTO community_posts (user_id, category, title, views, comment_count, is_notice, created_at) VALUES
(NULL, '잡담', '점매추~~~!!!', 3, 0, FALSE, '2025-10-22 01:01:00'),
(NULL, '고민/상담', '살려주세요ㅠㅠ', 12, 0, FALSE, '2025-10-22 00:35:00'),
-- ... 나머지 데이터
;

-- 공지글 처리
INSERT INTO community_posts (user_id, category, title, views, comment_count, is_notice, created_at) VALUES
(NULL, '', '[공지] 변호사 언급 금지', 25420, 0, TRUE, '2024-04-09'),
(NULL, '', '◤LM커뮤 이용 규칙◢', 25555, 0, TRUE, '2020-04-29'),
-- ... 나머지 공지글
;
```

#### 2.4 법률 정보 데이터 이관
```sql
-- 판례 데이터
INSERT INTO case_laws (title, court, case_number, judgment_date, case_type, summary, content, views) VALUES
('대법원 2021.04.01 선고 2020다286102 판결 [건물명도(인도)ㆍ보증금반환][공보불게재]', 
 '대법원', '2020다286102', '2021-04-01', '민사',
 '[1] 임대차계약이 종료된 후 임대차보증금이 반환되지 않은 상태에서 임차인이 임대차목적물을 사용·수익하지 않고 점유만을 계속하고 있는 경우...',
 '전체 판례 내용...', 0),
-- ... 나머지 판례 데이터
;

-- 법률 사전 데이터  
INSERT INTO legal_dictionaries (term, definition, category) VALUES
('공법', '공법은 국가의 조직이나 공공단체 상호간 또는 이들과 개인의 관계를 규정하는 법률로 헌법·행정법·형법·소송법...', '법학개론'),
('권리청원', '권리청원이란 1628년에 영국의회가 찰스 1세의 승인을 얻은 국민의 인권에 관한 선언으로...', '헌법학'),
-- ... 나머지 용어 데이터
;
```

#### 2.5 AI 상담 응답 샘플 데이터 준비
```javascript
// AI 상담 응답 구조 샘플 (실제로는 OpenAI API 연동)
const demoSearchPageData = {
  searchKeyword: "사건1",
  aiResponse: {
    highlight: "3달 전에 일했던 가게에서 사장님이 알바비를 3달째 안 주고 있어 어떻게 해야하나요?",
    description: "사장님이 알바비를 고의로 주지 않는 것이라면, 근로기준법 위반으로 처벌을 받을 수 있습니다..."
  },
  lawCategory: {
    title: "근로기준법 위반 (구 노사)",
    description: "사업주는 근로자가 일한 것은 반환할 경우 그 대가를 제때 지급해야 하며..."
  },
  precedents: [...], // 관련 판례
  recommendedLawyers: [...] // 추천 변호사
};
```

### Phase 3: 데이터 검증 및 최적화 (3주차)

#### 3.1 데이터 무결성 검증
```sql
-- 1. 기본키 및 외래키 제약조건 확인
SELECT 
    TABLE_NAME,
    CONSTRAINT_NAME,
    CONSTRAINT_TYPE
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS 
WHERE TABLE_SCHEMA = 'lawmate_db';

-- 2. 인덱스 생성 확인
SHOW INDEX FROM notices;
SHOW INDEX FROM community_posts;
SHOW INDEX FROM case_laws;
SHOW INDEX FROM legal_dictionaries;

-- 3. 데이터 개수 확인
SELECT 'notices' as table_name, COUNT(*) as count FROM notices
UNION ALL
SELECT 'community_posts', COUNT(*) FROM community_posts
UNION ALL
SELECT 'case_laws', COUNT(*) FROM case_laws
UNION ALL
SELECT 'legal_dictionaries', COUNT(*) FROM legal_dictionaries
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'lawyer_users', COUNT(*) FROM lawyer_users
UNION ALL
SELECT 'lawyer_profiles', COUNT(*) FROM lawyer_profiles;
```

#### 3.2 성능 최적화
```sql
-- 1. Full-text 검색 인덱스 최적화
ALTER TABLE notices ADD FULLTEXT(title, content, full_content);
ALTER TABLE community_posts ADD FULLTEXT(title, content);
ALTER TABLE case_laws ADD FULLTEXT(title, summary, content);
ALTER TABLE legal_dictionaries ADD FULLTEXT(term, definition);

-- 2. 복합 인덱스 생성
CREATE INDEX idx_notices_category_date ON notices(category, published_at DESC);
CREATE INDEX idx_community_posts_category_date ON community_posts(category, created_at DESC);
CREATE INDEX idx_case_laws_court_date ON case_laws(court, judgment_date DESC);

-- 3. 통계 정보 업데이트
ANALYZE TABLE notices, community_posts, case_laws, legal_dictionaries, users, lawyer_users, lawyer_profiles;
```

#### 3.3 검색 기능 테스트
```sql
-- 1. 공지사항 검색 테스트
SELECT * FROM notices 
WHERE MATCH(title, content) AGAINST('점검' IN NATURAL LANGUAGE MODE)
LIMIT 10;

-- 2. 판례 검색 테스트  
SELECT * FROM case_laws 
WHERE MATCH(title, summary) AGAINST('임대차' IN NATURAL LANGUAGE MODE)
LIMIT 10;

-- 3. 법률 용어 검색 테스트
SELECT * FROM legal_dictionaries 
WHERE MATCH(term, definition) AGAINST('공법' IN NATURAL LANGUAGE MODE)
LIMIT 10;

-- 4. 변호사 검색 테스트
SELECT lp.*, lu.name, lu.email 
FROM lawyer_profiles lp
JOIN lawyer_users lu ON lp.lawyer_user_id = lu.id
WHERE JSON_CONTAINS(lp.specialties, '"민사소송"')
LIMIT 10;
```

---

## 🛠️ 마이그레이션 스크립트

### 자동화 스크립트 (Python)
```python
#!/usr/bin/env python3
"""
LawMate 더미 데이터 마이그레이션 스크립트
"""

import mysql.connector
import json
import bcrypt
from datetime import datetime
import os

class LawMateDataMigrator:
    def __init__(self, db_config):
        self.db = mysql.connector.connect(**db_config)
        self.cursor = self.db.cursor()
    
    def hash_password(self, password):
        """비밀번호 해시화"""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def migrate_notices(self, notices_data):
        """공지사항 데이터 마이그레이션"""
        sql = """
        INSERT INTO notices (category, title, content, full_content, author, views, published_at, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for notice in notices_data:
            values = (
                notice['category'],
                notice['title'],
                notice['content'],
                notice.get('fullContent', ''),
                notice['author'],
                notice['views'],
                notice['date'],
                datetime.now()
            )
            self.cursor.execute(sql, values)
        
        self.db.commit()
        print(f"✅ {len(notices_data)}개 공지사항 마이그레이션 완료")
    
    def migrate_users(self, users_data):
        """일반 사용자 데이터 마이그레이션"""
        sql = """
        INSERT INTO users (name, email, password_hash, nickname, address, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        for user in users_data:
            values = (
                user['name'],
                user['email'],
                self.hash_password(user['password']),
                user['nickname'],
                user.get('address', ''),
                user['createdAt']
            )
            self.cursor.execute(sql, values)
        
        self.db.commit()
        print(f"✅ {len(users_data)}개 사용자 마이그레이션 완료")
    
    def migrate_lawyer_users(self, lawyer_users_data):
        """변호사 사용자 데이터 마이그레이션"""
        user_sql = """
        INSERT INTO lawyer_users (name, email, password_hash, nickname, phone, law_firm, 
                                lawyer_registration_number, address, is_verified, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        profile_sql = """
        INSERT INTO lawyer_profiles (lawyer_user_id, specialties, experience, consultation_fee, 
                                   rating, total_consultations, total_reviews)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        for lawyer in lawyer_users_data:
            # 변호사 기본 정보 삽입
            user_values = (
                lawyer['name'],
                lawyer['email'],
                self.hash_password(lawyer['password']),
                lawyer['nickname'],
                lawyer.get('phone', ''),
                lawyer.get('lawFirm', ''),
                lawyer.get('lawyerRegistrationNumber', ''),
                lawyer.get('address', ''),
                True,  # is_verified
                lawyer['createdAt']
            )
            self.cursor.execute(user_sql, user_values)
            lawyer_user_id = self.cursor.lastrowid
            
            # 변호사 프로필 정보 삽입
            profile_values = (
                lawyer_user_id,
                json.dumps(lawyer.get('specialties', []), ensure_ascii=False),
                json.dumps(lawyer.get('experience', []), ensure_ascii=False),
                lawyer.get('consultationFee', 0),
                lawyer.get('rating', 0.0),
                lawyer.get('reviews', 0),
                lawyer.get('reviews', 0)
            )
            self.cursor.execute(profile_sql, profile_values)
        
        self.db.commit()
        print(f"✅ {len(lawyer_users_data)}개 변호사 마이그레이션 완료")
    
    def migrate_community_posts(self, posts_data):
        """커뮤니티 게시글 데이터 마이그레이션"""
        sql = """
        INSERT INTO community_posts (category, title, views, comment_count, is_notice, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        for post in posts_data:
            # 날짜 형식 변환
            created_at = self.parse_date(post['date'])
            
            values = (
                post.get('category', ''),
                post['title'],
                int(post['views'].replace(',', '')) if isinstance(post['views'], str) else post['views'],
                post.get('commentCount', 0),
                post.get('isNotice', False),
                created_at
            )
            self.cursor.execute(sql, values)
        
        self.db.commit()
        print(f"✅ {len(posts_data)}개 커뮤니티 게시글 마이그레이션 완료")
    
    def migrate_case_laws(self, case_laws_data):
        """판례 데이터 마이그레이션"""
        sql = """
        INSERT INTO case_laws (title, summary, content, views, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        for case_law in case_laws_data:
            values = (
                case_law['title'],
                case_law['content'][:500],  # summary는 처음 500자
                case_law['content'],
                0,  # 초기 조회수
                datetime.now()
            )
            self.cursor.execute(sql, values)
        
        self.db.commit()
        print(f"✅ {len(case_laws_data)}개 판례 마이그레이션 완료")
    
    def migrate_legal_dictionary(self, dictionary_data):
        """법률 사전 데이터 마이그레이션"""
        sql = """
        INSERT INTO legal_dictionaries (term, definition, category)
        VALUES (%s, %s, %s)
        """
        
        for item in dictionary_data:
            values = (
                item['term'],
                item['definition'],
                '법학개론'  # 기본 카테고리
            )
            self.cursor.execute(sql, values)
        
        self.db.commit()
        print(f"✅ {len(dictionary_data)}개 법률 용어 마이그레이션 완료")
    
    def parse_date(self, date_str):
        """날짜 문자열을 datetime 객체로 변환"""
        if date_str in ['01:01', '00:35', '00:30']:
            # 시간만 있는 경우 오늘 날짜로 설정
            today = datetime.now().date()
            time_parts = date_str.split(':')
            return datetime.combine(today, datetime.min.time().replace(
                hour=int(time_parts[0]), 
                minute=int(time_parts[1])
            ))
        elif '.' in date_str:
            # '09.16' 형식인 경우
            month, day = date_str.split('.')
            current_year = datetime.now().year
            return datetime(current_year, int(month), int(day))
        else:
            # 기본값
            return datetime.now()
    
    def run_migration(self, demo_data_file):
        """전체 마이그레이션 실행"""
        print("🚀 LawMate 데이터 마이그레이션 시작")
        
        # 더미 데이터 파일 읽기 (JavaScript 파일을 수동으로 JSON으로 변환 필요)
        # 실제로는 demoData.js를 파싱하거나 JSON 파일로 변환 후 사용
        
        # 예시 데이터 (실제로는 파일에서 읽어옴)
        demo_data = {
            'notices': [
                {
                    'category': '공지사항',
                    'title': '웹 사이트 점검 안내',
                    'content': '2025년 11월 6일 오후 3시~오후 6시 동안 웹 사이트 점검을 실시할 예정입니다.',
                    'date': '2025-11-06',
                    'views': 32,
                    'author': '관리자',
                    'fullContent': '상세 내용...'
                }
                # ... 더 많은 데이터
            ]
            # ... 다른 데이터 유형들
        }
        
        try:
            # 순서대로 마이그레이션 실행
            if 'notices' in demo_data:
                self.migrate_notices(demo_data['notices'])
            
            if 'users' in demo_data:
                self.migrate_users(demo_data['users'])
            
            if 'lawyer_users' in demo_data:
                self.migrate_lawyer_users(demo_data['lawyer_users'])
            
            if 'community_posts' in demo_data:
                self.migrate_community_posts(demo_data['community_posts'])
            
            if 'case_laws' in demo_data:
                self.migrate_case_laws(demo_data['case_laws'])
            
            if 'legal_dictionary' in demo_data:
                self.migrate_legal_dictionary(demo_data['legal_dictionary'])
            
            print("✅ 모든 데이터 마이그레이션 완료!")
            
        except Exception as e:
            print(f"❌ 마이그레이션 중 오류 발생: {e}")
            self.db.rollback()
            raise
        
        finally:
            self.cursor.close()
            self.db.close()

# 사용 예시
if __name__ == "__main__":
    # 데이터베이스 설정
    db_config = {
        'host': 'localhost',
        'user': 'lawmate_user',
        'password': 'your_password',
        'database': 'lawmate_db',
        'charset': 'utf8mb4'
    }
    
    # 마이그레이션 실행
    migrator = LawMateDataMigrator(db_config)
    migrator.run_migration('src/data/demoData.js')
```

---

## 📋 마이그레이션 체크리스트

### 준비 단계
- [ ] 데이터베이스 서버 설정 완료
- [ ] 개발/스테이징/프로덕션 환경 구분
- [ ] 백업 및 복구 계획 수립
- [ ] 마이그레이션 스크립트 준비

### 스키마 생성
- [ ] 모든 테이블 생성 완료
- [ ] 기본키 및 외래키 제약조건 설정
- [ ] 인덱스 생성 (기본 인덱스)
- [ ] 트리거 및 프로시저 설정 (필요시)

### 데이터 마이그레이션
- [ ] 사용자 데이터 (비밀번호 해시화 포함)
- [ ] 변호사 데이터 및 프로필
- [ ] 공지사항 데이터
- [ ] 커뮤니티 게시글 데이터
- [ ] 판례 데이터
- [ ] 법률 사전 데이터

### 성능 최적화
- [ ] Full-text 검색 인덱스 생성
- [ ] 복합 인덱스 생성
- [ ] 쿼리 성능 테스트
- [ ] 통계 정보 업데이트

### 검증 및 테스트
- [ ] 데이터 무결성 검증
- [ ] 검색 기능 테스트
- [ ] API 연동 테스트
- [ ] 성능 벤치마크 테스트
- [ ] 에러 처리 테스트

### 배포 준비
- [ ] 프로덕션 환경 설정
- [ ] 모니터링 도구 설정
- [ ] 로그 설정
- [ ] 백업 스케줄 설정
- [ ] 문서화 완료

---

## ⚠️ 주의사항

### 보안 고려사항
1. **비밀번호 처리**: 모든 비밀번호는 bcrypt로 해시화
2. **개인정보 보호**: 실제 개인정보 사용 금지, 더미 데이터만 사용
3. **SQL Injection 방지**: 파라미터 바인딩 사용
4. **접근 권한**: 데이터베이스 사용자 권한 최소화

### 데이터 품질 관리
1. **데이터 검증**: 필수 필드 누락 확인
2. **일관성 검사**: 외래키 관계 확인
3. **중복 제거**: 이메일, 닉네임 등 유니크 필드 검증
4. **인코딩**: UTF-8 인코딩 확인

### 성능 고려사항
1. **인덱스 전략**: 검색 패턴에 맞는 인덱스 설계
2. **Full-text 검색**: 한국어 검색 최적화
3. **쿼리 최적화**: 복잡한 JOIN 쿼리 성능 확인
4. **캐싱 전략**: Redis 캐시 활용 계획

### 롤백 계획
1. **백업**: 마이그레이션 전 전체 백업
2. **트랜잭션**: 롤백 가능한 단위로 마이그레이션
3. **검증**: 각 단계별 검증 후 진행
4. **복구**: 실패 시 즉시 복구 절차

---

## 📊 예상 데이터 볼륨

### 초기 데이터 (더미 데이터 기준)
- **공지사항**: 4건
- **커뮤니티 게시글**: 20건
- **변호사 프로필**: 6개
- **판례**: 6건 (1개 상세 판례 샘플)
- **법률 용어**: 15개 (4개 상세 정의 샘플)
- **사용자**: 2명 (일반 1명, 변호사 1명)

### 서비스 런칭 후 예상 볼륨 (1년 후)
- **사용자**: 10,000명
- **변호사**: 500명
- **커뮤니티 게시글**: 50,000건
- **상담**: 10,000건
- **판례**: 100,000건 (대법원 API 연동)
- **법률 용어**: 5,000개 (법제처 API 연동)

### 데이터베이스 크기 예상
- **초기**: 100MB 미만
- **1년 후**: 10GB 이상
- **3년 후**: 100GB 이상

---

## 🚀 배포 일정

### Week 1: 환경 구축
- **월요일**: 데이터베이스 서버 설정
- **화요일**: 스키마 생성 및 테스트
- **수요일**: 인덱스 설계 및 생성
- **목요일**: 마이그레이션 스크립트 개발
- **금요일**: 개발 환경 테스트

### Week 2: 데이터 마이그레이션
- **월요일**: 사용자 데이터 마이그레이션
- **화요일**: 콘텐츠 데이터 마이그레이션
- **수요일**: 법률 정보 데이터 마이그레이션
- **목요일**: 검증 및 성능 테스트
- **금요일**: 스테이징 환경 배포

### Week 3: 최종 검증 및 배포
- **월요일**: API 연동 테스트
- **화요일**: 성능 튜닝
- **수요일**: 보안 점검
- **목요일**: 프로덕션 배포 준비
- **금요일**: 프로덕션 배포 및 모니터링

---

## 📞 연락처 및 지원

### 기술 지원
- **데이터베이스 관리자**: db-admin@lawmate.com
- **백엔드 개발팀**: backend@lawmate.com
- **DevOps 팀**: devops@lawmate.com

### 문서 및 리소스
- **API 문서**: `/docs` (Swagger UI)
- **데이터베이스 스키마**: `DATABASE_SPECIFICATION.md`
- **프론트엔드 요구사항**: `FRONTEND_API_REQUEST.md`

### 모니터링 및 로그
- **애플리케이션 로그**: `/var/log/lawmate/`
- **데이터베이스 로그**: `/var/log/mysql/`
- **성능 모니터링**: Grafana Dashboard

---

**📅 최종 업데이트**: 2025년 10월 22일  
**📝 작성자**: 백엔드 개발팀  
**🔄 버전**: 1.0