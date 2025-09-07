"""
Telegram Bridge Server
A Flask-based proxy server for Telegram Bot API integration.
"""

import os
import requests
import json
from flask import Flask, request, jsonify, Response
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
APP_URL = os.getenv('APP_URL')

TELEGRAM_API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
if not APP_URL:
    raise ValueError("APP_URL environment variable is required")

@app.route('/')
def home():
    return jsonify({"status": "Telegram Bridge Server Running", "version": "1.0"})

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    """
    Receives webhooks from Telegram and forwards them to app
    """
    try:
        telegram_data = request.get_json(force=True)

        if not telegram_data:
            logging.error("No JSON data received from Telegram")
            return jsonify({"error": "No data received"}), 400

        # Forward the webhook to app
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'TelegramBridge/1.0',
            'X-Forwarded-For': request.remote_addr
        }

        response = requests.post(
            APP_URL,
            json=telegram_data,
            headers=headers,
            timeout=30,
            allow_redirects=False  # Don't follow redirects
        )

        # Return OK to Telegram (important!)
        return jsonify({"ok": True})

    except Exception as e:
        logging.error(f"Webhook forwarding error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot<bot_token>/<path:telegram_method>', methods=['GET', 'POST'])
def telegram_api_proxy(bot_token, telegram_method):
    """
    Proxies API requests from App to Telegram API
    Mimics exact Telegram API structure: /bot<token>/method
    """

    try:
        # Verify token matches
        if bot_token != TELEGRAM_BOT_TOKEN:
            return jsonify({"error": "Invalid bot token"}), 401

        telegram_url = f"{TELEGRAM_API_BASE}/{telegram_method}"

        # Forward the request method and data
        if request.method == 'POST':
            if request.is_json:
                response = requests.post(telegram_url, json=request.get_json(), timeout=30)
            else:
                response = requests.post(telegram_url, data=request.form, files=request.files, timeout=30)
        else:
            response = requests.get(telegram_url, params=request.args, timeout=30)

        # Return the response from Telegram exactly as received
        response_headers = dict(response.headers)
        response_headers.pop('transfer-encoding', None)
        response_headers.pop('connection', None)

        return Response(
            response.content,
            status=response.status_code,
            headers=response_headers
        )

    except Exception as e:
        logging.error(f"API proxy error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/file/bot<bot_token>/<path:file_path>')
def download_telegram_file(bot_token, file_path):
    """
    Downloads files from Telegram with exact Telegram file URL structure
    Mimics: https://api.telegram.org/file/bot<token>/<file_path>
    """
    try:
        # Verify token matches (optional security check)
        if bot_token != TELEGRAM_BOT_TOKEN:
            return jsonify({"error": "Invalid bot token"}), 401

        # Download the file from Telegram
        download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        file_content = requests.get(download_url, timeout=30)

        if not file_content.ok:
            return jsonify({"error": "Failed to download file"}), 400

        # Return file with appropriate headers
        filename = os.path.basename(file_path)

        return Response(
            file_content.content,
            headers={
                'Content-Disposition': f'attachment; filename={filename}',
                'Content-Type': file_content.headers.get('Content-Type', 'application/octet-stream')
            }
        )

    except Exception as e:
        logging.error(f"File download error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/set-webhook', methods=['POST'])
def set_telegram_webhook():
    """
    Helper endpoint to set webhook URL on Telegram
    """
    try:
        webhook_data = request.get_json()
        webhook_url = webhook_data.get('url')

        if not webhook_url:
            return jsonify({"error": "webhook URL required"}), 400

        response = requests.post(
            f"{TELEGRAM_API_BASE}/setWebhook",
            json={"url": webhook_url},
            timeout=30
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# cPanel WSGI compatibility
application = app

# For local development only
if __name__ == '__main__':
    app.run(debug=True)
