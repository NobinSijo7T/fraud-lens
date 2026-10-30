from pathlib import Path
import json, hashlib
import pandas as pd
from backend.app.config import DATASET_DIR, REPORT_DIR

SUPPORTED = {'.csv', '.parquet', '.json'}
TARGET_HINTS = {'is_fraud','isfraud','fraud','class','label','target'}

def inventory():
    items=[]
    if not DATASET_DIR.exists(): return items
    for p in DATASET_DIR.rglob('*'):
        if p.is_file() and p.suffix.lower() in SUPPORTED:
            rel=p.relative_to(DATASET_DIR).as_posix()
            try:
                df=load(rel)
                targets=[c for c in df.columns if c.lower() in TARGET_HINTS]
                dist={str(k):int(v) for k,v in df[targets[0]].value_counts(dropna=False).items()} if targets else {}
                items.append(summary(rel, df, targets, dist))
            except Exception as e:
                items.append({'id':rel,'filename':p.name,'file_format':p.suffix.lower()[1:],'error':str(e)})
    return items

def safe_path(dataset_id):
    root=DATASET_DIR.resolve(); p=(root / dataset_id).resolve()
    if root not in p.parents or p.suffix.lower() not in SUPPORTED or not p.is_file(): raise ValueError('Unknown dataset')
    return p

def load(dataset_id):
    p=safe_path(dataset_id)
    if p.suffix.lower()=='.csv': return pd.read_csv(p)
    if p.suffix.lower()=='.parquet': return pd.read_parquet(p)
    return pd.read_json(p)

def summary(dataset_id, df=None, targets=None, dist=None):
    if df is None: df=load(dataset_id)
    targets=targets if targets is not None else [c for c in df.columns if c.lower() in TARGET_HINTS]
    dist=dist if dist is not None else ({str(k):int(v) for k,v in df[targets[0]].value_counts(dropna=False).items()} if targets else {})
    return {'id':dataset_id,'dataset_filename':Path(dataset_id).name,'file_format':Path(dataset_id).suffix.lower()[1:],'row_count':len(df),'column_count':len(df.columns),'column_names':list(df.columns),'column_data_types':{c:str(t) for c,t in df.dtypes.items()},'missing_value_counts':{c:int(v) for c,v in df.isna().sum().items() if v},'duplicate_count':int(df.duplicated().sum()),'candidate_target_columns':targets,'target_column':targets[0] if targets else None,'target_class_distribution':dist,'dataset_purpose':'Transaction fraud detection' if 'creditcard' in dataset_id.lower() or 'isfraud' in ' '.join(df.columns).lower() else ('Phishing URL detection' if 'phish' in dataset_id.lower() or 'url' in dataset_id.lower() else 'Unknown'),'selected_for_training':dataset_id=='creditcard.csv','selection_reason':'Selected as the primary transaction fraud dataset with real-world transaction fields.' if 'isfraud' in ' '.join(df.columns).lower() else ('Selected as the primary transaction fraud dataset with verified binary Class labels.' if dataset_id=='creditcard.csv' else 'Kept as a separate phishing URL classification dataset; schema and prediction target differ.'),'data_quality_warnings':(['Missing values present'] if df.isna().any().any() else []) + (['Exact duplicates present'] if df.duplicated().any() else [])}

def write_report():
    data=inventory(); (REPORT_DIR/'dataset_inspection.json').write_text(json.dumps({'generated_at':pd.Timestamp.utcnow().isoformat(),'datasets':data},indent=2),encoding='utf-8'); return data
