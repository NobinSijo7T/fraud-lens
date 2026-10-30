# How to Use Phishing URL Detection

## Two Ways to Check URLs

When you select "Phishing URL" on the Analyze page, you have **two options**:

---

## 🚀 Option 1: Quick URL Analysis (Recommended)

**Best for:** Most users, quick checks, real-world URLs

### Steps:
1. **Paste your URL** in the purple box at the top
   ```
   Example: http://192.168.1.100/login.php
   ```

2. **Click "Extract Features"**
   - All 22 feature fields below will be automatically filled
   - Takes less than 5 seconds

3. **Click "Run risk assessment"**
   - Get instant phishing prediction

### Why use this?
- ✅ **Fast** - Takes 5 seconds total
- ✅ **Easy** - No technical knowledge needed
- ✅ **Accurate** - Automatic calculation prevents errors
- ✅ **Practical** - Works with any real URL

---

## 🔧 Option 2: Manual Feature Entry (Advanced)

**Best for:** Researchers, testing specific values, educational purposes

### When to use manual entry:
- You want to test specific feature combinations
- You're researching how features affect predictions
- You have pre-calculated feature values
- You're testing edge cases

### The 22 Features You Need to Enter:

#### Length Metrics
1. **url_len** - Total URL length (characters)
2. **dom_len** - Domain name length
3. **tld_len** - Top-level domain length (.com = 3)
4. **path_len** - Path length (/login/page = 11)
5. **query_len** - Query string length

#### Domain Analysis
6. **is_ip** - Is domain an IP address? (0=no, 1=yes)
7. **subdom_cnt** - Number of subdomains

#### Character Counts
8. **letter_cnt** - Total letters
9. **digit_cnt** - Total digits
10. **special_cnt** - Total special characters

#### Character Ratios (0.0 to 1.0)
11. **letter_ratio** - Letters / total characters
12. **digit_ratio** - Digits / total characters
13. **spec_ratio** - Special chars / total characters

#### Special Character Counts
14. **eq_cnt** - Number of '=' characters
15. **qm_cnt** - Number of '?' characters
16. **amp_cnt** - Number of '&' characters
17. **dot_cnt** - Number of '.' characters
18. **dash_cnt** - Number of '-' characters
19. **under_cnt** - Number of '_' characters
20. **slash_cnt** - Number of '/' characters

#### Security & Complexity
21. **is_https** - Uses HTTPS? (0=no, 1=yes)
22. **entropy** - Shannon entropy (randomness, typically 3.0-5.0)

---

## 📊 Example: Legitimate URL

Let's analyze: `https://www.github.com/user/repo`

### Option 1 (Quick):
```
Paste: https://www.github.com/user/repo
Click: Extract Features
Result: All 22 fields auto-filled in 5 seconds
```

### Option 2 (Manual):
```
url_len: 34
dom_len: 10
is_ip: 0
tld_len: 3
subdom_cnt: 1
letter_cnt: 28
digit_cnt: 0
special_cnt: 6
eq_cnt: 0
qm_cnt: 0
amp_cnt: 0
dot_cnt: 2
dash_cnt: 0
under_cnt: 1
letter_ratio: 0.823529
digit_ratio: 0.0
spec_ratio: 0.176471
is_https: 1
slash_cnt: 3
entropy: 3.90
path_len: 10
query_len: 0
```

**Both give same result:** ✅ Legitimate, Low Risk

---

## ⚠️ Example: Phishing URL

Let's analyze: `http://192.168.1.100/login.php`

### Option 1 (Quick):
```
Paste: http://192.168.1.100/login.php
Click: Extract Features
Result: Phishing detected! (100% confidence)
Red flags shown: IP address, no HTTPS
```

