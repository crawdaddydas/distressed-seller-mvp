"""Main entry point for Distressed Seller Detection System"""
import argparse
import sys
from datetime import datetime
from collector import PropertyCollector
from scorer import DistressScorer
from emailer import Emailer
from config import DISTRESS_THRESHOLD

def main():
    parser = argparse.ArgumentParser(description='Distressed Seller Detection System')
    parser.add_argument('--mode', choices=['daily_scan', 'export_leads', 'test_email', 'test'],
                       default='test', help='Operation mode')
    parser.add_argument('--min_score', type=int, default=DISTRESS_THRESHOLD,
                       help='Minimum distress score for leads')
    parser.add_argument('--email_template', choices=['initial', 'followup', 'cash_offer'],
                       default='initial', help='Email template')

    args = parser.parse_args()

    if args.mode == 'test':
        print("🧪 Running tests...")
        test_system()
    elif args.mode == 'daily_scan':
        run_daily_scan(args.min_score)
    elif args.mode == 'export_leads':
        export_leads(args.min_score)
    elif args.mode == 'test_email':
        test_email(args.email_template)


def test_system():
    """Test the scoring system"""
    print("=" * 50)
    print("🧪 DISTRESS SELLER MVP - TEST MODE")
    print("=" * 50)

    # Test scorer
    scorer = DistressScorer()

    test_cases = [
        {
            'name': 'Highly Distressed',
            'data': {
                'property_id': 'test-urgent',
                'address': '456 Oak St, St. Petersburg, FL 33701',
                'current_price': 400000,
                'listing_days': 95,
                'price_history': [
                    {'date': '2025-01-01', 'price': 500000},
                    {'date': '2025-01-15', 'price': 470000},
                    {'date': '2025-02-01', 'price': 450000},
                    {'date': '2025-02-15', 'price': 420000},
                    {'date': '2025-03-01', 'price': 400000},
                ],
                'estimated_value': 480000,
                'views': 5000,
                'favorites': 80,
                'agent_name': 'Mary Agent',
                'agent_phone': '555-0100',
                'agent_email': 'test@test.com',
            }
        },
        {
            'name': 'Moderately Distressed',
            'data': {
                'property_id': 'test-moderate',
                'address': '789 Pine St, St. Petersburg, FL 33702',
                'current_price': 350000,
                'listing_days': 45,
                'price_history': [
                    {'date': '2025-01-01', 'price': 365000},
                ],
                'estimated_value': 360000,
                'views': 1500,
                'favorites': 100,
                'agent_name': 'Bob Broker',
                'agent_phone': '555-0200',
                'agent_email': 'test@test.com',
            }
        },
    ]

    print("\n📊 Scoring Test Results:")
    print("-" * 50)

    for test in test_cases:
        score, details = scorer.calculate_score(test['data'])
        category, action = scorer.get_category(score)
        print(f"\n{test['name']}")
        print(f"  Address: {test['data']['address']}")
        print(f"  Score: {score}/100")
        print(f"  Category: {category}")
        print(f"  Action: {action}")
        print(f"  Details: {details}")

    print("\n" + "=" * 50)
    print("✅ Test complete!")


def run_daily_scan(min_score=DISTRESS_THRESHOLD):
    """Run daily property scan"""
    print(f"\n📅 Daily Scan - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("-" * 50)

    collector = PropertyCollector()
    scorer = DistressScorer()

    # Collect properties
    properties = collector.batch_collect(max_per_zip=10)

    if not properties:
        print("❌ No properties collected")
        return

    # Score properties
    scored = scorer.score_all(properties)

    # Filter by score
    high_priority = [p for p in scored if p['score'] >= min_score]

    print(f"\n📊 Results:")
    print(f"  Total collected: {len(properties)}")
    print(f"  High priority (score >= {min_score}): {len(high_priority)}")

    # Show top leads
    if high_priority:
        print(f"\n🎯 Top {min(10, len(high_priority))} Leads:")
        for lead in high_priority[:10]:
            category, _ = scorer.get_category(lead['score'])
            print(f"  [{category}] {lead['score']}/100 - {lead['address']}")
            print(f"         ${lead['current_price']} | {lead['listing_days']} days")

    return scored


def export_leads(min_score=DISTRESS_THRESHOLD):
    """Export leads to CSV"""
    print(f"\n📤 Exporting leads (score >= {min_score})...")
    print("-" * 50)

    collector = PropertyCollector()
    scorer = DistressScorer()

    # Collect and score
    properties = collector.batch_collect(max_per_zip=10)
    scored = scorer.score_all(properties)

    # Filter
    leads = [p for p in scored if p['score'] >= min_score]

    # Export to CSV
    if leads:
        import csv
        filename = f"leads_{datetime.now().strftime('%Y%m%d')}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=leads[0].keys())
            writer.writeheader()
            writer.writerows(leads)
        print(f"✅ Exported {len(leads)} leads to {filename}")
    else:
        print("❌ No leads to export")


def test_email(template='initial'):
    """Test email sending"""
    print(f"\n📧 Testing email ({template})...")
    print("-" * 50)

    emailer = Emailer()

    test_lead = {
        'property_id': 'test-email',
        'address': '123 Test St, St. Petersburg, FL 33701',
        'score': 85,
        'agent_name': 'Test Agent',
        'agent_email': 'dasgoswami@gmail.com',
    }

    emailer.send_outreach(test_lead['agent_email'], test_lead, template)


if __name__ == '__main__':
    main()