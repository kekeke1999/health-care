from fastapi import FastAPI
from api.v1.endpoints import user, health
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Diabetes Management API")

# add routers
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)