from celery import Celery
from src.mail import mail, create_message
from asgiref.sync import async_to_sync
from src.config import Config

# Initialize Celery with Redis Cloud as the broker and result backend
c_app = Celery(
    "tasks",
    broker=Config.REDIS_URL,  # Use Redis Cloud as the broker
    backend=Config.REDIS_URL,  # Use Redis Cloud as the result backend
)

def send_email(recipients: list[str], subject: str, html_message: str) -> None:
    message = create_message(
        recipients=recipients, subject=subject, body=html_message
    )
    # Using async_to_sync to call the async send_message method
    async_to_sync(mail.send_message)(message)
    print(f"Email sent to {recipients} with subject '{subject}'", flush=True)