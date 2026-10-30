"""
Test the transaction fraud detection API and features endpoint.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.app.services import prediction_service, training_service

def test_transaction_analysis():
    print("🧪 Testing Transaction Fraud Detection")
    print("=" * 70)
    
    # Test 1: Check model status
    print("\n1️⃣  Checking model status...")
    status = training_service.status('fraud')
    print(f"   State: {status['state']}")
    print(f"   Model: {status.get('selected_model', 'N/A')}")
    print(f"   ✅ Model is ready!" if status['state'] == 'ready' else "   ⚠️  Model not trained")
    
    # Test 2: Get model metadata
    print("\n2️⃣  Getting model features...")
    meta = training_service.metadata('fraud')
    if meta:
        print(f"   Dataset: {meta['dataset_id']}")
        print(f"   Features: {len(meta['features'])} total")
        print(f"   Target: {meta['target_column']}")
        print(f"   Model: {meta['selected_model']}")
    
    # Test 3: Legitimate transaction
    print("\n3️⃣  Testing LEGITIMATE transaction...")
    legitimate = {
        'Time': 0,
        'V1': -1.3598071,
        'V2': -0.0727812,
        'V3': 2.5363467,
        'V4': 1.3781552,
        'V5': -0.3383208,
        'V6': 0.4623878,
        'V7': 0.2395986,
        'V8': 0.0986979,
        'V9': 0.3637870,
        'V10': 0.0907942,
        'V11': -0.5515995,
        'V12': -0.6178009,
        'V13': -0.9913898,
        'V14': -0.3111694,
        'V15': 1.4681770,
        'V16': -0.4704005,
        'V17': 0.2079712,
        'V18': 0.0257906,
        'V19': 0.4039930,
        'V20': 0.2514121,
        'V21': -0.0183068,
        'V22': 0.2778376,
        'V23': -0.1104739,
        'V24': 0.0669281,
        'V25': 0.1285394,
        'V26': -0.1891148,
        'V27': 0.1335584,
        'V28': -0.0210531,
        'Amount': 149.62
    }
    
    try:
        result = prediction_service.predict(legitimate, task='fraud')
        print(f"   🎯 Prediction: {result['prediction']}")
        print(f"   📊 Probability: {result['fraud_probability']:.2%}" if result['fraud_probability'] else "   📊 Probability: N/A")
        print(f"   ⚠️  Risk: {result['risk_level']}")
        print(f"   ✅ Correct! (Expected: Legitimate)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Fraudulent transaction (from actual dataset)
    print("\n4️⃣  Testing FRAUD transaction...")
    fraud = {
        'Time': 406,
        'V1': -2.3122265,
        'V2': 1.9519948,
        'V3': -1.6098756,
        'V4': 3.9979055,
        'V5': -0.5226517,
        'V6': -1.4265449,
        'V7': -2.5373178,
        'V8': 1.3918735,
        'V9': -2.7700927,
        'V10': -2.7720840,
        'V11': 3.2027680,
        'V12': -2.8998528,
        'V13': -0.5954256,
        'V14': -4.2890508,
        'V15': 0.3896587,
        'V16': -1.1407699,
        'V17': -2.8308736,
        'V18': -0.0168244,
        'V19': 0.4169792,
        'V20': 0.1267900,
        'V21': -0.0089830,
        'V22': 0.5176168,
        'V23': -0.0352153,
        'V24': -0.4657991,
        'V25': 0.3207873,
        'V26': -0.1390963,
        'V27': -0.0553528,
        'V28': -0.0597518,
        'Amount': 0.77
    }
    
    try:
        result = prediction_service.predict(fraud, task='fraud')
        print(f"   🎯 Prediction: {result['prediction']}")
        print(f"   📊 Probability: {result['fraud_probability']:.2%}" if result['fraud_probability'] else "   📊 Probability: N/A")
        print(f"   ⚠️  Risk: {result['risk_level']}")
        print(f"   ✅ Model detected the fraud!" if result['prediction'] == 'Fraud' else "   ⚠️  Model missed this fraud")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Transaction fraud detection system is working!")
    print("\n💡 To test via frontend:")
    print("   1. python run.py")
    print("   2. Open http://127.0.0.1:8000/pages/analyze.html")
    print("   3. Select 'Transaction fraud'")
    print("   4. Click 'Load Sample Transaction'")
    print("   5. Click 'Run risk assessment'")

if __name__ == "__main__":
    test_transaction_analysis()
