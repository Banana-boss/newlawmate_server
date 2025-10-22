"""
데이터베이스 연결 및 세션 관리

SQLAlchemy를 사용한 데이터베이스 연결 설정 및 세션 관리를 담당합니다.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

# 데이터베이스 엔진 생성
engine = create_engine(
    settings.get_database_url(),
    pool_pre_ping=True,  # 연결 상태 확인
    pool_recycle=3600,  # 1시간마다 연결 재생성
    echo=settings.DEBUG,  # DEBUG 모드에서 SQL 로그 출력
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성 (모든 ORM 모델의 부모 클래스)
Base = declarative_base()


def get_db():
    """
    데이터베이스 세션 의존성

    FastAPI의 Depends()와 함께 사용됩니다.
    요청마다 새로운 세션을 생성하고, 요청 종료 시 자동으로 닫습니다.

    Yields:
        Session: 데이터베이스 세션
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
