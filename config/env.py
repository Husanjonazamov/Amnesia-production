"""
Default value for environ variable
"""

import os

import environ

environ.Env.read_env(os.path.join(".env"))

env = environ.Env(
    DEBUG=(bool, False),
    CACHE_TIME=(int, 180),
    OTP_EXPIRE_TIME=(int, 2),
    VITE_LIVE=(bool, False),
    ALLOWED_HOSTS=(str, "localhost"),
    CSRF_TRUSTED_ORIGINS=(str, "localhost"),
    DJANGO_SETTINGS_MODULE=(str, "config.settings.local"),
    CACHE_TIMEOUT=(int, 120),
    CACHE_ENABLED=(bool, False),
    VITE_PORT=(int, 5173),
    VITE_HOST=(str, "vite"),
    NGROK_AUTHTOKEN=(str, "TOKEN"),
    BOT_TOKEN=(str, "TOKEN"),
    ADMIN_ID=(str, "TOKEN"),
    WEB_APP_URL=(str, "TOKEN"),
    CHANNEL_ID=(str, "TOKEN"),
    EXCHANGE_URL=(str, "TOKEN"),
    PAYME_ID=(str, "TOKEN"),
    PAYME_KEY=(str, "TOKEN"),
    OTP_MODULE="core.services.otp",
    OTP_SERVICE="EskizService",
    PROJECT_ENV=(str, "prod"),
)
