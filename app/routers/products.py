from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from slugify import slugify
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.baskend.db_depends import get_db
from app.models import *
from app.shemas import CreateProduct
from .auth import get_current_user

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def all_products(db: Annotated[AsyncSession, Depends(get_db)],
                       get_user: Annotated[User, Depends(get_current_user)]):
    products = await db.scalars(select(Product).where(Product.is_active == True, Product.stock > 0))
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="products not found")
    return products.all()


@router.post('/create')
async def create_product(db: Annotated[AsyncSession, Depends(get_db)], create_product: CreateProduct,
                         get_user: Annotated[User, Depends(get_current_user)]):
    if get_user.get('is_admin') or get_user.get('is_supplier'):
        await db.execute(insert(Product).values(name=create_product.name,
                                                description=create_product.description,
                                                price=create_product.price,
                                                image_url=create_product.image_url,
                                                stock=create_product.stock,
                                                category_id=create_product.category,
                                                slug=slugify(create_product.name),
                                                rating=0.0
                                                ))

        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'success'
        }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have admin permission or supplier")


@router.get('/{category_slug}')
async def product_by_category(category_slug: str, db: Annotated[AsyncSession, Depends(get_db)],
                              get_user: Annotated[User, Depends(get_current_user)]):
    category = await db.scalar(select(Category).where(Category.slug == category_slug))
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")

    subcategory = await db.scalars(select(Category).where(Category.id == category.parent_id))
    cat_and_sub = [i.id for i in subcategory.all()] + [category.id]
    products_in_category = await db.scalars(select(Product).where(Product.is_active == True,
                                                                  Product.stock > 0,
                                                                  Product.category_id.in_(cat_and_sub)))
    return products_in_category.all()


@router.get('/detail/{product_slug}')
async def product_detail(product_slug: str, db: Annotated[AsyncSession, Depends(get_db)]):
    product = await db.scalar(select(Product).where(Product.slug == product_slug,
                                                    Product.is_active == True,
                                                    Product.stock > 0))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    return product


@router.put('/detail/{product_slug}')
async def update_product(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str,
                         update_product_model: CreateProduct, get_user: Annotated[User, Depends(get_current_user)]):
    product = await db.scalar(select(Product).where(Product.slug == product_slug))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    if get_user.get('is_supplier') or get_user.get('is_admin'):
        if get_user.get('id') == product.supplier_id or get_user.get('is_admin'):
            await db.execute(update(Product).where(Product.slug == product_slug).values(name=update_product_model.name,
                                                                                        description=update_product_model.description,
                                                                                        price=update_product_model.price,
                                                                                        image_url=update_product_model.image_url,
                                                                                        stock=update_product_model.stock,
                                                                                        category_id=update_product_model.category,
                                                                                        slug=slugify(update_product_model.name)
                                                                                        ))
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'success'
            }
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to use this method')
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have admin permission or supplier")

@router.delete('/delete')
async def delete_product(db: Annotated[AsyncSession, Depends(get_db)], product_id: int,
                         get_user: Annotated[User, Depends(get_current_user)]):
    product_delete = await db.scalar(select(Product).where(Product.id == product_id))
    if product_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )
    if get_user.get('is_supplier') or get_user.get('is_admin'):
        if get_user.get('id') == product_delete.supplier_id or get_user.get('is_admin'):
            await db.execute(update(Product).where(Product.id == product_id).values(is_active=False))
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'Product delete is successful'
            }
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to use this method')
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have admin permission or supplier")
