import multiprocessing
import logging
from app.core.config import settings

workers = multiprocessing.cpu_count() * 2 + 1
bind = f"{settings.UVICORN_HOST}:{settings.UVICORN_PORT}"
loglevel= "debug" if settings.DEBUG else "info"
worker_class = "uvicorn.workers.UvicornWorker"
wsgi_app= "app.main:app"
log_dir = settings.LOG_DIR
accesslog = "-"
errorlog = "-"