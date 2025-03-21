import logging
from logging.handlers import TimedRotatingFileHandler
import os
from app.core.config import settings

# 로그 디렉토리 확인 및 생성
log_dir = settings.LOG_DIR
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "app.log")
access_log_file = os.path.join(log_dir, "access.log")

def setup_logger():
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 애플리케이션 로그 설정 (uvicorn.error와 동일하게)
    app_logger = logging.getLogger("uvicorn.error")
    app_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=14, encoding="utf-8")
    app_handler.setFormatter(formatter)
    app_handler.setLevel(log_level)
    app_logger.handlers.clear() # gunicorn 사용 시 기존핸들러에 추가되기 때문에, 초기화 후 넣어준다.
    app_logger.addHandler(app_handler)
    app_logger.setLevel(log_level)

    # 접근 로그 설정 (클라이언트 요청 기록)
    access_logger = logging.getLogger("uvicorn.access")
    access_handler = TimedRotatingFileHandler(access_log_file, when="midnight", interval=1, backupCount=14, encoding="utf-8")
    access_handler.setFormatter(formatter)
    access_handler.setLevel(log_level)
    access_logger.handlers.clear()
    access_logger.addHandler(access_handler)
    access_logger.setLevel(log_level)

    return app_logger, access_logger

logger, access_logger = setup_logger()