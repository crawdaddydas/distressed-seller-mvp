"""Distress scoring engine for properties"""
import pandas as pd
from datetime import datetime
from config import TARGET_ZIP_CODES

class DistressScorer:
    """Calculate and store distress scores for properties"""

    def __init__(self, market_avg_dom=30):
        self.market_avg_dom = market_avg_dom

    def calculate_score(self, property_data, market_data=None):
        """
        Calculate distress score from 0-100
        Higher score = more distressed seller
        """
        if not market_data:
            market_data = {'avg_days_on_market': self.market_avg_dom}

        score = 0
        details = {}

        # PRIMARY SIGNALS (70 points possible)

        # 1. Days on Market (25 points)
        dom = property_data.get('listing_days', 0)
        if dom >= 120:
            score += 25
            dom_pts = 25
        elif dom >= 90:
            score += 20
            dom_pts = 20
        elif dom >= 60:
            score += 15
            dom_pts = 15
        elif dom >= 45:
            score += 10
            dom_pts = 10
        elif dom >= 30:
            score += 5
            dom_pts = 5
        else:
            dom_pts = 0
        details['dom_points'] = dom_pts

        # 2. Price Reduction % (25 points)
        price_history = property_data.get('price_history', [])
        if len(price_history) > 1:
            original_price = price_history[0].get('price', 0)
            current_price = property_data.get('current_price', 0)
            if original_price > 0:
                reduction_pct = ((original_price - current_price) / original_price) * 100

                if reduction_pct >= 15:
                    score += 25
                    red_pts = 25
                elif reduction_pct >= 10:
                    score += 20
                    red_pts = 20
                elif reduction_pct >= 7:
                    score += 15
                    red_pts = 15
                elif reduction_pct >= 5:
                    score += 10
                    red_pts = 10
                elif reduction_pct >= 3:
                    score += 5
                    red_pts = 5
                else:
                    red_pts = 0
        else:
            reduction_pct = 0
            red_pts = 0
        details['reduction_points'] = red_pts

        # 3. Number of Price Drops (20 points)
        num_drops = len(price_history) - 1 if len(price_history) > 0 else 0
        if num_drops >= 5:
            score += 20
            drop_pts = 20
        elif num_drops >= 4:
            score += 16
            drop_pts = 16
        elif num_drops >= 3:
            score += 12
            drop_pts = 12
        elif num_drops >= 2:
            score += 8
            drop_pts = 8
        elif num_drops >= 1:
            score += 4
            drop_pts = 4
        else:
            drop_pts = 0
        details['drop_count_points'] = drop_pts

        # SECONDARY SIGNALS (30 points possible)

        # 4. Price Below Zestimate (10 points)
        zestimate = property_data.get('estimated_value', 0)
        current_price = property_data.get('current_price', 0)
        if zestimate > 0 and current_price > 0:
            below_zestimate_pct = ((zestimate - current_price) / zestimate) * 100
            if below_zestimate_pct >= 10:
                score += 10
                est_pts = 10
            elif below_zestimate_pct >= 5:
                score += 7
                est_pts = 7
            elif below_zestimate_pct >= 3:
                score += 4
                est_pts = 4
            else:
                est_pts = 0
        else:
            est_pts = 0
        details['below_estimate_points'] = est_pts

        # 5. View-to-Favorite Ratio (5 points)
        views = property_data.get('views', 0)
        favorites = property_data.get('favorites', 0)
        if views > 0:
            fav_ratio = (favorites / views) * 100
            if fav_ratio < 3:
                score += 5
                eng_pts = 5
            elif fav_ratio < 5:
                score += 3
                eng_pts = 3
            else:
                eng_pts = 0
        else:
            eng_pts = 0
        details['engagement_points'] = eng_pts

        # 6. Market Context (15 points)
        local_avg_dom = market_data.get('avg_days_on_market', 30)
        if local_avg_dom > 0:
            dom_multiple = dom / local_avg_dom
            if dom_multiple >= 3:
                score += 15
                mkt_pts = 15
            elif dom_multiple >= 2:
                score += 10
                mkt_pts = 10
            elif dom_multiple >= 1.5:
                score += 5
                mkt_pts = 5
            else:
                mkt_pts = 0
        else:
            mkt_pts = 0
        details['market_context_points'] = mkt_pts

        return min(score, 100), details

    def score_property(self, property_data, market_data=None):
        """Score a single property"""
        score, details = self.calculate_score(property_data, market_data)
        return {
            'property_id': property_data.get('property_id'),
            'score': score,
            'score_date': datetime.utcnow().date(),
            **details
        }

    def score_all(self, properties):
        """Score multiple properties"""
        results = []
        for prop in properties:
            score, _ = self.calculate_score(prop)
            results.append({
                'property_id': prop.get('property_id'),
                'address': prop.get('address'),
                'current_price': prop.get('current_price'),
                'listing_days': prop.get('listing_days'),
                'score': score,
                'agent_name': prop.get('agent_name'),
                'agent_phone': prop.get('agent_phone'),
                'agent_email': prop.get('agent_email'),
            })
        return sorted(results, key=lambda x: x['score'], reverse=True)

    def get_category(self, score):
        """Get category based on score"""
        if score >= 85:
            return 'URGENT', 'Contact immediately'
        elif score >= 70:
            return 'HIGH', 'Reach out within 24-48hrs'
        elif score >= 50:
            return 'MODERATE', 'Monitor'
        else:
            return 'LOW', 'Not a priority'


if __name__ == '__main__':
    scorer = DistressScorer()

    # Test with mock data
    test_prop = {
        'property_id': 'test-123',
        'address': '123 Test St, St. Petersburg, FL 33701',
        'current_price': 450000,
        'listing_days': 75,
        'price_history': [
            {'date': '2025-01-01', 'price': 500000},
            {'date': '2025-01-15', 'price': 475000},
            {'date': '2025-02-01', 'price': 450000},
        ],
        'estimated_value': 480000,
        'views': 3000,
        'favorites': 100,
        'agent_name': 'John Smith',
        'agent_phone': '555-1234',
        'agent_email': 'john@realty.com',
    }

    score, details = scorer.calculate_score(test_prop)
    category, action = scorer.get_category(score)

    print(f"Score: {score}/100")
    print(f"Category: {category}")
    print(f"Action: {action}")
    print(f"Details: {details}")