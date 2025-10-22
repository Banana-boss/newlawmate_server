"""
User Router

사용자 관리 API 엔드포인트를 정의하는 Router 계층입니다.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.features.user.service import UserService
from app.features.user.schema import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/api/v1/users", tags=["users"])
user_service = UserService()


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="사용자 생성",
    description="새로운 사용자를 생성합니다. 이메일 중복 검증이 수행됩니다.",
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    사용자 생성 API

    - **email**: 사용자 이메일 (중복 불가)
    - **name**: 사용자 이름
    - **age**: 나이 (선택, 0-150)
    - **is_active**: 활성화 상태 (기본값: true)
    """
    return user_service.create_user(db, user_data)


@router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="사용자 목록 조회",
    description="등록된 사용자 목록을 조회합니다. 페이지네이션을 지원합니다.",
)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    사용자 목록 조회 API

    - **skip**: 건너뛸 항목 수 (기본값: 0)
    - **limit**: 조회할 최대 항목 수 (기본값: 100)
    """
    return user_service.get_all_users(db, skip, limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="사용자 단건 조회",
    description="특정 사용자의 정보를 조회합니다.",
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    사용자 단건 조회 API

    - **user_id**: 사용자 ID
    """
    return user_service.get_user_by_id(db, user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="사용자 정보 수정",
    description="사용자 정보를 수정합니다. 제공된 필드만 업데이트됩니다.",
)
def update_user(
    user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)
):
    """
    사용자 정보 수정 API

    - **user_id**: 사용자 ID
    - **email**: 사용자 이메일 (선택)
    - **name**: 사용자 이름 (선택)
    - **age**: 나이 (선택)
    - **is_active**: 활성화 상태 (선택)
    """
    return user_service.update_user(db, user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="사용자 삭제",
    description="사용자를 삭제합니다.",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    사용자 삭제 API

    - **user_id**: 사용자 ID
    """
    user_service.delete_user(db, user_id)
