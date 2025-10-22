# FastAPI Server Template

3-tier 아키텍처 기반의 FastAPI 서버 템플릿입니다.

## 📋 주요 특징

- **3-tier 아키텍처**: Router → Service → Repository 계층 분리
- **기능 단위 모듈화**: 각 기능별로 독립적인 폴더 구조
- **문서 기반 개발**: 요청 문서 → 설계 → 코드 → 테스트 워크플로우
- **자동 테스트**: 엔드포인트별 테스트 코드 필수
- **Docker 배포**: docker-compose 기반 MySQL + FastAPI 구성
- **자동 DB 초기화**: 서버 시작 시 엔티티 및 DB 자동 세팅

## 🏗️ 프로젝트 구조

```
server_templete/
├── app/
│   ├── core/                    # 핵심 인프라
│   │   ├── config.py           # 설정 관리
│   │   ├── database.py         # DB 연결 및 세션
│   │   ├── dependencies.py     # 의존성 주입
│   │   └── init_db.py          # DB 초기화
│   ├── features/               # 기능 단위 모듈
│   │   └── user/              # User 기능 예시
│   │       ├── entity/        # 엔티티 (ORM 모델)
│   │       ├── repository/    # 데이터 접근 계층
│   │       ├── service/       # 비즈니스 로직 계층
│   │       ├── router/        # API 엔드포인트 계층
│   │       └── schema/        # Pydantic 스키마
│   └── main.py                # FastAPI 앱 진입점
├── tests/                      # 테스트 코드
│   ├── conftest.py
│   └── features/
│       └── user/
├── docs/                       # 문서
│   ├── 00_template/           # 문서 템플릿
│   ├── example/               # 예시 문서
│   ├── workflow_guide.md      # 개발 워크플로우 가이드
│   └── architecture.md        # 아키텍처 설명
├── docker-compose.yml
├── Dockerfile
├── deploy.sh                   # 배포 스크립트
├── requirements.txt
└── DEVELOPMENT_RULES.md        # 개발 필수 규칙

```

## 🚀 시작하기

### 1. 환경 설정

```bash
# .env 파일 생성
cp .env.example .env

# 필요시 .env 파일 수정
```

### 2. Docker로 실행

```bash
# 빌드 및 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### 3. 로컬 개발 환경

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload
```

## 🧪 테스트

```bash
# 모든 테스트 실행
pytest

# 커버리지 포함
pytest --cov=app tests/

# 특정 테스트만 실행
pytest tests/features/user/
```

## 📦 배포

```bash
# 테스트 통과 후 자동 배포
./deploy.sh
```

배포 스크립트는 다음 순서로 동작합니다:
1. 테스트 실행
2. 테스트 통과 확인
3. Docker 이미지 빌드
4. 컨테이너 재시작

## 📖 문서

- [개발 워크플로우 가이드](docs/workflow_guide.md)
- [아키텍처 설명](docs/architecture.md)
- [개발 필수 규칙](DEVELOPMENT_RULES.md)

## 🔧 새 기능 추가 방법

1. `docs/00_template/request_template.md`를 복사하여 요청 문서 작성
2. 설계, 엔드포인트, 엔티티 문서 작성
3. 문서 기반으로 코드 구현
4. 테스트 코드 작성
5. 모든 테스트 통과 확인

자세한 내용은 [DEVELOPMENT_RULES.md](DEVELOPMENT_RULES.md)를 참고하세요.

## 📝 API 문서

서버 실행 후 다음 URL에서 API 문서 확인:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ 기술 스택

- **Framework**: FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Testing**: pytest
- **Deployment**: Docker, Docker Compose
