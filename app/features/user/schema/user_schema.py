"""
User Pydantic 스키마 정의

API 요청/응답에 사용되는 데이터 검증 스키마입니다.
"""

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """사용자 기본 스키마"""

    email: EmailStr = Field(..., max_length=255, description="사용자 이메일")
    name: str = Field(..., min_length=1, max_length=100, description="사용자 이름")
    age: int | None = Field(None, ge=0, le=150, description="나이 (0-150)")
    is_active: bool = Field(True, description="활성화 상태")


class UserCreate(UserBase):
    """사용자 생성 스키마"""

    pass


class UserUpdate(BaseModel):
    """사용자 수정 스키마 (부분 수정 지원)"""

    email: EmailStr | None = Field(None, max_length=255, description="사용자 이메일")
    name: str | None = Field(
        None, min_length=1, max_length=100, description="사용자 이름"
    )
    age: int | None = Field(None, ge=0, le=150, description="나이 (0-150)")
    is_active: bool | None = Field(None, description="활성화 상태")


class UserResponse(UserBase):
    """사용자 응답 스키마"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ORM 모델 → Pydantic 변환 허용
