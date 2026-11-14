from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, clients, projects

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Gestion'aire API",
    description="A business operations API for independent professionals and small teams.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(clients.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")

@app.get("/health", tags=["Operations"])
def health():
    return {"status": "ok", "service": "gestion-aire-api", "version": app.version}
