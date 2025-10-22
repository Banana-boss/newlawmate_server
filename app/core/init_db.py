"""
데이터베이스 초기화

서버 시작 시 데이터베이스 테이블을 생성하고 초기 데이터를 설정합니다.
"""

from sqlalchemy import text
from app.core.database import engine, Base, SessionLocal
from app.core.config import get_settings

# 모든 엔티티 import (Base.metadata에 등록하기 위함)
from app.features.user.entity import User  # noqa: F401

settings = get_settings()


def init_database():
    """
    데이터베이스 초기화

    1. 데이터베이스 연결 확인
    2. 테이블 생성 (존재하지 않는 경우)
    3. 초기 데이터 설정 (필요시)
    """
    print("🔄 Initializing database...")

    try:
        # 데이터베이스 연결 확인
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")

        # 테이블 생성
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created")

        # 초기 데이터 설정 (필요시)
        # _create_initial_data()

        print("✅ Database initialization complete")

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise


def _create_initial_data():
    """
    초기 데이터 생성

    개발/테스트 환경에서 필요한 초기 데이터를 생성합니다.
    운영 환경에서는 호출하지 않습니다.
    """
    db = SessionLocal()
    try:
        # 예시: 초기 사용자 생성
        # from app.features.user.repository import UserRepository
        # from app.features.user.schema import UserCreate
        #
        # existing_user = UserRepository.get_by_email(db, "admin@example.com")
        # if not existing_user:
        #     admin_user = UserCreate(
        #         email="admin@example.com",
        #         name="Admin User",
        #         age=30,
        #         is_active=True
        #     )
        #     UserRepository.create(db, admin_user)
        #     print("✅ Initial admin user created")

        pass

    except Exception as e:
        print(f"❌ Initial data creation failed: {e}")
        db.rollback()
    finally:
        db.close()


def drop_all_tables():
    """
    모든 테이블 삭제

    주의: 테스트 환경에서만 사용해야 합니다!
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All tables dropped")
