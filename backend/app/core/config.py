from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "DarkWeb Intel"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite://darkweb_intel.db"
    ANTHROPIC_API_KEY: str = "your-api-key-here"
    TELEGRAM_BOT_TOKEN: str = "your-bot-token-here"
    TELEGRAM_CHAT_ID: str = "your-chat-id-here"
    TOR_PROXY_URL: str = "socks5://127.0.0.1:9050"
    
    # Payment Gateway Keys
    STRIPE_PUBLISHABLE_KEY: str = "your-stripe-publishable-key-here"
    STRIPE_SECRET_KEY: str = "your-stripe-secret-key-here"
    STRIPE_WEBHOOK_SECRET: str = "your-stripe-webhook-secret-here"
    
    PAYPAL_CLIENT_ID: str = "your-paypal-client-id-here"
    PAYPAL_CLIENT_SECRET: str = "your-paypal-client-secret-here"
    PAYPAL_WEBHOOK_ID: str = "your-paypal-webhook-id-here"
    
    RAZORPAY_KEY_ID: str = "your-razorpay-key-id-here"
    RAZORPAY_KEY_SECRET: str = "your-razorpay-key-secret-here"
    RAZORPAY_WEBHOOK_SECRET: str = "your-razorpay-webhook-secret-here"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
