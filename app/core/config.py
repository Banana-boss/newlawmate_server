"""
애플리케이션 설정 관리

환경 변수를 로드하고 애플리케이션 전역 설정을 관리합니다.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # Application
    APP_NAME: str = "FastAPI Server Template"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "lawmate_db"

    # Database URL
    DATABASE_URL: str = ""
    TEST_DATABASE_URL: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_database_url(self) -> str:
        """데이터베이스 URL 생성"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?client_encoding=utf8"

    def get_test_database_url(self) -> str:
        """테스트 데이터베이스 URL 생성"""
        if self.TEST_DATABASE_URL:
            return self.TEST_DATABASE_URL
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/test_{self.DB_NAME}?client_encoding=utf8"


@lru_cache()
def get_settings() -> Settings:
    """
    설정 객체 반환 (싱글톤 패턴)

    @lru_cache 데코레이터로 한 번만 생성되고 캐시됨
    """
    return Settings()
