from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AI Trading Research Agent FastAPI server started.")
    yield
    logger.info("AI Trading Research Agent FastAPI server shutting down.")

app = FastAPI(
    title="AI Trading Research Agent API",
    description="Production Multi-Agent Platform for Financial Equity Research & Analysis",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
