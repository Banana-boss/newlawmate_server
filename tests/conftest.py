"""
pytest 설정 및 공통 fixture 정의
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base
from app.core.dependencies import get_db
from app.core.config import get_settings

# 테스트 설정
settings = get_settings()

# 테스트 데이터베이스 엔진 생성
TEST_DATABASE_URL = settings.get_test_database_url()
test_engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db():
    """
    테스트용 데이터베이스 세션 fixture

    각 테스트마다 새로운 데이터베이스 세션을 생성하고,
    테스트 종료 시 롤백하여 데이터를 초기화합니다.
    """
    # 테이블 생성
    Base.metadata.create_all(bind=test_engine)

    # 세션 생성
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.rollback()
        db.close()
        # 테이블 삭제 (격리된 테스트 환경)
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db):
    """
    테스트용 FastAPI 클라이언트 fixture

    테스트용 데이터베이스를 사용하도록 의존성을 오버라이드합니다.
    """

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
