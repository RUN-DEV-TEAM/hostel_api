from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from db.connection import init_db
from api.endpoints import admin_endpoint, auth_endpoint



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
 
app = FastAPI(lifespan=lifespan,description="RUN HOSTEL MANAGEMENT BACKEND APP") 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_endpoint.router,prefix="/api/admin", tags=["admin"])

app.include_router(auth_endpoint.router,prefix="/api/user", tags=["auth"])
