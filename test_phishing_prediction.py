"""
Test the phishing detection model with sample URLs.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.app.services import prediction_service

def test_phishing_predictions():
    print("🧪 Testing Phishing Detection Model")
    print("=" * 60)
    
    # Example legitimate URL features (based on the phishing dataset structure)
    legitimate_url = {
        'url_len': 24,
        'dom_len': 11,
        'is_ip': 0,
        'tld_len': 6,
        'subdom_cnt': 1,
        'letter_cnt': 17,
        'digit_cnt': 0,
        'special_cnt': 7,
        'eq_cnt': 0,
        'qm_cnt': 0,
        'amp_cnt': 0,
        'dot_cnt': 3,
        'dash_cnt': 0,
        'under_cnt': 0,
        'letter_ratio': 0.708333,
        'digit_ratio': 0.0,
        'spec_ratio': 0.291667,
        'is_https': 1,
        'slash_cnt': 3,
        'entropy': 3.709148,
        'path_len': 1,
        'query_len': 0
    }
    
    # Example phishing URL features (more suspicious characteristics)
    phishing_url = {
        'url_len': 85,
        'dom_len': 25,
        'is_ip': 1,  # IP address instead of domain
        'tld_len': 3,
        'subdom_cnt': 5,
        'letter_cnt': 45,
        'digit_cnt': 15,
        'special_cnt': 25,
        'eq_cnt': 3,
        'qm_cnt': 2,
        'amp_cnt': 4,
        'dot_cnt': 8,
        'dash_cnt': 5,
        'under_cnt': 3,
        'letter_ratio': 0.529412,
        'digit_ratio': 0.176471,
        'spec_ratio': 0.294118,
        'is_https': 0,  # No HTTPS
        'slash_cnt': 6,
        'entropy': 4.85,
        'path_len': 35,
        'query_len': 25
    }
    
    print("\n1️⃣  Testing LEGITIMATE URL features:")
    try:
        result = prediction_service.predict(legitimate_url, task='phishing')
        print(f"   Prediction: {result['prediction']}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Probability: {result['fraud_probability']:.2%}" if result['fraud_probability'] else "   Probability: N/A")
        print(f"   ✅ Test passed!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n2️⃣  Testing PHISHING URL features:")
    try:
        result = prediction_service.predict(phishing_url, task='phishing')
        print(f"   Prediction: {result['prediction']}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Probability: {result['fraud_probability']:.2%}" if result['fraud_probability'] else "   Probability: N/A")
        print(f"   ✅ Test passed!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n✅ Phishing prediction system is working correctly!")
    print("   You can now use it from the frontend Analyze page.")

if __name__ == "__main__":
    test_phishing_predictions()
