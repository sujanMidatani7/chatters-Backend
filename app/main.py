from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from starlette.middleware.cors import CORSMiddleware
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"]
)




app.include_router(user_router, prefix="/user" ,tags=["user_routes"])

