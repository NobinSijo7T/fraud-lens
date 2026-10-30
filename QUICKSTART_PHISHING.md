# Quick Start: Phishing URL Detection

## ✅ Model Already Trained!

The phishing detection model is already trained and ready to use with:
- **Dataset**: 116,600 URLs
- **Model**: Decision Tree
- **Accuracy**: 96.54%
- **Recall**: 93.34%

## 🚀 Start Using It Now

### 1. Start the Server
```powershell
python run.py
```

### 2. Open the Web Interface
Navigate to: **http://127.0.0.1:8000**

### 3. Analyze a URL

1. Click **"Analyze"** in the navigation
2. Select **"Phishing URL"** from the dropdown
3. Enter the 22 URL features (see examples below)
4. Click **"Run risk assessment"**

## 📊 Example: Legitimate URL

```
url_len: 24
dom_len: 11
is_ip: 0
tld_len: 6
subdom_cnt: 1
letter_cnt: 17
digit_cnt: 0
special_cnt: 7
eq_cnt: 0
qm_cnt: 0
amp_cnt: 0
dot_cnt: 3
dash_cnt: 0
under_cnt: 0
letter_ratio: 0.708333
digit_ratio: 0
spec_ratio: 0.291667
is_https: 1
slash_cnt: 3
entropy: 3.709148
path_len: 1
query_len: 0
```

**Expected Result**: Legitimate, Low Risk

## 📊 Example: Suspicious URL

```
url_len: 85
dom_len: 25
is_ip: 1 (← Red flag: IP address)
tld_len: 3
subdom_cnt: 5 (← Red flag: many subdomains)
letter_cnt: 45
digit_cnt: 15
special_cnt: 25
eq_cnt: 3
qm_cnt: 2
amp_cnt: 4
dot_cnt: 8
dash_cnt: 5
under_cnt: 3
letter_ratio: 0.529412
digit_ratio: 0.176471
spec_ratio: 0.294118
is_https: 0 (← Red flag: no HTTPS)
slash_cnt: 6
entropy: 4.85 (← Red flag: high randomness)
path_len: 35
query_len: 25
```

**Expected Result**: Higher risk probability

## 🔧 API Usage

### Check Model Status
```bash
curl http://127.0.0.1:8000/api/v1/models/status
```

### Make a Prediction
```bash
curl -X POST http://127.0.0.1:8000/api/v1/predict/phishing \
  -H "Content-Type: application/json" \
  -d '{"data": {"url_len": 24, "dom_len": 11, ...}}'
```

### View Evaluation Metrics
```bash
curl http://127.0.0.1:8000/api/v1/models/evaluation?task=phishing
```

## 📖 More Information

- **Full Guide**: See `PHISHING_DETECTION_GUIDE.md`
- **API Docs**: http://127.0.0.1:8000/docs (when server is running)
- **Retrain**: `python train_phishing_model.py`
- **Test**: `python test_phishing_prediction.py`

## 🎯 Key Features to Watch

Phishing URLs often have:
- ✗ IP address instead of domain (`is_ip = 1`)
- ✗ No HTTPS (`is_https = 0`)
- ✗ Very long URLs (`url_len > 75`)
- ✗ Many subdomains (`subdom_cnt > 3`)
- ✗ High entropy (`entropy > 4.5`)
- ✗ Many special characters
- ✗ Unusual TLD length

## 📱 Frontend Features

- **Dashboard**: See model status and recent predictions
- **Analyze**: Test individual URLs (fraud or phishing)
- **Datasets**: View dataset details and retrain models
- **Evaluation**: Compare model performance
- **History**: Browse all past predictions

---

**Ready to go!** Just run `python run.py` and start analyzing URLs. 🚀
