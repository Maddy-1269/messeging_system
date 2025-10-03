from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    "messaging_system",
    broker=os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "rpc://"),
)

# 👇 this ensures Celery loads all tasks
import tasks
