import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.service.gpt_service import call_openai, parse_gpt_response
from app.core.config import settings

@pytest.mark.asyncio
async def test_call_openai_with_mock():
    fake_messages = [
        {"role": "system", "content": settings.SYSTEM_PROMPT},
        {"role": "user", "content": "data 1: Alice\n\ndata 2: Bob"}
    ]

    fake_json_response = {
        "data": [
            {"name": ["Alice"], "company": ["Company A"], "email": [], "etc": []},
            {"name": ["Bob"], "company": ["Company B"], "email": [], "etc": []}
        ]
    }

    # 응답을 mock 객체로 구성
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=fake_json_response))]

    with patch("app.service.gpt_service.client_openai.chat.completions.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_response

        result = await call_openai(fake_messages)

        assert result["data"][0]["name"][0] == "Alice"
        assert result["data"][1]["name"][0] == "Bob"
        assert len(result["data"]) == 2
