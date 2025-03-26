from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.util.logger import logger
from pydantic import BaseModel, HttpUrl
import app.service.ocr_service as ocr_service
import app.service.image_service as image_service

router = APIRouter()

# 테스트
@router.get("/ping", tags=["OCR"])
async def ping():
    logger.info("📡 Received /ping request")
    logger.debug("📡 Received /ping request")
    return JSONResponse(content={"message": "pong"})


class OCRRequest(BaseModel):
    image_url: HttpUrl
    user_id: str
    user_email: str

@router.post("/process_ocr", tags=["OCR"])
async def process_ocr(payload: OCRRequest):
    logger.debug(f"Processing OCR for user: {payload.user_id}, image: {payload.image_url}")

    # 이미지 불러오기
    original_image = await image_service.retrieve_image(payload.image_url)
    if not original_image:
        raise HTTPException(status_code=400, detail="이미지 다운로드 실패")

    # 이미지 전처리
    extracted_cards = await image_service.divide_image_to_cards(original_image)
    if not extracted_cards:
        raise HTTPException(status_code=500, detail="카드 추출 실패")

    # google vision text 추출
    extracted_text = await ocr_service.call_google_vision_api(extracted_cards,)
    if not extracted_text:
        raise HTTPException(status_code=500, detail="텍스트 인식 실패")

    # gpt로 분류하기
    result = await ocr_service.classify_cards_with_gpt(extracted_text)

    return JSONResponse(content={"result": result})