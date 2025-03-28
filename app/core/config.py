from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
import tempfile

# below codes are executed before reading .env.* files,
# if you want to set this ENV, I recommand below code use. 
# example: ENV=dev python run_server.py
ENV = os.getenv("ENV", "local")
ENV_FILE = f".env.{ENV}"

if os.path.exists(ENV_FILE):
    print(f"Loading environment file: {ENV_FILE}")
    # 서버 세팅 시 error 사항 때문에 추가 
    # .env에서 불러온 변수는 os.getenv()에서만 사용할 수 있고 os.environ에는 자동 반영되지 않으므로 내부에서 환경 변수 등록 시 에로 사항이 있어 등록을 위함
    load_dotenv(ENV_FILE, override=True)
else:
    print(f"Warning: `{ENV_FILE}` file not found. Using default settings.")

class Settings(BaseSettings):
    ENV: str = "dev"
    OPENAI_API_KEY: str
    LOG_DIR: str = "./logs"
    
    UVICORN_HOST: str = "127.0.0.1"
    UVICORN_PORT: int = 8080
    UVICORN_RELOAD: bool 
    DEBUG: bool = ENV != "prod"
    GPT_MODEL: str = "gpt-4o-mini" 
    SYSTEM_PROMPT: str = """
    You are a helpful assistant that classifies business card text into structured JSON.
    Only use the given text. If any field is missing, return it as an empty list.
    Do not make up any data. If there isn't suitable category, Just give me a empty array.
    """
    # Google Cloud SDK는 OS환경변수로 os.environ에서 값을 찾으므로 os.environ에 등록해줘야합니다.
    GOOGLE_APPLICATION_CREDENTIALS: str = "your-google-key"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.GOOGLE_APPLICATION_CREDENTIALS:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set.")
    
        if not self.LOG_DIR:
            self.LOG_DIR = tempfile.mkdtemp(prefix="demo_log")

# 인스턴스화
settings = Settings()