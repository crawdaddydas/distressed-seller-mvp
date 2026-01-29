"""Property data collection from HasData Zillow/Redfin API"""
import requests
from datetime import datetime
from config import HASDATA_API_KEY, TARGET_ZIP_CODES

class PropertyCollector:
    """Fetch property data from HasData API"""

    def __init__(self, api_key=HASDATA_API_KEY):
        self.api_key = api_key
        self.base_url = "https://api.hasdata.com/scrape/zillow"

    def search_properties(self, zip_code, max_results=100):
        """Search properties in a zip code"""
        if not self.api_key:
            print("⚠️  No API key configured - using mock data")
            return self._mock_search(zip_code, max_results)

        search_url = f"https://www.zillow.com/homes/{zip_code}_rb/"
        payload = {
            "apikey": self.api_key,
            "url": search_url,
            "render": "json"
        }

        try:
            response = requests.get(self.base_url, params=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                property_ids = [p.get('zpid') for p in data.get('results', [])]
                return property_ids[:max_results]
            else:
                print(f"❌ API error: {response.status_code}")
                return self._mock_search(zip_code, max_results)
        except Exception as e:
            print(f"❌ Request error: {e}")
            return self._mock_search(zip_code, max_results)

    def get_property_details(self, property_id):
        """Fetch detailed property data"""
        if not self.api_key:
            return self._mock_property(property_id)

        detail_url = f"{self.base_url}/property/{property_id}"
        payload = {
            "apikey": self.api_key,
            "country": "us"
        }

        try:
            response = requests.get(detail_url, params=payload, timeout=30)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"❌ Detail request error: {e}")
            return None

    def batch_collect(self, zip_codes=TARGET_ZIP_CODES, max_per_zip=50):
        """Collect properties from multiple zip codes"""
        all_properties = []

        for zip_code in zip_codes:
            print(f"📍 Scanning zip code: {zip_code}")

            try:
                property_ids = self.search_properties(zip_code, max_per_zip)
                print(f"   Found {len(property_ids)} properties")

                for prop_id in property_ids:
                    details = self.get_property_details(prop_id)
                    if details:
                        all_properties.append(details)

            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue

        print(f"\n✅ Total properties collected: {len(all_properties)}")
        return all_properties

    def _mock_search(self, zip_code, max_results):
        """Generate mock property IDs for testing"""
        return [f"mock-{zip_code}-{i}" for i in range(min(max_results, 5))]

    def _mock_property(self, property_id):
        """Generate mock property data for testing"""
        import random
        return {
            'property_id': property_id,
            'address': f'{random.randint(100,999)} Mock Street',
            'city': 'St. Petersburg',
            'state': 'FL',
            'zip_code': property_id.split('-')[1] if '-' in property_id else '33701',
            'current_price': random.randint(200000, 800000),
            'listing_date': '2025-01-01',
            'listing_days': random.randint(30, 120),
            'status': 'FOR_SALE',
            'views': random.randint(100, 5000),
            'favorites': random.randint(5, 200),
            'estimated_value': random.randint(250000, 850000),
            'last_sold_price': random.randint(150000, 600000),
            'last_sold_date': '2020-01-01',
            'agent_name': 'Mock Agent',
            'agent_phone': '555-0100',
            'agent_email': 'mock@realty.com',
            'price_history': [
                {'date': '2025-01-01', 'price': random.randint(200000, 800000)},
            ]
        }


if __name__ == '__main__':
    collector = PropertyCollector()
    properties = collector.batch_collect(['33701'], max_per_zip=5)
    print(f"Collected {len(properties)} properties")