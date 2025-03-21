from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app
import json

def test_process_ocr_dummy():
    dummy_response = [{
        "name": ["John Doe"],
        "company": ["Example Inc."],
        "email": ["john@example.com"],
        "mobile_phone_number": ["010-1234-5678"],
        "etc": []
    }]

    with patch("app.service.ocr_service.call_openai", new=AsyncMock(return_value=json.dumps({"data": dummy_response}))):
        client = TestClient(app)
        payload = {
            "user_id": "test_user",
            "user_email": "test@example.com",
            "image_url": "https://dummy.image.url/card.jpg"
        }

        response = client.post("/api/process_ocr", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["result"][0]["name"][0] == "John Doe"