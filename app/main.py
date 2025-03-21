from fastapi import FastAPI
from app.core.config import settings
from app.util.logger import logger
from app.api import ocr

app = FastAPI(title="Bizcard OCR GPT Demo")

logger.info(f"✅ FastAPI app started in {settings.ENV} mode")
logger.debug(f"✅ FastAPI app started in {settings.ENV} mode")

app.include_router(ocr.router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ok"}