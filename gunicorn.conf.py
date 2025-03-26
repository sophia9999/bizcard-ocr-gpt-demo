import multiprocessing
import logging
from app.core.config import settings
from logging.handlers import TimedRotatingFileHandler

workers = multiprocessing.cpu_count * 2 + 1
bind = f"{settings.UVICORN_HOST}:{settings.UVICORN_PORT}"
# gunicorn.conf.py
loglevel= "debug" if settings.DEBUG else "info"
logging_level = getattr(logging, loglevel.upper(), logging.INFO)
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
wsgi_app= "app.main:app"
log_dir = settings.LOG_DIR
error_log_file = f"{log_dir}/app.log"
access_log_file = f"{log_dir}/access.log"
accesslog = None
errorlog = None

# Gunicorn 프로세스 레벨의 로깅을 다룹니다.
# 여기서 설정하는 로그는 Gunicorn 프로세스 및 워커 관련 로그입니다.
# FastAPI의 세부 로깅은 `logger.py`에서 관리합니다.
def setup_logging():
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Gunicorn 에러 로그 파일 (자정마다 회전, 최대 31일 유지)
    error_handler = TimedRotatingFileHandler(error_log_file, when="midnight", interval=1, backupCount=31, encoding="utf-8")
    error_handler.setLevel(logging_level)
    error_handler.setFormatter(formatter)

    # Gunicorn 접근 로그 파일 (자정마다 회전, 최대 31일 유지)
    access_handler = TimedRotatingFileHandler(access_log_file, when="midnight", interval=1, backupCount=31, encoding="utf-8")
    access_handler.setFormatter(formatter)

    # 콘솔 핸들러 (터미널에 출력)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(formatter)

    # Gunicorn 에러 로거 설정 (파일 & 콘솔 출력)
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    gunicorn_error_logger.addHandler(error_handler)
    gunicorn_error_logger.addHandler(console_handler)  # 콘솔 출력 추가 local 확인용

setup_logging()