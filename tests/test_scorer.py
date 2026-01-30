"""
Ralph Wiggum Tests for Distressed Seller Scorer
================================================

SUCCESS CRITERIA:
- All tests must PASS
- Test coverage for all scoring logic
- Edge cases handled gracefully
- No crashes on invalid input

Run tests:
    python -m pytest tests/test_scorer.py -v

Ralph Loop:
    /ralph-loop "Fix scorer.py until all tests pass. Output <promise>COMPLETE</promise> when done." --max-iterations 20
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.scorer import DistressScorer


class TestDistressScorer(unittest.TestCase):
    """Core scoring tests - these MUST pass."""

    def setUp(self):
        self.scorer = DistressScorer()

    # ========================================================================
    # BASIC FUNCTIONALITY TESTS (Must Pass)
    # ========================================================================

    def test_highly_distressed_property(self):
        """Property with 95 DOM, 15% price reduction, 4 drops = HIGH distress."""
        prop = {
            'property_id': 'prop-1',
            'address': '456 Oak St, St. Petersburg, FL 33701',
            'current_price': 425000,
            'listing_days': 95,
            'price_history': [
                {'date': '2025-01-01', 'price': 500000},
                {'date': '2025-01-15', 'price': 480000},
                {'date': '2025-02-01', 'price': 460000},
                {'date': '2025-02-15', 'price': 440000},
                {'date': '2025-03-01', 'price': 425000},
            ],
            'estimated_value': 480000,
            'views': 3000,
            'favorites': 50,
        }
        score, details = self.scorer.calculate_score(prop)
        self.assertGreaterEqual(score, 70, "Should be HIGH distress")
        self.assertEqual(details['dom_points'], 20, "95 DOM = 20 points")

    def test_low_distress_property(self):
        """Property with 10 DOM, no price changes = LOW distress."""
        prop = {
            'property_id': 'prop-2',
            'address': '789 Pine St, St. Petersburg, FL 33702',
            'current_price': 350000,
            'listing_days': 10,
            'price_history': [{'date': '2025-03-01', 'price': 350000}],
            'estimated_value': 355000,
            'views': 2000,
            'favorites': 200,
        }
        score, details = self.scorer.calculate_score(prop)
        self.assertLessEqual(score, 20, "Should be LOW distress")
        self.assertEqual(details['dom_points'], 0, "10 DOM = 0 points")

    def test_score_never_exceeds_100(self):
        """Score must be capped at 100."""
        prop = {
            'property_id': 'prop-3',
            'address': '111 Max St',
            'current_price': 100000,
            'listing_days': 200,
            'price_history': [
                {'date': '2025-01-01', 'price': 1000000},
            ],
            'estimated_value': 500000,
            'views': 10000,
            'favorites': 0,
        }
        score, details = self.scorer.calculate_score(prop)
        self.assertLessEqual(score, 100, "Score must not exceed 100")
        self.assertEqual(score, 100, "Score should be exactly 100")

    # ========================================================================
    # EDGE CASES (Must Handle Gracefully)
    # ========================================================================

    def test_empty_price_history(self):
        """Empty price history should not crash."""
        prop = {
            'property_id': 'prop-4',
            'address': '222 Empty St',
            'current_price': 400000,
            'listing_days': 30,
            'price_history': [],
            'estimated_value': 410000,
            'views': 500,
            'favorites': 25,
        }
        score, details = self.scorer.calculate_score(prop)
        self.assertIsInstance(score, int, "Score must be an integer")
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_zero_views(self):
        """Zero views should not cause division by zero."""
        prop = {
            'property_id': 'prop-5',
            'address': '333 Zero St',
            'current_price': 300000,
            'listing_days': 45,
            'price_history': [{'date': '2025-01-01', 'price': 300000}],
            'estimated_value': 305000,
            'views': 0,
            'favorites': 0,
        }
        score, details = self.scorer.calculate_score(prop)
        self.assertIsInstance(score, int, "Score must be an integer")

    def test_zero_zestimate(self):
        """Zero zestimate should not crash."""
        prop = {
            'property_id': 'prop-6',
            'address': '444 Zillow Fail Ave',
            'current_price': 350000,
            'listing_days': 50,
            'price_history': [{'date': '2025-01-01', 'price': 350000}],
            'estimated_value': 0,
            'views': 800,
            'favorites': 40,
        }
        score, details = self.scorer.calculate_score(prop)
        self.assertIsInstance(score, int)
        self.assertEqual(details['below_estimate_points'], 0)

    # ========================================================================
    # CATEGORY ASSIGNMENTS (Must Be Correct)
    # ========================================================================

    def test_category_urgent(self):
        """Score >= 85 should be URGENT."""
        category, _ = self.scorer.get_category(85)
        self.assertEqual(category, 'URGENT')

    def test_category_high(self):
        """Score 70-84 should be HIGH."""
        category, _ = self.scorer.get_category(70)
        self.assertEqual(category, 'HIGH')
        category, _ = self.scorer.get_category(84)
        self.assertEqual(category, 'HIGH')

    def test_category_moderate(self):
        """Score 50-69 should be MODERATE."""
        category, _ = self.scorer.get_category(50)
        self.assertEqual(category, 'MODERATE')
        category, _ = self.scorer.get_category(69)
        self.assertEqual(category, 'MODERATE')

    def test_category_low(self):
        """Score < 50 should be LOW."""
        category, _ = self.scorer.get_category(49)
        self.assertEqual(category, 'LOW')
        category, _ = self.scorer.get_category(0)
        self.assertEqual(category, 'LOW')

    # ========================================================================
    # SCORING BREAKDOWN VERIFICATION
    # ========================================================================

    def test_dom_points_calculation(self):
        """Verify DOM points are calculated correctly."""
        test_cases = [
            (29, 0),   # <30 days = 0
            (30, 5),   # 30-44 = 5
            (45, 10),  # 45-59 = 10
            (60, 15),  # 60-89 = 15
            (90, 20),  # 90-119 = 20
            (120, 25), # 120+ = 25
        ]
        for days, expected in test_cases:
            prop = {
                'property_id': f'prop-{days}',
                'address': '123 Test St',
                'current_price': 400000,
                'listing_days': days,
                'price_history': [{'date': '2025-01-01', 'price': 400000}],
                'estimated_value': 400000,
                'views': 1000,
                'favorites': 50,
            }
            score, details = self.scorer.calculate_score(prop)
            self.assertEqual(details['dom_points'], expected, 
                           f"Days={days}: expected {expected}, got {details['dom_points']}")


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)