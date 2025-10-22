"""
공통 의존성 정의

FastAPI의 Depends()와 함께 사용되는 의존성들을 정의합니다.
"""

from sqlalchemy.orm import Session
from app.core.database import get_db

# 데이터베이스 세션 의존성 (재export)
__all__ = ["get_db"]
