# Distressed Seller Detection System - MVP

Automated pipeline to identify properties with high seller distress probability in St. Petersburg, Florida.

## Quick Start

```bash
# 1. Install dependencies
pip install requests pandas sqlalchemy schedule python-dotenv

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your API keys and database URL

# 3. Initialize database
python -m src.db.init

# 4. Run daily scan
python -m src.main --mode=daily_scan

# 5. Generate leads report
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
│   ├── emailer.py           # Email outreach
│   └── db/
│       ├── __init__.py
│       └── schema.py        # Database models
├── data/                    # Output files
├── config.py                # Configuration
├── .env.example             # Environment template
├── requirements.txt
└── README.md
```

## Configuration

Copy `.env.example` to `.env` and fill in:

- `HASDATA_API_KEY` - Property data API
- `DATABASE_URL` - PostgreSQL connection
- `GMAIL_USER` - Gmail for sending emails
- `GMAIL_APP_PASSWORD` - Gmail app password
- `TARGET_ZIP_CODES` - 33701,33702,33703,33704,33705,33706,33707,33708,33709,33710,33711,33712,33713,33714,33715,33716

## Target Market

St. Petersburg, Florida zip codes:
- Downtown: 33701, 33704
- Beach areas: 33706, 33707, 33708
- Mid-city: 33702, 33703, 33705, 33710
- South St. Pete: 33711, 33712, 33713, 33714

## Scoring System

Properties scored 0-100 based on distress signals:

- **Days on Market (25 pts)**: >60 days = high distress
- **Price Reduction % (25 pts)**: >10% reduction = high distress
- **Price Drops Count (20 pts)**: 3+ drops = motivated seller
- **Below Zestimate (10 pts)**: >5% below = distressed
- **View-to-Favorite Ratio (5 pts)**: <5% = low interest
- **Market Context (15 pts)**: 2x avg DOM = problem property

## Contact Strategy

Score Range | Category | Action
---|---|---
85-100 | Urgent | Contact immediately
70-84 | High | Reach out within 24-48hrs
50-69 | Moderate | Monitor
0-49 | Low | Not a priority

## Notes

- **Don't push live without approval** - All changes are PRs for review
- Test with free tier APIs before scaling
- Check local compliance rules for cold outreach