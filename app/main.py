from fastapi import FastAPI

from app.models import User
from app.routers import category, products, auth, permission, review
from sqladmin import Admin, ModelView
from app.baskend.db import engine

app = FastAPI()
admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.first_name]


@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(permission.router)
app.include_router(review.router)


admin.add_view(UserAdmin)
