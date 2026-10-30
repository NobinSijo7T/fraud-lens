import json
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, average_precision_score, balanced_accuracy_score,
                             confusion_matrix)
from backend.app.config import ARTIFACT_DIR, REPORT_DIR
from backend.app.services.dataset_service import load

STATUS = {'fraud': {'state': 'not_trained', 'selected_model': None, 'trained_at': None, 'error': None},
          'phishing': {'state': 'not_trained', 'selected_model': None, 'trained_at': None, 'error': None}}

def _key(name):
    return name.lower().replace(' ', '_')

def train(dataset_id='creditcard/creditcard.csv', task=None):
    task = task or ('phishing' if 'phishing' in dataset_id.lower() or 'url' in dataset_id.lower() else 'fraud')
    STATUS[task].update(state='training', error=None)
    prefix = f'{task}_'
    try:
        df = load(dataset_id).drop_duplicates().reset_index(drop=True)
        target = 'Class' if 'Class' in df.columns else next(c for c in df.columns if c.lower() in {'label', 'fraud', 'is_fraud', 'isfraud', 'target'})
        y, X = df[target].astype(int), df.drop(columns=[target])
        # Raw URL/domain strings are intentionally excluded from this first phishing model;
        # engineered URL statistics remain available as numeric signals.
        if task == 'phishing':
            X = X.select_dtypes(include='number')
        elif target.lower() == 'isfraud':
            # PaySim: expose fields a person can know at transaction time.
            # Account IDs and post-outcome flags are intentionally excluded.
            user_features = ['type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']
            X = X[[name for name in user_features if name in X.columns]]
            # The full PaySim file is ~500 MB. Keep every fraud row and a
            # representative legitimate sample for a practical local model.
            if len(X) > 250_000:
                positive = y == 1
                keep_positive = X.index[positive]
                keep_negative = X.index[~positive].to_series().sample(n=min(200_000, int((~positive).sum())), random_state=42)
                keep = keep_positive.union(keep_negative).sort_values()
                X, y = X.loc[keep], y.loc[keep]
        numeric = list(X.select_dtypes(include='number').columns)
        categorical = list(X.select_dtypes(exclude='number').columns)
        prep = ColumnTransformer([
            ('num', Pipeline([('impute', SimpleImputer(strategy='median')), ('scale', StandardScaler())]), numeric),
            ('cat', Pipeline([('impute', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore'))]), categorical)
        ], remainder='drop')
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
        models = {
            'Logistic Regression': LogisticRegression(max_iter=300, class_weight='balanced', solver='liblinear'),
            'Decision Tree': DecisionTreeClassifier(max_depth=12, class_weight='balanced', random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=120, n_jobs=-1, class_weight='balanced_subsample', random_state=42, max_depth=18)
        }
        results, best = {}, None
        for name, estimator in models.items():
            pipe = Pipeline([('preprocessor', prep), ('model', estimator)])
            pipe.fit(Xtr, ytr)
            pred = pipe.predict(Xte)
            prob = pipe.predict_proba(Xte)[:, 1] if hasattr(pipe, 'predict_proba') else None
            cm = confusion_matrix(yte, pred, labels=[0, 1]).tolist()
            metrics = {'model': name, 'accuracy': accuracy_score(yte, pred),
                       'precision': precision_score(yte, pred, zero_division=0),
                       'recall': recall_score(yte, pred, zero_division=0),
                       'f1_score': f1_score(yte, pred, zero_division=0),
                       'balanced_accuracy': balanced_accuracy_score(yte, pred),
                       'roc_auc': roc_auc_score(yte, prob) if prob is not None else None,
                       'pr_auc': average_precision_score(yte, prob) if prob is not None else None,
                       'false_positive_rate': cm[0][1] / sum(cm[0]) if sum(cm[0]) else 0,
                       'confusion_matrix': cm, 'test_samples': len(yte),
                       'class_counts': {str(k): int(v) for k, v in yte.value_counts().items()}}
            results[name] = metrics
            joblib.dump(pipe, ARTIFACT_DIR / f'{prefix}{_key(name)}.joblib')
            # For phishing, false positives are especially harmful for valid sites.
            # Prefer precision first, then F1, while keeping recall as a tie-breaker.
            score = (metrics['precision'], metrics['f1_score'], metrics['recall']) if task == 'phishing' else (metrics['f1_score'], metrics['precision'], metrics['recall'])
            best_score = ((best[1]['precision'], best[1]['f1_score'], best[1]['recall']) if task == 'phishing' else (best[1]['f1_score'], best[1]['precision'], best[1]['recall'])) if best else None
            if best is None or score > best_score:
                best = (name, metrics)
        selected = best[0]
        joblib.dump(joblib.load(ARTIFACT_DIR / f'{prefix}{_key(selected)}.joblib'), ARTIFACT_DIR / f'{prefix}selected_model.joblib')
        trained_at = pd.Timestamp.utcnow().isoformat()
        meta = {'task': task, 'dataset_id': dataset_id, 'target_column': target, 'features': list(X.columns),
                'numeric_features': numeric, 'categorical_features': categorical, 'selected_model': selected,
                'model_version': f'{task}_{_key(selected)}_v1', 'trained_at': trained_at}
        (ARTIFACT_DIR / f'{prefix}metadata.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
        report = {'generated_at': trained_at, 'task': task, 'dataset_id': dataset_id,
                  'target_column': target, 'selected_model': selected, 'models': results}
        (REPORT_DIR / f'{task}_model_evaluation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        # Keep the original fraud report names for backwards compatibility.
        if task == 'fraud':
            # The prediction service keeps this legacy filename for the
            # transaction endpoint; keep it synchronized with the new model.
            joblib.dump(joblib.load(ARTIFACT_DIR / f'{prefix}selected_model.joblib'), ARTIFACT_DIR / 'selected_model.joblib')
            (ARTIFACT_DIR / 'metadata.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
            (REPORT_DIR / 'model_evaluation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        STATUS[task].update(state='ready', selected_model=selected, trained_at=trained_at)
        return meta
    except Exception as exc:
        STATUS[task].update(state='error', error=str(exc))
        raise

def status(task=None):
    tasks = ('fraud', 'phishing') if task is None else (task,)
    for current in tasks:
        path = ARTIFACT_DIR / f'{current}_metadata.json'
        if current == 'fraud' and not path.exists(): path = ARTIFACT_DIR / 'metadata.json'
        if path.exists():
            data = json.loads(path.read_text())
            STATUS[current].update(state='ready', selected_model=data.get('selected_model'), trained_at=data.get('trained_at'))
    return STATUS if task is None else STATUS[task]

def metadata(task='fraud'):
    path = ARTIFACT_DIR / f'{task}_metadata.json'
    if task == 'fraud' and not path.exists(): path = ARTIFACT_DIR / 'metadata.json'
    return json.loads(path.read_text()) if path.exists() else None

def evaluation(task='fraud'):
    path = REPORT_DIR / f'{task}_model_evaluation.json'
    if task == 'fraud' and not path.exists(): path = REPORT_DIR / 'model_evaluation.json'
    return json.loads(path.read_text()) if path.exists() else None
