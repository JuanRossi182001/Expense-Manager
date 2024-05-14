from fastapi import FastAPI
from routers import userRouter, typeSpentRouter,spentRouter
from model import user, spent, typeSpent
from config.config import engine

app = FastAPI()

app.include_router(userRouter.router)
app.include_router(typeSpentRouter.router)
app.include_router(spentRouter.router)

user.base.metadata.create_all(bind=engine)
spent.base.metadata.create_all(bind=engine)
typeSpent.base.metadata.create_all(bind=engine)