Messaging System with RabbitMQ, Celery, Nginx, and Python
Overview

This project demonstrates a simple messaging system with asynchronous task processing using RabbitMQ (message broker) and Celery (task queue).
The system provides two main functionalities:

Asynchronous Email Sending → ?sendmail=<recipient_email>

Logging Current Time → ?talktome

The Python application (Flask/FastAPI) is served with Gunicorn/Uvicorn behind Nginx, and is externally exposed using ngrok for public testing.

Objective

Showcase asynchronous task processing with Celery & RabbitMQ.

Serve a Python web app behind Nginx for production-like behavior.

Provide endpoints to test both email sending and server logging.

Expose the local setup using ngrok for external validation.

System Architecture
Client → Nginx (Port 80) → Gunicorn/Uvicorn → Flask/FastAPI App
            │
            └── Celery → RabbitMQ → Workers → (SMTP, Logging)


Frontend: Nginx as a reverse proxy.

Backend: Flask or FastAPI web application.

Task Queue: Celery workers connected to RabbitMQ.

External Exposure: ngrok tunneling to Nginx.

Project layout
.
├─ app.py               # Flask app + routes
├─ celery_app.py        # Celery factory (broker/backend and task discovery)
├─ tasks.py             # Celery task: send_email(...)
├─ requirements.txt     # (create one with pinned deps if needed)
├─ app.log              # runtime log (created automatically)
└─ .env                 # environment config (you create this)

Functional Requirements
1. Email Sending (/action?sendmail=<email>)

Accepts recipient email as query param.

Publishes a Celery task to RabbitMQ.

Celery worker sends email via SMTP.

2. Logging Current Time (/action?talktome)

Logs current server timestamp into app.log.

Demonstrates synchronous logging (or Celery-enabled logging if desired).

Implementation Steps
1. Install Dependencies
# System packages
sudo apt-get update
sudo apt-get install rabbitmq-server nginx python3-venv -y

# Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install flask fastapi celery gunicorn uvicorn pika

2. Start RabbitMQ
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

3. Configure Celery Tasks (tasks.py)

Define:

send_email_task → send email using SMTP

log_time_task → log current timestamp

4. Run Flask/FastAPI App (app.py)

Endpoints:

/action?sendmail=<email>

/action?talktome

5. Run Celery Workers
celery -A tasks worker --loglevel=info

6. Serve Behind Gunicorn
gunicorn -w 2 -b 127.0.0.1:8000 app:app

7. Configure Nginx Reverse Proxy

Example /etc/nginx/sites-available/messaging_sys:

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}


Enable site & restart Nginx:

sudo ln -s /etc/nginx/sites-available/messaging_sys /etc/nginx/sites-enabled/
sudo systemctl restart nginx

8. Expose via Ngrok
ngrok http 80


Ngrok will provide a public HTTPS URL.

Testing
Send Email
https://<ngrok-id>.ngrok.io/action?sendmail=test@example.com


Expected: Email sent to recipient asynchronously.

Log Time
https://<ngrok-id>.ngrok.io/action?talktome


Expected: Current time logged in app.log.

 Deliverables

Running system accessible via ngrok endpoint.

Screen recording (≤ 3 minutes) showing:

RabbitMQ running locally.

Celery workers executing tasks.

Flask/Nginx serving requests.

Successful email send.

Log file update.

External testing via ngrok.

🛠 Technologies Used

RabbitMQ – Message broker

Celery – Task queue manager

Flask / FastAPI – Web framework

Gunicorn / Uvicorn – Application server

Nginx – Reverse proxy

SMTP – Email sending

Ngrok – Public endpoint

Python 3.9+

Conclusion

This project demonstrates how to integrate RabbitMQ + Celery with a Python web service, managed behind Nginx, and exposed publicly with ngrok.
It simulates real-world production patterns like task queuing, reverse proxying, and background job execution in a lightweight, testable environment.
