from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from .auth import get_current_user
from app.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.baskend.db_depends import get_db

router = APIRouter(
    prefix='/permissions',
    tags=['permissions'],
    responses={404: {'description': 'Not found'}}
)


@router.patch('/')
async def update_permission(get_user: Annotated[User, Depends(get_current_user)], db: Annotated[AsyncSession,
                            Depends(get_db)], user_id: int):

    if get_user.get('is_admin'):
        user = await db.scalar(select(User).where(User.id == user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user.is_supplier:
            await db.execute(update(User).where(User.id == user_id).values(is_supplier=False, is_customer=True))
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'detail': 'User is no longer supplier'
            }

        else:
            await db.execute(update(User).where(User.id == user_id).values(is_supplier=True, is_customer=False))
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'detail': 'User is now supplier'
            }

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have admin permission")


@router.delete('/delete')
async def delete_user(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)], user_id: int):
    if get_user.get('is_admin'):
        user = await db.scalar(select(User).where(User.id == user_id))

        if user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You can't delete admin user"
            )

        if user.is_active:
            await db.execute(update(User).where(User.id == user_id).values(is_active=False))
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'detail': 'User is deleted'
            }
        else:
            await db.execute(update(User).where(User.id == user_id).values(is_active=True))
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'detail': 'User is activated'
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have admin permission"
        )

