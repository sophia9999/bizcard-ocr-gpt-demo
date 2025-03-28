import requests
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from app.util.logger import logger

async def retrieve_image(image_url: str) -> Image.Image | None:
    try:
        logger.debug(f"이미지 다운로드 중: {image_url}")
        response = requests.get(image_url, timeout=5)
        response.raise_for_status()

        return Image.open(BytesIO(response.content))

    except Exception as e:
        logger.exception(f"이미지 다운로드 실패: {e}")
        return None

def divide_image_to_cards(image: Image.Image) -> list[Image.Image]:
    try:
        logger.debug("이미지에서 명함 추출 중...")
        # 이미지 이진화 -> 흑백전환, 블러, 오츠 이진화 -> 문서와 배경 구분
        img = np.array(image.convert("RGB"))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        extracted_docs = []
        doc_index = 1
        # 컨투어 추출 및 필터링 
        for cnt in contours:
            # 너무 작은 사각형은 제외
            area = cv2.contourArea(cnt)
            if area < 5000:
                    continue

            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # 꼭지점이 4개여야 사각형 모양이라고 판단. (사각형 모양 = 문서)
            if len(approx) == 4:
                warped = four_point_transform(img, approx)

                doc_index += 1
                extracted_docs.append(warped)

        return extracted_docs

    except Exception as e:
        logger.exception("명함 추출 실패")
        return []

def order_points(pts):
    pts = pts.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)
    rect[0] = pts[np.argmin(s)]      # top-left
    rect[2] = pts[np.argmax(s)]      # bottom-right
    rect[1] = pts[np.argmin(diff)]   # top-right
    rect[3] = pts[np.argmax(diff)]   # bottom-left
    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped