from celery_app import celery
import os, smtplib
from email.mime.text import MIMEText
import logging
from datetime import datetime

logging.basicConfig(filename="app.log", level=logging.INFO)

@celery.task(name="send_email_task")
def send_email(recipient):
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    msg = MIMEText("Hello, this is a test from Celery!")
    msg["Subject"] = "Celery Test"
    msg["From"] = smtp_user
    msg["To"] = recipient

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

    logging.info(f"✅ Email sent to {recipient} at {datetime.utcnow()}")
    return f"Email sent to {recipient}"
