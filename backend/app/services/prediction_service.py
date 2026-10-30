import json, sqlite3
from datetime import datetime, timezone
import joblib, pandas as pd
from backend.app.config import ARTIFACT_DIR, DATABASE_PATH
from backend.app.services.training_service import metadata

def init_db():
    with sqlite3.connect(DATABASE_PATH) as c: c.execute('CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT, payload TEXT, result TEXT)')
def predict(payload, task='fraud'):
    meta=metadata(task)
    if not meta: raise RuntimeError('No trained model is available. Train a model first.')
    missing=[f for f in meta['features'] if f not in payload]
    if missing: raise ValueError('Missing required fields: '+', '.join(missing))
    model_file = ARTIFACT_DIR / ('selected_model.joblib' if task == 'fraud' else f'{task}_selected_model.joblib')
    model=joblib.load(model_file); row={k:payload[k] for k in meta['features']}; pred=int(model.predict(pd.DataFrame([row]))[0]); prob=float(model.predict_proba(pd.DataFrame([row]))[0][1]) if hasattr(model,'predict_proba') else None
    risk='High' if prob is not None and prob>=.7 else ('Medium' if prob is not None and prob>=.3 else 'Low')
    result={'prediction':('Phishing' if pred else 'Legitimate') if task == 'phishing' else ('Fraud' if pred else 'Legitimate'),'is_fraud':pred,'fraud_probability':prob,'risk_level':risk,'contributing_factors':[],'model_version':meta['model_version'],'task':task,'disclaimer':'This prediction is a risk assessment, not proof of fraud.'}
    init_db(); created=datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(DATABASE_PATH) as c: cur=c.execute('INSERT INTO predictions(created_at,payload,result) VALUES (?,?,?)',(created,json.dumps(payload),json.dumps(result))); ident=cur.lastrowid
    result['prediction_id']=ident; result['created_at']=created; return result
def history(page=1,page_size=20):
    init_db(); offset=(page-1)*page_size
    with sqlite3.connect(DATABASE_PATH) as c:
        total=c.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]; rows=c.execute('SELECT id,created_at,result FROM predictions ORDER BY id DESC LIMIT ? OFFSET ?',(page_size,offset)).fetchall()
    return {'items':[{'prediction_id':r[0],'created_at':r[1],**json.loads(r[2])} for r in rows],'page':page,'page_size':page_size,'total':total}
def detail(ident):
    init_db()
    with sqlite3.connect(DATABASE_PATH) as c: r=c.execute('SELECT id,created_at,payload,result FROM predictions WHERE id=?',(ident,)).fetchone()
    if not r: return None
    return {'prediction_id':r[0],'created_at':r[1],'payload':json.loads(r[2]),**json.loads(r[3])}
def delete(ident):
    with sqlite3.connect(DATABASE_PATH) as c: return c.execute('DELETE FROM predictions WHERE id=?',(ident,)).rowcount>0
