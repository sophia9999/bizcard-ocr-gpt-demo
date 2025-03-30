import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from app.core.config import settings
import multiprocessing

log_dir = settings.LOG_DIR
os.makedirs(log_dir, exist_ok=True)

worker_pid = str(multiprocessing.current_process().pid)
log_file = os.path.join(log_dir, f"app_{worker_pid}.log")
access_log_file = os.path.join(log_dir, f"access_{worker_pid}.log")

def setup_logging():
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    # 포맷터 정의
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(module)s] [PID:%(process)d] : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 루트 로거 초기화 (핸들러 중복 방지)
    logging.getLogger().handlers.clear()

    file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=14, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    access_handler = TimedRotatingFileHandler(access_log_file, when="midnight", interval=1, backupCount=14, encoding="utf-8")
    access_handler.setFormatter(formatter)
    access_handler.setLevel(log_level)

    # 콘솔 - 개발 시에는 terminal에서 확인을 위해 주석해제하십시오.
    # console_handler = logging.StreamHandler(sys.stdout)
    # console_handler.setFormatter(formatter)
    # console_handler.setLevel(log_level)

    # uvicorn.error 
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.addHandler(file_handler)
    uvicorn_error_logger.setLevel(log_level)
    uvicorn_error_logger.propagate = False

    # uvicorn.access 로컬테스트 시 안봐도되는 로그이긴 합니다. (운영에선 추적 시 필수임)
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.addHandler(access_handler)
    uvicorn_access_logger.setLevel(log_level)
    uvicorn_access_logger.propagate = False

    # gunicorn.error --> gunicorn으로 실행 시
    if "gunicorn" in sys.argv[0]:
        gunicorn_logger = logging.getLogger("gunicorn.error")
        gunicorn_logger.addHandler(file_handler)
        gunicorn_logger.setLevel(log_level)

        gunicorn_logger = logging.getLogger("gunicorn.access")
        gunicorn_logger.addHandler(access_handler)
        gunicorn_logger.setLevel(log_level)

    return uvicorn_error_logger, uvicorn_access_logger

logger, uvicorn_access_logger = setup_logging()
