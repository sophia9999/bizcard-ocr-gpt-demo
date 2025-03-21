import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    print(f"Starting FastAPI in {settings.ENV} mode (DEBUG={settings.DEBUG})...")
    uvicorn.run(
        "app.main:app",  # FastAPI 엔트리 포인트
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=settings.UVICORN_RELOAD
    )