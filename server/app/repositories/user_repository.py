from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.user import User


# 🔍 Get user by email
async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


# 🔍 Get user by ID
async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


# ➕ Create user
async def create_user(
    db: AsyncSession,
    email: str,
    hashed_password: str
) -> User:
    new_user = User(
        email=email,
        password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


# 📄 Get all users
async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()


# ✏️ Update user
async def update_user(
    db: AsyncSession,
    user_id: int,
    email: str | None = None,
    password: str | None = None
) -> User | None:
    user = await get_user_by_id(db, user_id)

    if not user:
        return None

    if email:
        user.email = email
    if password:
        user.password = password

    await db.commit()
    await db.refresh(user)

    return user


# ❌ Delete user
async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(db, user_id)

    if not user:
        return False

    await db.delete(user)
    await db.commit()

    return True