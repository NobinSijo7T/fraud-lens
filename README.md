# FraudLens — Digital Scam and Fraud Analysis

FraudLens is a FastAPI + vanilla HTML/CSS/JavaScript dashboard for inspecting datasets, training both transaction fraud and phishing URL detection models, and storing real prediction results in SQLite.

## What was discovered

- `datasets/creditcard.csv`: 284,807 rows, 30 numeric input features, target `Class`; 284,315 legitimate and 492 fraud records. This is the selected transaction dataset.
- `datasets/phishing_links_url/Dataset.csv`: 116,600 rows, target `label`, with 14 missing `tld` values and 1,369 duplicate records. It is documented separately because it is a phishing URL task, not a compatible transaction schema.

The generated inspection report is `reports/dataset_inspection.json`. Original datasets are never modified.

## Training datasets

The datasets are intentionally excluded from Git because of their size. Download them from the links below and place the extracted files at the indicated paths:

| Dataset | Direct download | Expected project path |
| --- | --- | --- |
| Credit Card Fraud | [Download from Kaggle](https://www.kaggle.com/api/v1/datasets/download/mlg-ulb/creditcardfraud) | `datasets/creditcard/creditcard.csv` |
| PaySim mobile-money transactions | [Download from Kaggle](https://www.kaggle.com/api/v1/datasets/download/ealaxi/paysim1) | `datasets/paysim/PS_20174392719_1491204439457_log.csv` |
| URL-Phish phishing URLs | [Download Dataset.csv](https://raw.githubusercontent.com/SamarthGarge/Phishing_URL_Detection/main/Dataset.csv) | `datasets/phishing_links_url/Dataset.csv` |

Kaggle downloads are ZIP archives; extract the CSV file into the expected directory. Kaggle may require you to sign in before downloading.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Open http://127.0.0.1:8000. The API documentation is available at `/docs`.

The trained artifacts and actual held-out evaluation are already generated in `artifacts/` and `reports/`. To retrain models:

**Transaction Fraud Model:**
```powershell
python -c "from backend.app.services.training_service import train; print(train('creditcard.csv'))"
```

**Phishing URL Detection Model:**
```powershell
python train_phishing_model.py
# Or use the API:
python -c "from backend.app.services.training_service import train; print(train('phishing_links_url/Dataset.csv', task='phishing'))"
```

## API

All API endpoints use `/api/v1`: health, datasets, dataset summaries, model training/status/evaluation, dashboard, transaction prediction, phishing prediction, and paginated prediction history.

Key endpoints:
- `/api/v1/predict/transaction` - Predict transaction fraud
- `/api/v1/predict/phishing` - Predict phishing URLs
- `/api/v1/models/evaluation?task=fraud` - Get fraud model metrics
- `/api/v1/models/evaluation?task=phishing` - Get phishing model metrics

The prediction endpoints validate the model feature schema, return a model probability when supported, assign documented Low/Medium/High thresholds (below .30, .30–.69, and .70+), and include a risk-assessment disclaimer.

## Features

### Transaction Fraud Detection
- Trained on creditcard.csv dataset (284,807 transactions)
- Uses 28 anonymized features (V1-V28), Time, and Amount
- Three models: Logistic Regression, Decision Tree, Random Forest
- Achieves 96%+ accuracy with high recall

### Phishing URL Detection
- Trained on phishing_links_url dataset (116,600 URLs)
- Uses 22 URL-based features (length, domain, special characters, entropy, etc.)
- Three models: Logistic Regression, Decision Tree, Random Forest
- Achieves 96%+ accuracy with 93% recall

### Frontend Features
- **Dashboard**: Overview of datasets and model status
- **Analyze**: Test predictions for both fraud and phishing
- **Datasets**: View dataset details and train models
- **Evaluation**: Compare model performance metrics
- **History**: Browse and manage past predictions
