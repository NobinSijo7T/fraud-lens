"""
Test the transaction scenarios with the actual API
"""
import requests
import json

API_BASE = "http://127.0.0.1:8000/api/v1"

# Test scenario from analyze-simple.js
scenarios = {
    "small_purchase": {
        "name": "Small Online Purchase ($25)",
        "features": {
            "Time": 0, "V1": -1.36, "V2": -0.07, "V3": 2.54, "V4": 1.38, "V5": -0.34,
            "V6": 0.46, "V7": 0.24, "V8": 0.10, "V9": 0.36, "V10": 0.09,
            "V11": -0.55, "V12": -0.62, "V13": -0.99, "V14": -0.31, "V15": 1.47,
            "V16": -0.47, "V17": 0.21, "V18": 0.03, "V19": 0.40, "V20": 0.25,
            "V21": -0.02, "V22": 0.28, "V23": -0.11, "V24": 0.07, "V25": 0.13,
            "V26": -0.19, "V27": 0.13, "V28": -0.02, "Amount": 25
        }
    },
    "suspicious_rapid": {
        "name": "🚨 Suspicious: Rapid Multiple Transactions",
        "features": {
            "Time": 406, "V1": -2.31, "V2": 1.95, "V3": -1.61, "V4": 4.00, "V5": -0.52,
            "V6": -1.43, "V7": -2.54, "V8": 1.39, "V9": -2.77, "V10": -2.77,
            "V11": 3.20, "V12": -2.90, "V13": -0.60, "V14": -4.29, "V15": 0.39,
            "V16": -1.14, "V17": -2.83, "V18": -0.02, "V19": 0.42, "V20": 0.13,
            "V21": -0.01, "V22": 0.52, "V23": -0.04, "V24": -0.47, "V25": 0.32,
            "V26": -0.14, "V27": -0.06, "V28": -0.06, "Amount": 0.77
        }
    }
}

print("Testing Transaction Scenarios\n" + "=" * 50)

for key, scenario in scenarios.items():
    print(f"\n{scenario['name']}")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{API_BASE}/predict/transaction",
            json={"data": scenario["features"]},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction: {result['prediction']}")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   Probability: {result['fraud_probability']:.1%}")
            print(f"   Model: {result['model_version']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

print("\n" + "=" * 50)
print("Test complete!")
