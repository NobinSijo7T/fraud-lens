"""
Test the URL analysis API endpoint.
This test requires the server to be running.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.app.services.url_feature_extractor import extract_features
from backend.app.services import prediction_service

def test_complete_flow():
    print("🧪 Testing Complete URL Analysis Flow")
    print("=" * 70)
    
    test_urls = [
        ("https://www.rmit.edu.au/", "Legitimate educational site"),
        ("http://192.168.1.100/login.php", "Suspicious IP-based URL"),
        ("https://github.com/user/repo", "Legitimate tech site")
    ]
    
    for url, description in test_urls:
        print(f"\n📊 Testing: {description}")
        print(f"   URL: {url}")
        print("-" * 70)
        
        try:
            # Step 1: Extract features
            features = extract_features(url)
            print(f"   ✓ Extracted {len(features)} features")
            
            # Step 2: Make prediction
            result = prediction_service.predict(features, task='phishing')
            
            # Display results
            print(f"\n   🎯 PREDICTION: {result['prediction']}")
            print(f"   📈 Probability: {result['fraud_probability']:.2%}" if result['fraud_probability'] else "   📈 Probability: N/A")
            print(f"   ⚠️  Risk Level: {result['risk_level']}")
            print(f"   🔧 Model: {result['model_version']}")
            
            # Show key indicators
            if features['is_ip']:
                print(f"   ⚠️  Warning: URL uses IP address instead of domain")
            if not features['is_https']:
                print(f"   ⚠️  Warning: URL does not use HTTPS")
            if features['subdom_cnt'] > 3:
                print(f"   ⚠️  Warning: Many subdomains ({features['subdom_cnt']})")
            if features['entropy'] > 4.5:
                print(f"   ⚠️  Warning: High entropy ({features['entropy']:.2f})")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Complete URL analysis flow test completed!")
    print("\n💡 To test via API (with server running):")
    print('   curl -X POST http://127.0.0.1:8000/api/v1/analyze/url \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d "{\\"url\\": \\"https://www.example.com\\"}"')

if __name__ == "__main__":
    test_complete_flow()
