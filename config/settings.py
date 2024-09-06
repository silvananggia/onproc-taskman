# config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# Redis configuration for Celery
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Celery configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Other settings
POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', '5'))  # in seconds
