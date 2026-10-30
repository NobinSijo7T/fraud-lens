# Phishing URL Detection Guide

## Overview

The phishing detection system analyzes URL characteristics to predict whether a URL is legitimate or potentially phishing. The model is trained on 116,600 URLs with 22 engineered features.

## Features Used

The model analyzes these URL characteristics:

### Length & Structure
- `url_len` - Total URL length
- `dom_len` - Domain length
- `path_len` - Path length
- `query_len` - Query string length

### Domain Analysis
- `is_ip` - Whether domain is an IP address (0/1)
- `tld_len` - Top-level domain length
- `subdom_cnt` - Number of subdomains

### Character Composition
- `letter_cnt` - Number of letters
- `digit_cnt` - Number of digits
- `special_cnt` - Number of special characters
- `letter_ratio` - Proportion of letters
- `digit_ratio` - Proportion of digits
- `spec_ratio` - Proportion of special characters

### Special Character Counts
- `eq_cnt` - Number of '=' characters
- `qm_cnt` - Number of '?' characters
- `amp_cnt` - Number of '&' characters
- `dot_cnt` - Number of '.' characters
- `dash_cnt` - Number of '-' characters
- `under_cnt` - Number of '_' characters
- `slash_cnt` - Number of '/' characters

### Security & Complexity
- `is_https` - Whether URL uses HTTPS (0/1)
- `entropy` - Shannon entropy (randomness measure)

## Using the Frontend

### Step 1: Train the Model (if not already trained)

1. Navigate to the **Datasets** page
2. Find the "phishing_links_url/Dataset.csv" card
3. Click **"Train phishing models →"**
4. Wait for training to complete (~30-60 seconds)

### Step 2: Analyze URLs

1. Navigate to the **Analyze** page
2. Select **"Phishing URL"** from the dropdown
3. Enter the 22 feature values for your URL
4. Click **"Run risk assessment"**

### Step 3: View Results

The result will show:
- **Prediction**: Legitimate or Phishing
- **Risk Level**: Low, Medium, or High
- **Probability**: Confidence score (0-100%)
- **Disclaimer**: Risk assessment notice

## Using the API

### Train the Model

```bash
POST /api/v1/models/train
Content-Type: application/json

{
  "dataset_id": "phishing_links_url/Dataset.csv"
}
```

### Make Predictions

```bash
POST /api/v1/predict/phishing
Content-Type: application/json

{
  "data": {
    "url_len": 24,
    "dom_len": 11,
    "is_ip": 0,
    "tld_len": 6,
    "subdom_cnt": 1,
    "letter_cnt": 17,
    "digit_cnt": 0,
    "special_cnt": 7,
    "eq_cnt": 0,
    "qm_cnt": 0,
    "amp_cnt": 0,
    "dot_cnt": 3,
    "dash_cnt": 0,
    "under_cnt": 0,
    "letter_ratio": 0.708333,
    "digit_ratio": 0.0,
    "spec_ratio": 0.291667,
    "is_https": 1,
    "slash_cnt": 3,
    "entropy": 3.709148,
    "path_len": 1,
    "query_len": 0
  }
}
```

**Response:**
```json
{
  "prediction": "Legitimate",
  "is_fraud": 0,
  "fraud_probability": 0.0026,
  "risk_level": "Low",
  "contributing_factors": [],
  "model_version": "phishing_decision_tree_v1",
  "task": "phishing",
  "disclaimer": "This prediction is a risk assessment, not proof of fraud.",
  "prediction_id": 123,
  "created_at": "2026-10-29T17:40:50.177812+00:00"
}
```

### Check Model Status

```bash
GET /api/v1/models/status
```

**Response:**
```json
{
  "fraud": {
    "state": "ready",
    "selected_model": "Random Forest",
    "trained_at": "2026-10-29T17:30:00.000000+00:00",
    "error": null
  },
  "phishing": {
    "state": "ready",
    "selected_model": "Decision Tree",
    "trained_at": "2026-10-29T17:40:50.177812+00:00",
    "error": null
  }
}
```

### View Evaluation Metrics

```bash
GET /api/v1/models/evaluation?task=phishing
```

**Response includes:**
- Accuracy, Precision, Recall, F1 Score
- ROC AUC, PR AUC
- Confusion matrix
- Balanced accuracy
- False positive rate

## Model Performance

The phishing detection model achieves:
- **Accuracy**: ~96.5%
- **Precision**: ~84%
- **Recall**: ~93% (catches 93% of phishing URLs)
- **F1 Score**: ~89%
- **ROC AUC**: ~97%

## Interpreting Results

### Risk Levels
- **Low Risk**: Probability < 30% - Likely legitimate
- **Medium Risk**: Probability 30-69% - Suspicious, investigate further
- **High Risk**: Probability ≥ 70% - Likely phishing

### Red Flags
URLs with these characteristics are more likely to be phishing:
- Uses IP address instead of domain name (`is_ip = 1`)
- No HTTPS (`is_https = 0`)
- Very long URL or domain
- Many special characters
- High entropy (random-looking)
- Many subdomains
- Unusual TLD length

## Python Usage

```python
from backend.app.services import training_service, prediction_service

# Train the model
training_service.train('phishing_links_url/Dataset.csv', task='phishing')

# Make a prediction
url_features = {
    'url_len': 24,
    'dom_len': 11,
    'is_ip': 0,
    # ... other features
}

result = prediction_service.predict(url_features, task='phishing')
print(f"Prediction: {result['prediction']}")
print(f"Risk: {result['risk_level']}")
print(f"Probability: {result['fraud_probability']:.2%}")
```

## Notes

- All predictions are stored in the database and can be viewed in the History page
- The model uses only engineered numeric features, not raw URL strings
- Training takes ~30-60 seconds depending on your system
- Three models are trained (Logistic Regression, Decision Tree, Random Forest)
- The best-performing model is automatically selected based on recall and F1 score
