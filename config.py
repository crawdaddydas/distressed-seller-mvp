"""Configuration for Distressed Seller MVP"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
HASDATA_API_KEY = os.getenv('HASDATA_API_KEY', '')

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/distressed_sellers')

# Gmail
GMAIL_USER = os.getenv('GMAIL_USER', '')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')

# Target Market - St. Petersburg, FL
TARGET_ZIP_CODES = [
    '33701', '33702', '33703', '33704', '33705',
    '33706', '33707', '33708', '33709', '33710',
    '33711', '33712', '33713', '33714', '33715', '33716'
]

# Scoring Thresholds
DISTRESS_THRESHOLD = 70  # Score >= 70 = high priority lead
URGENT_THRESHOLD = 85    # Score >= 85 = urgent contact

# Email Settings
EMAIL_SIGNATURE = """
---
Sent via Distressed Seller Detection System
"""