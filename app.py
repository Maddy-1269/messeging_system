from flask import Flask, request, jsonify
from tasks import send_email
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(filename="app.log", level=logging.INFO)

@app.route("/")
def index():
    return (
        "<h1>Messaging System is running</h1>"
        '<p>Try: <a href="/action?talktome">/action?talktome</a></p>'
        '<p>Or: <code>/action?sendmail=you@example.com</code></p>'
    )

@app.route("/action")
def action():
    if "talktome" in request.args:
        timestamp = datetime.utcnow().isoformat()
        logging.info(f"Timestamp logged: {timestamp}")
        return jsonify({"logged": timestamp, "status": "ok"})
    elif "sendmail" in request.args:
        email = request.args.get("sendmail")
        send_email.delay(email)   # queue async task
        return jsonify({"message": "email task queued"})
    else:
        return jsonify({"error": "use ?sendmail=<email> or ?talktome"})
