from app.service.gpt_service import build_messages, call_openai, parse_gpt_response
from app.util.logger import logger
from google.cloud import vision
import cv2
import numpy as np

# 전역 클라이언트 생성
vision_client = vision.ImageAnnotatorClient()

def call_google_vision_api(extracted_cards: list[np.ndarray]) -> list[str]:
    '''
    return [extracted texts,...]
    '''
    result_texts = []

    try:
        logger.debug(f"Google Vision API로 명함 이미지들 전달 중...")
        
        # 추출된 개수만큼의 카드별 array로 변환
        for idx, cv_image in enumerate(extracted_cards):
            # OpenCV -> jpeg byte encoding
            _, buffer = cv2.imencode(".jpg", cv_image)
            content = buffer.tobytes()

            vision_image = vision.Image(content=content)
            response = vision_client.text_detection(image=vision_image)

            texts = response.text_annotations
            if texts:
                full_text = texts[0].description.strip()
                full_text = full_text.replace("\n", " ")
                logger.debug(f"card {idx+1} 텍스트: {full_text}")
                result_texts.append({
                    "detected_texts" : full_text
                })
            else:
                result_texts.append("")

    except Exception as e:
        logger.exception("Vision API 호출 실패")

    return result_texts
    

async def classify_cards_with_gpt(cards: list) -> list:
    """
    return: List of structured GPT classification result with card index
    """
    result = []

    try:
        messages = build_messages(cards)
        gpt_response_str = await call_openai(messages)
        parsed_data_list = parse_gpt_response(gpt_response_str, expected_len=len(cards))

        for i, parsed in enumerate(parsed_data_list):
            card = cards[i]
            result.append({
                "card_idx": i + 1,
                **parsed 
            })

    except Exception as e:
        logger.exception("Failed to classify cards with GPT")
    
    return result
