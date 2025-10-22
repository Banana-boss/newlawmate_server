"""
User Repository

데이터베이스 CRUD 작업을 담당하는 Repository 계층입니다.
"""

from sqlalchemy.orm import Session
from app.features.user.entity import User
from app.features.user.schema import UserCreate, UserUpdate


class UserRepository:
    """사용자 데이터 접근 계층"""

    @staticmethod
    def create(db: Session, user_data: UserCreate) -> User:
        """
        사용자 생성

        Args:
            db: 데이터베이스 세션
            user_data: 사용자 생성 데이터

        Returns:
            생성된 User 엔티티
        """
        db_user = User(
            email=user_data.email.lower(),  # 이메일 소문자 정규화
            name=user_data.name,
            age=user_data.age,
            is_active=user_data.is_active,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        """
        ID로 사용자 조회

        Args:
            db: 데이터베이스 세션
            user_id: 사용자 ID

        Returns:
            User 엔티티 또는 None
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        """
        이메일로 사용자 조회

        Args:
            db: 데이터베이스 세션
            email: 사용자 이메일

        Returns:
            User 엔티티 또는 None
        """
        return db.query(User).filter(User.email == email.lower()).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """
        사용자 목록 조회

        Args:
            db: 데이터베이스 세션
            skip: 건너뛸 항목 수
            limit: 조회할 최대 항목 수

        Returns:
            User 엔티티 리스트
        """
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, user_id: int, user_data: UserUpdate) -> User | None:
        """
        사용자 정보 수정

        Args:
            db: 데이터베이스 세션
            user_id: 사용자 ID
            user_data: 수정할 데이터

        Returns:
            수정된 User 엔티티 또는 None
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None

        # 제공된 필드만 업데이트
        update_data = user_data.model_dump(exclude_unset=True)
        if "email" in update_data:
            update_data["email"] = update_data["email"].lower()  # 이메일 소문자 정규화

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """
        사용자 삭제

        Args:
            db: 데이터베이스 세션
            user_id: 사용자 ID

        Returns:
            삭제 성공 여부
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False

        db.delete(db_user)
        db.commit()
        return True
