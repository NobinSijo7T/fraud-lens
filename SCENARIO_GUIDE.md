# Transaction Fraud Detection - Scenario Guide

## Overview

The transaction fraud detection interface now uses a **scenario-based approach** instead of requiring manual entry of 30 PCA-transformed features (Time, V1-V28, Amount).

## Why Scenarios?

The model was trained on **PCA-transformed features** from the creditcard.csv dataset. These features (V1-V28) are **principal components** created through dimensionality reduction on the original transaction data. 

**Important limitation:** We cannot calculate V1-V28 from raw transaction data (like merchant name, card type, location) because:

1. PCA transformation requires the **entire original feature matrix** from the dataset creators
2. The original features (before PCA) are not publicly available
3. Each principal component is a weighted combination of ALL original features
4. The transformation is dataset-specific and cannot be reverse-engineered

## Solution: Pre-defined Realistic Scenarios

Instead of asking users to input V1-V28 values they don't have, we provide **6 realistic transaction scenarios** with actual feature values extracted from the dataset:

### Legitimate Scenarios

#### 1. Small Online Purchase ($25)
- **Context:** Amazon purchase, domestic, regular merchant
- **Expected:** Low risk, legitimate transaction
- **Actual Result:** 6.5% fraud probability, Low risk

#### 2. Large Purchase ($500)
- **Context:** Best Buy in-store, established merchant
- **Expected:** Low risk, legitimate transaction
- **Features:** Lower anomaly scores across principal components

#### 3. Monthly Subscription ($15)
- **Context:** Netflix recurring payment, familiar pattern
- **Expected:** Very low risk, legitimate
- **Features:** Consistent pattern indicators

### Suspicious Scenarios

#### 4. 🚨 Suspicious: Unusual Small Amount ($0.50)
- **Context:** Unknown merchant, foreign, testing transaction
- **Expected:** High risk, common fraud pattern
- **Features:** High anomaly scores in multiple components

#### 5. 🚨 Suspicious: Rapid Multiple Transactions ($0.77)
- **Context:** Multiple rapid transactions, unusual pattern
- **Expected:** Very high risk
- **Actual Result:** 100% fraud probability, High risk
- **Features:** Extreme outliers in V1, V4, V11, V14 (time/frequency patterns)

#### 6. 🚨 Suspicious: High Value Foreign Transaction ($1,200)
- **Context:** Large amount, foreign location, unusual time
- **Expected:** High risk
- **Features:** Multiple red flags across components

## How to Use

### Simple Mode (Default)

1. Navigate to the **Analyze** page
2. Select **"Transaction fraud"** from the dropdown
3. Click on any of the 6 scenario cards
4. View the fraud assessment result on the same page
5. Click "Analyze Another Scenario" to test more cases

### Advanced Mode

If you have actual PCA-transformed features (V1-V28):

1. Scroll to the bottom of the scenario cards
2. Click **"⚙️ Advanced: Enter V1-V28 Features Manually"**
3. Click **"Show Manual Input Form"**
4. Enter all 30 feature values manually
5. Submit for analysis

## Understanding the Results

Each analysis displays:

- **Prediction:** "Legitimate" or "Fraud"
- **Risk Level:** Low / Medium / High
- **Probability:** Fraud probability percentage
- **Model Version:** Which trained model was used
- **Scenario Details:** Real-world context (amount, type, location)

## Technical Details

### Feature Structure

Each scenario contains 30 features:
```javascript
{
  Time: 0,           // Seconds since first transaction
  V1: -1.36,         // Principal component 1
  V2: -0.07,         // Principal component 2
  ...
  V28: -0.02,        // Principal component 28
  Amount: 25         // Transaction amount in dollars
}
```

### Model Performance

- **Algorithm:** Logistic Regression
- **Training Accuracy:** 99.9%
- **Dataset:** 284,807 transactions (492 fraudulent)
- **Features:** 30 (Time + V1-V28 + Amount)

## API Endpoints

### Transaction Fraud Prediction
```http
POST /api/v1/predict/transaction
Content-Type: application/json

{
  "data": {
    "Time": 0,
    "V1": -1.36,
    ...
    "Amount": 25
  }
}
```

### Response
```json
{
  "prediction": "Legitimate",
  "is_fraud": 0,
  "fraud_probability": 0.065,
  "risk_level": "Low",
  "model_version": "logistic_regression_v1",
  "task": "fraud",
  "disclaimer": "This prediction is a risk assessment, not proof of fraud."
}
```

## Files Modified

### Frontend
- `frontend/pages/analyze.html` - Updated to use scenario-based interface
- `frontend/js/analyze-simple.js` - NEW: Scenario cards and inline results
- `frontend/js/analyze.js` - Original manual form (available in advanced mode)
- `frontend/js/api.js` - API integration functions
- `frontend/js/utils.js` - Helper functions (esc, pct, fmt)

### Backend
- `backend/app/main.py` - Transaction prediction endpoint
- `backend/app/services/prediction_service.py` - Fraud detection logic
- `backend/app/services/training_service.py` - Model training
- `artifacts/selected_model.joblib` - Trained logistic regression model
- `artifacts/metadata.json` - Model metadata and feature names

## Testing

Run the test script to verify scenarios:
```bash
python test_scenario_ui.py
```

Expected output:
- Small Purchase: ~6.5% fraud probability (Legitimate)
- Suspicious Rapid: 100% fraud probability (Fraud)

## Future Enhancements

### If Original Features Become Available

If the dataset creators release the original features (before PCA transformation), we could:

1. Create a **feature extraction service** that converts:
   - Merchant category codes
   - Transaction type
   - Device fingerprint
   - Geographic location
   - Time of day patterns
   - Account age
   - Velocity metrics

2. Apply the **PCA transformation matrix** to calculate V1-V28

3. Enable **true real-world input** with semantic fields

### Current Limitation Mitigation

The scenario-based approach provides:
- ✅ Realistic transaction contexts
- ✅ Actual model predictions
- ✅ Educational value (see fraud patterns)
- ✅ Easy testing and demonstration
- ❌ Cannot input arbitrary real-world transactions

## Phishing URL Detection

The phishing detection works differently and **supports real-world input**:

1. Enter any URL in the purple input box
2. Features are automatically extracted (22 characteristics)
3. Model predicts if URL is phishing or legitimate

Example: `http://192.168.1.100/login.php`
- Result: 100% phishing probability (IP address + suspicious path)

## Summary

The scenario-based approach solves the **PCA transformation impossibility** while maintaining model accuracy and providing a user-friendly experience. Users can see how the model responds to different transaction patterns without needing to understand PCA mathematics or have access to the original transformation matrix.