### Option 2 (Manual):
```
url_len: 31
dom_len: 13
is_ip: 1        ← RED FLAG!
tld_len: 3
subdom_cnt: 0
letter_cnt: 17
digit_cnt: 7
special_cnt: 7
eq_cnt: 0
qm_cnt: 0
amp_cnt: 0
dot_cnt: 3
dash_cnt: 0
under_cnt: 0
letter_ratio: 0.548387
digit_ratio: 0.225806
spec_ratio: 0.225806
is_https: 0     ← RED FLAG!
slash_cnt: 2
entropy: 4.53   ← RED FLAG!
path_len: 10
query_len: 0
```

**Both give same result:** ⚠️ Phishing, High Risk

---

## 🤔 Why Are the Number Fields Still There?

Good question! Here's why:

### Reason 1: Flexibility
- Some users prefer manual control
- Researchers want to test specific values
- Advanced users may want to edit extracted values

### Reason 2: Transparency
- Shows exactly what features the model uses
- Educational - learn what makes a URL suspicious
- Verifiable - see the numbers that led to the prediction

### Reason 3: Edge Cases
- Pre-calculated feature datasets
- Testing model behavior
- Integration with other tools that generate features

---

## 💡 Best Practices

### For Regular Users:
1. **Always use Option 1** (Quick URL Analysis)
2. Paste the full URL including http:// or https://
3. Don't edit the extracted features unless you know what you're doing
4. Trust the automatic extraction - it's more accurate than manual entry

### For Researchers/Developers:
1. Use Option 1 to verify your calculations
2. Use Option 2 to test specific hypotheses
3. Compare automatic vs manual to understand feature extraction
4. Document any custom feature values you test

---

## 🎯 Common Use Cases

### Use Case 1: Suspicious Email Link
```
Scenario: Received email with suspicious link
Method: Option 1 (Quick URL Analysis)
Time: 10 seconds
Result: Phishing detected, email deleted
```

### Use Case 2: Testing Model Behavior
```
Scenario: Research how entropy affects predictions
Method: Option 2 (Manual Entry)
Process: Test entropy values from 3.0 to 5.0
Result: Find threshold where prediction flips
```

### Use Case 3: Batch URL Analysis
```
Scenario: Check 100 URLs from security scan
Method: Use API with Option 1 logic
Code: Python script calling /api/v1/analyze/url
Result: Automated report of all phishing URLs
```

---

## ❓ FAQ

**Q: Do I need to understand the 22 features?**
A: No! Just use Option 1 (Quick URL Analysis). Paste the URL and click.

**Q: What if I want to learn about the features?**
A: Use Option 1, then look at the extracted values below. The guide explains each one.

**Q: Can I edit the automatically extracted features?**
A: Yes, but it's not recommended unless you're testing something specific.

**Q: Why do some fields show decimal numbers?**
A: Features like entropy, letter_ratio are calculated values with decimals.

**Q: Which option is more accurate?**
A: Both are equally accurate if values are correct. Option 1 prevents manual errors.

**Q: Can I use Option 1 for any URL?**
A: Yes! It works with any format: http, https, with/without www, IP addresses, etc.

---

## 🚀 Quick Start (5 Seconds)

1. Go to: http://127.0.0.1:8000/pages/analyze.html
2. Select: **"Phishing URL"** from dropdown
3. Paste: Any suspicious URL in the purple box
4. Click: **"Extract Features"**
5. Click: **"Run risk assessment"**
6. Done! ✅

---

## 📖 Summary

| Aspect | Option 1: Quick | Option 2: Manual |
|--------|-----------------|------------------|
| **Time** | 5 seconds | 5-10 minutes |
| **Difficulty** | Easy | Requires understanding |
| **Accuracy** | High (automated) | High (if correct) |
| **Use Case** | Real-world URLs | Research/testing |
| **Recommended For** | Everyone | Advanced users |

**Bottom Line:** Use Option 1 unless you have a specific reason to use Option 2.

The numeric fields are there for transparency and advanced use, but **most users should ignore them** and just use the URL input box! 🎉
