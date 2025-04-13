from openai import AsyncOpenAI
import json
from app.core.config import settings
from app.util.logger import logger
import time

client_openai = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY
)

def build_messages(cards: list) -> list:
    messages = [
        {
            "role": "system",
            "content": settings.SYSTEM_PROMPT
        }
    ]

    # user message에 카드 번호별로 텍스트 구분해서 넣기
    user_message = ""
    for idx, card in enumerate(cards):
        user_message += f"data {idx + 1}:\n{card['detected_texts']}\n\n"

    messages.append({
        "role": "user",
        "content": user_message.strip()
    })

    return messages

async def call_openai(messages: list) -> str:
    logger.debug("GPT 호출 시작")
    start = time.monotonic()

    response = await client_openai.chat.completions.create(
        model=settings.GPT_MODEL,
        messages=messages,
        temperature=0.1,
        max_tokens=3000,
        response_format={
            "type": "json_object"
        }
    )

    elapsed = time.monotonic() - start
    logger.debug(f"GPT 호출 완료 (소요 시간: {elapsed:.2f}초)")
    
    return response.choices[0].message.content

def parse_gpt_response(content: str, expected_len: int) -> list:
    try :
        parsed = json.loads(content)

        # 1개일 때와 배열일 때 다르게 옴
        if  "data" in parsed and isinstance(parsed["data"], list):
            if len(parsed["data"]) == expected_len:
                return parsed["data"]
            else:
                raise ValueError(f"Mismatch: expected {expected_len} results, got {len(parsed['data'])}")
        elif isinstance(parsed, dict) and expected_len == 1:
            return [parsed]
        else:
            raise ValueError(f"Invalid GPT response format: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError(f"GPT 응답이 JSON이 아님: {str(e)}")
    except Exception as e:
        raise ValueError(f"GPT 응답 파싱 실패: {str(e)}")