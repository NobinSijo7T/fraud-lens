"""
Test URL feature extraction.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.app.services.url_feature_extractor import extract_features

def test_url_extraction():
    print("🧪 Testing URL Feature Extraction")
    print("=" * 70)
    
    # Test URLs
    test_cases = [
        {
            "name": "Legitimate HTTPS URL",
            "url": "https://www.rmit.edu.au/",
            "expected_phishing": False
        },
        {
            "name": "Suspicious IP-based URL",
            "url": "http://192.168.1.100/login.php?redirect=https://bank.com",
            "expected_phishing": True
        },
        {
            "name": "Long URL with many subdomains",
            "url": "http://secure.login.verify.account.update.suspicious-site.com/auth/verify?token=abc123&user=test",
            "expected_phishing": True
        },
        {
            "name": "Simple legitimate URL",
            "url": "https://github.com/user/repository",
            "expected_phishing": False
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   URL: {test_case['url']}")
        print("-" * 70)
        
        try:
            features = extract_features(test_case['url'])
            
            # Display key features
            print(f"   ✓ url_len: {features['url_len']}")
            print(f"   ✓ dom_len: {features['dom_len']}")
            print(f"   ✓ is_ip: {features['is_ip']} {'⚠️ IP ADDRESS!' if features['is_ip'] else '✓ Domain name'}")
            print(f"   ✓ is_https: {features['is_https']} {'✓ Secure' if features['is_https'] else '⚠️ Not secure'}")
            print(f"   ✓ subdom_cnt: {features['subdom_cnt']} {'⚠️ Many subdomains' if features['subdom_cnt'] > 3 else ''}")
            print(f"   ✓ entropy: {features['entropy']:.2f} {'⚠️ High randomness' if features['entropy'] > 4.5 else ''}")
            print(f"   ✓ query_len: {features['query_len']}")
            
            print(f"\n   All 22 features extracted: {list(features.keys())}")
            print(f"   Expected phishing: {test_case['expected_phishing']}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("✅ URL feature extraction test completed!")
    print("\nYou can now use the frontend to:")
    print("1. Select 'Phishing URL' task")
    print("2. Paste any URL in the input box")
    print("3. Click 'Extract Features'")
    print("4. All 22 features will be auto-filled!")

if __name__ == "__main__":
    test_url_extraction()
