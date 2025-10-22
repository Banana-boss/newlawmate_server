"""
FastAPI 애플리케이션 진입점

서버 시작 시 실행되는 메인 파일입니다.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import get_settings
from app.core.init_db import init_database
from app.features.user.router import router as user_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 수명 주기 관리

    서버 시작 시 데이터베이스 초기화를 수행합니다.
    """
    # Startup
    print("🚀 Starting FastAPI server...")
    init_database()
    print(f"✅ Server started: {settings.APP_NAME} v{settings.APP_VERSION}")
    yield
    # Shutdown
    print("👋 Shutting down server...")


# FastAPI 앱 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="3-tier 아키텍처 기반의 FastAPI 서버 템플릿",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 환경에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(user_router)


@app.get("/", tags=["health"])
def health_check():
    """
    헬스 체크 엔드포인트

    서버 상태를 확인합니다.
    """
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/health", tags=["health"])
def health():
    """
    헬스 체크 엔드포인트 (별칭)

    서버 상태를 확인합니다.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
