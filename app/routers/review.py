from app.routers.auth import get_current_user
from app.shemas import CreateReview
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.baskend.db_depends import get_db

from app.models import *

router = APIRouter(prefix='/reviews', tags=['reviews'])


@router.get('/all_reviews')
async def all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.is_active == True))
    if not reviews:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="reviews not found")
    return reviews.all()


@router.post('/create')
async def create_review(create_review: CreateReview, db: Annotated[AsyncSession, Depends(get_db)],
                        get_user: Annotated[User, Depends(get_current_user)]):
    if get_user.get('is_customer'):
        await db.execute(insert(Review).values(comment=create_review.comment,
                                               comment_date=create_review.comment_date,
                                               rating=create_review.rating,
                                               product_id=create_review.product_id,
                                               user_id=get_user.get('id')
                                               ))

        average_rating = await db.scalars(select(Review.rating).where(Review.product_id == create_review.product_id))
        rating_count = average_rating.all()
        rating_result = sum(rating_count) / len(rating_count)
        await db.execute(update(Product).where(Product.id == create_review.product_id).values(rating=rating_result))

        await db.commit()

        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'success'}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have customer permission")


@router.get('/products_reviews/{product_id}')
async def products_reviews(product_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.product_id == product_id, Review.is_active == True))
    if not reviews:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="reviews not found")
    return reviews.all()


@router.delete('/delete/{review_id}')
async def delete_review(review_id: int, db: Annotated[AsyncSession, Depends(get_db)],
                        get_user: Annotated[User, Depends(get_current_user)]):
    review_delete = await db.scalar(select(Review).where(Review.id == review_id))
    if review_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no review found'
        )

    if get_user.get('is_admin'):
        await db.execute(update(Review).where(Review.id == review_id).values(is_active=False))
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Review delete is successful'
        }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have admin permission")
