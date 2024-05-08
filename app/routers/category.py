from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.baskend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert, select, update
from app.shemas import CreateCategory
from .auth import get_current_user

from slugify import slugify

router = APIRouter(
    prefix="/category",
    tags=["category"],
    responses={404: {"description": "Not found"}},
)


@router.get("/all_categories")
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db)]):
    categories = await db.scalars(select(Category).where(Category.is_active == True))
    return categories.all()


@router.post("/create")
async def create_category(db: Annotated[AsyncSession, Depends(get_db)], create_category: CreateCategory,
                          get_user: Annotated[User, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        await db.execute(insert(Category).values(name=create_category.name,
                                                 parent_id=create_category.parent_id,
                                                 slug=slugify(create_category.name)))
        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'success'
        }

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have admin permission")


@router.put("/update_category")
async def update_category(db: Annotated[AsyncSession, Depends(get_db)], category_id: int,
                          update_category: CreateCategory,get_user: Annotated[User, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        category = await db.scalar(select(Category).where(Category.id == category_id))
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")
        await db.execute(update(Category).where(Category.id == category_id).values(name=update_category.name,
                                                                                   parent_id=update_category.parent_id,
                                                                                   slug=slugify(update_category.name)))
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'success'
        }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have admin permission")


@router.delete("/delete")
async def delete_category(db: Annotated[AsyncSession, Depends(get_db)], category_id: int, get_user: Annotated[User, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        category = await db.scalar(select(Category).where(Category.id == category_id))
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")
        await db.execute(update(Category).where(Category.id == category_id).values(is_active=False))
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'success'
        }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have admin permission")
