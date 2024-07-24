from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from db.connection import init_db
from api.endpoints import auth_endpoints, ug_admin_endpoints, ug_endpoints,dest_admin_endpoints,dest_endpoints,pg_admin_endpoints,pg_endpoints


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

app.include_router(auth_endpoints.router,prefix="/api/user", tags=["auth"])

app.include_router(ug_admin_endpoints.router,prefix="/api/ug/admin", tags=["Undergraduate Admin"])

app.include_router(ug_endpoints.router,prefix="/api/ug/student", tags=["Undergraduate Student"])

app.include_router(dest_admin_endpoints.router,prefix="/api/dest/admin", tags=["Dest Admin"])

app.include_router(dest_endpoints.router,prefix="/api/dest/student", tags=["Dest Student"])

app.include_router(pg_admin_endpoints.router,prefix="/api/pg/admin", tags=["Postgraduate Admin"])

app.include_router(pg_endpoints.router,prefix="/api/pg/student", tags=["Postgraduate Student"])