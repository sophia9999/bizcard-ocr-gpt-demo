# Bizcard OCR + GPT Demo

This project is a simplified and restructured version of a business card information extraction pipeline  
that I helped develop and maintain as part of a team project in my company.

To make the structure reusable and shareable, I rebuilt the core logic using mock data and public APIs.

## 🧑‍💻 Technology Stack

- **Backend Framework**: FastAPI
- **OCR**: Google Vision API
- **Text Classification**: OpenAI GPT (GPT-4o-mini)
- **Database**: None (For simplicity, no database used in this demo)
- **Testing**: pytest for unit testing
- **CI/CD**: Planned setup for deployment automation (GitHub Actions, Docker)
- **Environment Management**: venv for managing dependencies

## ⚙️ Features
- Simulated image processing & OCR flow with Google Vision API
- Prompt engineering for structured GPT responses (name, company, etc.)
- Modular FastAPI project layout with organized services and routes
- Logging, environment separation, and planned CI/CD setup
- Unit tests with `pytest` for critical functions

## Project Structure
```
📦bizcard-ocr-gpt-demo
 ┣ 📂app
 ┃ ┣ 📂api
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┗ 📜ocr.py
 ┃ ┣ 📂core
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┗ 📜config.py
 ┃ ┣ 📂service
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜gpt_service.py
 ┃ ┃ ┣ 📜image_service.py
 ┃ ┃ ┗ 📜ocr_service.py
 ┃ ┣ 📂util
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┗ 📜logger.py
 ┃ ┗ 📜main.py
 ┣ 📂secrets
 ┣ 📂tests
 ┃ ┣ 📜test_api.py
 ┃ ┣ 📜test_gpt_call.py
 ┃ ┗ 📜test_gpt_service.py
 ┣ 📜.env.example
 ┣ 📜.gitignore
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┗ 📜run_server.py
 ```

## 🛠 Installation & Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/bizcard-ocr-gpt-demo.git
    cd bizcard-ocr-gpt-demo
    ```

2. Create and activate a Python environment (`.venv`):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # MacOS/Linux
    # 또는
    .venv\Scripts\activate  # Windows
    ```

3. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the `.env` file with your API keys and credentials:
    ```env
    GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google-vision-key.json
    OPENAI_API_KEY=your-openai-api-key
    ```

5. Run the server:
    ```bash
    python run_server.py
    ```

6. Test the endpoints using `pytest`:
    ```bash
    PYTHONPATH=. pytest -v
    ```

## 🚀 API Endpoints

### POST `/api/process_ocr`

- **Description**: Processes a business card image URL, extracts the text, and returns the classified data.
- **Request Body**:
  ```json
  {
    "user_id": "test_user",
    "user_email": "test@example.com",
    "image_url": "https://dummy.image.url/card.jpg"
  }
- **Response Body**:
  ```json
    {
    "result": [
        {
        "card_idx": 1,
        "name": ["John Doe"],
        "company": ["Example Inc."],
        "phone_numbers": ["010-1234-5678"],
        ... # It depends on your prompt.
        ]
    }


## 🔐 Disclaimer
This repository does not include any proprietary code or data from the original project.  
All content is public, simulated, or self-developed for learning and demonstration purposes only.

## 🧪 For Testing
You can run unit tests using `pytest` to verify the core functionalities:
```bash
PYTHONPATH=. pytest -v
