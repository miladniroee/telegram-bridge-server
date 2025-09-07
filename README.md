# Telegram Bridge Server

A Flask-based proxy server that bridges Telegram Bot API with your applications. This server handles webhook forwarding, API proxying, and file downloads while providing proper error handling, logging, and security features.

## Features

- 🔄 **Webhook Forwarding**: Forwards Telegram webhooks to your application
- 🔗 **API Proxying**: Proxies Telegram Bot API requests from Laravel
- 📁 **File Downloads**: Handles Telegram file downloads with proper security
- 🛡️ **Security**: Token validation

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/miladniroee/telegram-bridge-server.git
cd telegram-bridge-server
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server

```bash
python app.py
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from @BotFather | - | ✅ |
| `APP_URL` | Your application webhook URL | - | ✅ |

## Endpoints

### Core Endpoints

- `GET /` - Health check and server info
- `POST /webhook` - Telegram webhook receiver
- `GET|POST /bot<token>/<method>` - Telegram API proxy
- `GET /file/bot<token>/<file_path>` - File download proxy

### Management Endpoints

- `POST /set-webhook` - Set Telegram webhook URL


### Logs

The application logs all requests and errors. In production, consider using structured logging:

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/miladniroee/telegram-bridge-server/issues) page
2. Create a new issue with detailed information
3. Include logs and configuration (without sensitive data)

