"""CityBuddy Backend API Test Suite - Phase 2 V1"""
import requests
import sys
import time
import base64
from datetime import datetime

class CityBuddyAPITester:
    def __init__(self, base_url="https://nepal-companion.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'X-User-Id': 'demo-user'
        }
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.test_data = {}

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None, timeout=30):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        self.tests_run += 1
        print(f"\n🔍 Test {self.tests_run}: {name}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, params=params, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=self.headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=self.headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ PASSED - Status: {response.status_code}")
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"   Response: {response.text[:200]}")
                except:
                    pass
                self.failed_tests.append({
                    "test": name,
                    "endpoint": endpoint,
                    "expected": expected_status,
                    "actual": response.status_code
                })
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ FAILED - Request timeout after {timeout}s")
            self.failed_tests.append({
                "test": name,
                "endpoint": endpoint,
                "error": f"Timeout after {timeout}s"
            })
            return False, {}
        except Exception as e:
            print(f"❌ FAILED - Error: {str(e)}")
            self.failed_tests.append({
                "test": name,
                "endpoint": endpoint,
                "error": str(e)
            })
            return False, {}

    def test_health(self):
        """Test health endpoints"""
        print("\n" + "="*60)
        print("TESTING: Health & Root")
        print("="*60)
        
        self.run_test("Root endpoint", "GET", "", 200)
        self.run_test("Health check", "GET", "health", 200)

    def test_places(self):
        """Test places endpoints"""
        print("\n" + "="*60)
        print("TESTING: Places")
        print("="*60)
        
        # Get cities
        success, cities = self.run_test("Get cities", "GET", "places/cities", 200)
        if success and cities:
            print(f"   Found {len(cities)} cities")
            if cities:
                self.test_data['city'] = cities[0]['city']
        
        # Get all places
        success, places = self.run_test("Get all places", "GET", "places", 200)
        if success and places:
            print(f"   Found {len(places)} places")
            if places:
                self.test_data['place_id'] = places[0]['id']
        
        # Filter by type
        self.run_test("Filter by type (restaurant)", "GET", "places", 200, 
                     params={"type": "restaurant"})
        
        # Filter by city
        if 'city' in self.test_data:
            self.run_test(f"Filter by city ({self.test_data['city']})", "GET", "places", 200,
                         params={"city": self.test_data['city']})
        
        # Search query
        self.run_test("Search places (q=temple)", "GET", "places", 200,
                     params={"q": "temple"})
        
        # Geo search (Kathmandu center)
        self.run_test("Geo search near Kathmandu", "GET", "places", 200,
                     params={"lat": 27.7172, "lon": 85.3240, "radius_km": 10})
        
        # Sort options
        self.run_test("Sort by price_low", "GET", "places", 200,
                     params={"sort": "price_low"})
        
        # Get place detail
        if 'place_id' in self.test_data:
            success, place = self.run_test(f"Get place detail", "GET", 
                                          f"places/{self.test_data['place_id']}", 200)
            if success:
                print(f"   Place: {place.get('name', 'N/A')}")
                print(f"   Has nearby: {len(place.get('nearby', []))} places")
                print(f"   Review stats: {place.get('review_count', 0)} reviews")

    def test_chat(self):
        """Test CityBrain chat endpoints"""
        print("\n" + "="*60)
        print("TESTING: CityBrain Chat (AI - may take 6-15s)")
        print("="*60)
        
        # Send a chat message
        success, response = self.run_test(
            "Send chat message",
            "POST",
            "chat/message",
            200,
            data={
                "message": "What are the best temples to visit in Kathmandu?",
                "context": {}
            },
            timeout=20
        )
        
        if success:
            conv_id = response.get('conversation_id')
            self.test_data['conversation_id'] = conv_id
            result = response.get('response', {})
            print(f"   Conversation ID: {conv_id}")
            print(f"   Summary: {result.get('summary', 'N/A')[:80]}...")
            print(f"   Recommendations: {len(result.get('recommendations', []))}")
            print(f"   Agents used: {result.get('agents_used', [])}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
        
        # List conversations
        success, convs = self.run_test("List conversations", "GET", "chat/conversations", 200)
        if success:
            print(f"   Found {len(convs)} conversations")
        
        # Get conversation detail
        if 'conversation_id' in self.test_data:
            success, conv = self.run_test(
                "Get conversation detail",
                "GET",
                f"chat/conversations/{self.test_data['conversation_id']}",
                200
            )
            if success:
                print(f"   Messages: {len(conv.get('messages', []))}")

    def test_trips(self):
        """Test trip generation and CRUD"""
        print("\n" + "="*60)
        print("TESTING: Trips (AI - may take 6-15s)")
        print("="*60)
        
        # Generate trip
        success, trip = self.run_test(
            "Generate trip itinerary",
            "POST",
            "trips/generate",
            200,
            data={
                "city": "Kathmandu",
                "days": 3,
                "budget_npr": 15000,
                "interests": ["culture", "food"]
            },
            timeout=30
        )
        
        if success:
            print(f"   Days: {len(trip.get('days', []))}")
            print(f"   Total cost: NPR {trip.get('estimated_cost_npr', 0)}")
        
        # Save trip
        if success:
            save_success, saved = self.run_test(
                "Save trip",
                "POST",
                "trips",
                200,
                data={
                    "title": "Test Kathmandu Trip",
                    "city": "Kathmandu",
                    "days": len(trip.get('days', [])),
                    "itinerary": trip.get('days', []),
                    "estimated_cost_npr": trip.get('estimated_cost_npr', 0)
                }
            )
            if save_success:
                self.test_data['trip_id'] = saved.get('id')
        
        # List trips
        success, trips = self.run_test("List trips", "GET", "trips", 200)
        if success:
            print(f"   Found {len(trips)} trips")
        
        # Get trip detail
        if 'trip_id' in self.test_data:
            self.run_test("Get trip detail", "GET", f"trips/{self.test_data['trip_id']}", 200)
        
        # Delete trip
        if 'trip_id' in self.test_data:
            self.run_test("Delete trip", "DELETE", f"trips/{self.test_data['trip_id']}", 200)

    def test_budgets(self):
        """Test budget CRUD"""
        print("\n" + "="*60)
        print("TESTING: Budgets")
        print("="*60)
        
        # Create budget
        success, budget = self.run_test(
            "Create budget",
            "POST",
            "budgets",
            200,
            data={
                "title": "Test Nepal Trip Budget",
                "city": "Kathmandu",
                "total_budget_npr": 50000,
                "entries": [
                    {"category": "Accommodation", "label": "Hotels", "amount_npr": 15000},
                    {"category": "Food", "label": "Meals", "amount_npr": 10000},
                    {"category": "Transport", "label": "Local transport", "amount_npr": 8000}
                ]
            }
        )
        
        if success:
            self.test_data['budget_id'] = budget.get('id')
            print(f"   Budget ID: {budget.get('id')}")
            print(f"   Total: NPR {budget.get('total_budget_npr')}")
            print(f"   Entries: {len(budget.get('entries', []))}")
        
        # List budgets
        success, budgets = self.run_test("List budgets", "GET", "budgets", 200)
        if success:
            print(f"   Found {len(budgets)} budgets")
        
        # Update budget
        if 'budget_id' in self.test_data:
            self.run_test(
                "Update budget",
                "PUT",
                f"budgets/{self.test_data['budget_id']}",
                200,
                data={
                    "title": "Updated Nepal Trip Budget",
                    "city": "Kathmandu",
                    "total_budget_npr": 55000,
                    "entries": [
                        {"category": "Accommodation", "label": "Hotels", "amount_npr": 15000},
                        {"category": "Food", "label": "Meals", "amount_npr": 12000},
                        {"category": "Transport", "label": "Local transport", "amount_npr": 8000}
                    ]
                }
            )
        
        # Delete budget
        if 'budget_id' in self.test_data:
            self.run_test("Delete budget", "DELETE", f"budgets/{self.test_data['budget_id']}", 200)

    def test_weather(self):
        """Test weather endpoints"""
        print("\n" + "="*60)
        print("TESTING: Weather (Live Open-Meteo)")
        print("="*60)
        
        # Get weather for Kathmandu
        success, weather = self.run_test(
            "Get weather for Kathmandu",
            "GET",
            "weather",
            200,
            params={"city": "Kathmandu"}
        )
        
        if success:
            print(f"   Current temp: {weather.get('current', {}).get('temperature_c', 'N/A')}°C")
            print(f"   Hourly forecast: {len(weather.get('hourly', []))} hours")
            print(f"   Daily forecast: {len(weather.get('daily', []))} days")
        
        # Get weather cities
        success, cities = self.run_test("Get weather cities", "GET", "weather/cities", 200)
        if success:
            print(f"   Available cities: {len(cities)}")

    def test_emergency(self):
        """Test emergency endpoints"""
        print("\n" + "="*60)
        print("TESTING: Emergency")
        print("="*60)
        
        # Get emergency numbers
        success, numbers = self.run_test("Get emergency numbers", "GET", "emergency/numbers", 200)
        if success:
            print(f"   Emergency numbers: {len(numbers)}")
        
        # Get nearby emergency (Kathmandu center)
        success, nearby = self.run_test(
            "Get nearby hospitals",
            "GET",
            "emergency/nearby",
            200,
            params={"lat": 27.7172, "lon": 85.3240, "type": "hospital"}
        )
        if success:
            print(f"   Nearby hospitals: {len(nearby)}")
        
        # Get all guidance
        success, guidance = self.run_test("Get all safety guidance", "GET", "emergency/guidance-all", 200)
        if success:
            print(f"   Guidance categories: {len(guidance)}")

    def test_nepal_info(self):
        """Test Nepal information endpoints"""
        print("\n" + "="*60)
        print("TESTING: Nepal Intelligence")
        print("="*60)
        
        self.run_test("Get Nepal overview", "GET", "nepal/overview", 200)
        
        success, festivals = self.run_test("Get festivals", "GET", "nepal/festivals", 200)
        if success:
            print(f"   Festivals: {len(festivals)}")
        
        success, treks = self.run_test("Get treks", "GET", "nepal/treks", 200)
        if success:
            print(f"   Treks: {len(treks)}")
        
        success, unesco = self.run_test("Get UNESCO sites", "GET", "nepal/unesco", 200)
        if success:
            print(f"   UNESCO sites: {len(unesco)}")
        
        self.run_test("Get transport info", "GET", "nepal/transport", 200)
        self.run_test("Get essential info", "GET", "nepal/info", 200)

    def test_vision(self):
        """Test vision analysis endpoint"""
        print("\n" + "="*60)
        print("TESTING: Vision Analysis (AI - may take 6-15s)")
        print("="*60)
        
        # Create a simple test image (1x1 red pixel PNG)
        test_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="
        
        success, result = self.run_test(
            "Analyze image",
            "POST",
            "vision/analyze",
            200,
            data={
                "image_base64": f"data:image/png;base64,{test_image_b64}",
                "note": "Test image analysis"
            },
            timeout=20
        )
        
        if success:
            print(f"   Identification: {result.get('identification', 'N/A')[:60]}...")
            print(f"   Has facts: {bool(result.get('facts'))}")
            print(f"   Has traveler tip: {bool(result.get('traveler_tip'))}")

    def test_favorites_reviews_profile(self):
        """Test favorites, reviews, and profile"""
        print("\n" + "="*60)
        print("TESTING: Favorites, Reviews, Profile")
        print("="*60)
        
        # Favorites
        success, favs = self.run_test("Get favorites", "GET", "favorites", 200)
        if success:
            print(f"   Favorites: {len(favs)}")
        
        success, fav_ids = self.run_test("Get favorite IDs", "GET", "favorites/ids", 200)
        if success:
            print(f"   Favorite IDs: {len(fav_ids)}")
        
        # Add favorite
        if 'place_id' in self.test_data:
            success, _ = self.run_test(
                "Add favorite",
                "POST",
                f"favorites/{self.test_data['place_id']}",
                200
            )
            
            # Remove favorite
            if success:
                self.run_test(
                    "Remove favorite",
                    "DELETE",
                    f"favorites/{self.test_data['place_id']}",
                    200
                )
        
        # Reviews
        if 'place_id' in self.test_data:
            success, reviews = self.run_test(
                "Get place reviews",
                "GET",
                f"places/{self.test_data['place_id']}/reviews",
                200
            )
            if success:
                print(f"   Reviews: {len(reviews)}")
            
            # Add review
            self.run_test(
                "Add review",
                "POST",
                f"places/{self.test_data['place_id']}/reviews",
                200,
                data={
                    "rating": 5,
                    "comment": "Great place! Test review from automated testing."
                }
            )
        
        # Profile
        success, profile = self.run_test("Get profile", "GET", "profile", 200)
        if success:
            print(f"   Profile name: {profile.get('name', 'N/A')}")
        
        # Update profile
        self.run_test(
            "Update profile",
            "PUT",
            "profile",
            200,
            data={
                "name": "Test User",
                "email": "test@example.com",
                "preferences": {
                    "interests": ["culture", "food", "trekking"]
                }
            }
        )

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {len(self.failed_tests)}")
        print(f"Success rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for fail in self.failed_tests:
                error_msg = fail.get('error', f"Status {fail.get('actual')}")
                print(f"  - {fail['test']}: {error_msg} (endpoint: {fail['endpoint']})")
        
        return 0 if len(self.failed_tests) == 0 else 1

def main():
    print("="*60)
    print("CityBuddy Backend API Test Suite - Phase 2 V1")
    print("="*60)
    
    tester = CityBuddyAPITester()
    
    # Run all test suites
    tester.test_health()
    tester.test_places()
    tester.test_chat()
    tester.test_trips()
    tester.test_budgets()
    tester.test_weather()
    tester.test_emergency()
    tester.test_nepal_info()
    tester.test_vision()
    tester.test_favorites_reviews_profile()
    
    return tester.print_summary()

if __name__ == "__main__":
    sys.exit(main())
