# Distressed Seller Detection System - MVP

Automated pipeline to identify properties with high seller distress probability in St. Petersburg, Florida.

## Quick Start

```bash
# 1. Install dependencies
pip install requests pandas sqlalchemy schedule python-dotenv

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your API keys and database URL

# 3. Initialize database (SQLite - no Docker needed)
python -m src.db.init

# 4. Run test
python -m src.main --mode=test

# 5. Run daily scan
python -m src.main --mode=daily_scan

# 6. Generate leads report
python -m src.main --mode=export_leads --min_score=70
```

## Project Structure

```
distressed-seller-mvp/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── collector.py         # Property data collection
│   ├── scorer.py            # Distress scoring engine
│   ├── emailer.py           # Email outreach (5 templates)
│   └── db/
│       ├── __init__.py
│       └── schema.py        # Database models
├── scripts/
│   ├── daily_scan.sh        # Cron script
│   └── crontab.example      # Cron setup
├── data/                    # SQLite database (auto-created)
├── logs/                    # Cron logs
├── config.py                # Configuration
├── .env.example             # Environment template
├── requirements.txt
└── README.md
```

## Database

**SQLite** (no Docker or server needed):
- Location: `data/distressed_sellers.db`
- Tables: properties, price_history, distress_scores

## Configuration

Copy `.env.example` to `.env` and fill in:

- `HASDATA_API_KEY` - Property data API (HasData recommended)
- `DATABASE_URL` - SQLite: `sqlite:///data/distressed_sellers.db`
- `GMAIL_USER` - Gmail for sending emails
- `GMAIL_APP_PASSWORD` - Gmail app password
- `TARGET_ZIP_CODES` - 33701-33716 (St. Petersburg, FL)

## Email Templates

5 personalized templates included:
- `initial` - First outreach
- `followup` - Follow-up email
- `cash_offer` - Direct cash offer
- `urgent` - High-urgency template
- `data_point` - Data-driven approach

Usage:
```bash
python -m src.main --email_template=cash_offer
```

## Automation (Cron)

```bash
# Add to crontab (runs daily at 6 AM EST)
crontab -e
# Add: 0 6 * * * /path/to/distressed-seller-mvp/scripts/daily_scan.sh
```

See `scripts/crontab.example` for full setup.