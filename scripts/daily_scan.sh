#!/bin/bash
# Daily scan script for cron job
# Add to crontab: 0 6 * * * /path/to/distressed-seller-mvp/scripts/daily_scan.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Run daily scan
python -m src.main --mode=daily_scan

# Export leads with score >= 70
python -m src.main --mode=export_leads --min_score=70

echo "✅ Daily scan complete at $(date)"