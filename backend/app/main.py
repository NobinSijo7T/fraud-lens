from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any
from backend.app.config import ORIGIN
from backend.app.services import dataset_service, training_service, prediction_service
from backend.app.services.url_feature_extractor import extract_features, is_trusted_domain

app=FastAPI(title='Digital Scam and Fraud Analysis',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=[ORIGIN,'http://127.0.0.1:8000'],allow_methods=['*'],allow_headers=['*'])
class DatasetSelect(BaseModel): dataset_id: str = Field(min_length=1,max_length=255)
class TrainRequest(BaseModel): dataset_id: str = 'creditcard/creditcard.csv'
class Transaction(BaseModel): data: Dict[str,Any]
class URLAnalysis(BaseModel): url: str = Field(min_length=1,max_length=2048)

@app.get('/api/v1/health')
def health(): return {'status':'ok','models':training_service.status()}
@app.get('/api/v1/datasets')
def datasets(): return {'items':dataset_service.inventory()}
@app.get('/api/v1/datasets/{dataset_id:path}/summary')
def summary(dataset_id:str):
    try:return dataset_service.summary(dataset_id)
    except ValueError as e: raise HTTPException(404,str(e))
@app.post('/api/v1/datasets/select')
def select(req:DatasetSelect):
    try:
        s=dataset_service.summary(req.dataset_id); return {'selected_dataset':s['id'],'summary':s}
    except ValueError as e: raise HTTPException(404,str(e))
@app.post('/api/v1/models/train')
def train(req:TrainRequest):
    try:return training_service.train(req.dataset_id)
    except Exception as e: raise HTTPException(400,f'Training failed: {e}')
@app.get('/api/v1/models/status')
def model_status(): return training_service.status()
@app.get('/api/v1/models/features')
def model_features(task:str='fraud'):
    if task not in ('fraud','phishing'): raise HTTPException(400,'Unsupported model task')
    meta=training_service.metadata(task)
    if not meta: raise HTTPException(404,f'{task.capitalize()} model not trained yet')
    descriptions={
        'step':('number','Hours since the start of the simulation'),
        'type':('select','Transaction type: CASH_IN, CASH_OUT, DEBIT, PAYMENT, or TRANSFER'),
        'amount':('number','Transaction amount'),
        'oldbalanceOrg':('number','Sender balance before the transaction'),
        'newbalanceOrig':('number','Sender balance after the transaction'),
        'oldbalanceDest':('number','Receiver balance before the transaction'),
        'newbalanceDest':('number','Receiver balance after the transaction'),
    }
    features_list=[{'name':f,'type':descriptions.get(f,('number',f'Feature {f}'))[0],'required':True,'description':descriptions.get(f,('number',f'Feature {f}'))[1]} for f in meta['features']]
    note='PaySim transaction fields' if meta.get('target_column','').lower() == 'isfraud' else 'Legacy anonymized transaction features'
    return {'task':task,'model_name':meta.get('selected_model'),'model_version':meta.get('model_version'),'target_name':meta.get('target_column'),'features':features_list,'note':note}
@app.get('/api/v1/models/evaluation')
def model_evaluation(task:str='fraud'):
    if task not in ('fraud','phishing'): raise HTTPException(400,'Unsupported model task')
    data=training_service.evaluation(task)
    if not data: raise HTTPException(404,'Training or evaluation has not completed.')
    return data
@app.get('/api/v1/analysis/dashboard')
def dashboard():
    sets=dataset_service.inventory(); ev=training_service.evaluation('fraud'); st=training_service.status('fraud'); fraud_meta=training_service.metadata('fraud') or {}; primary=next((x for x in sets if x.get('id')==fraud_meta.get('dataset_id')),sets[0] if sets else {})
    meta=training_service.metadata('fraud') or {}
    return {'dataset':primary,'datasets':sets,'model_status':{**st,'features':meta.get('features',[])},'selected_model':ev.get('selected_model') if ev else None,'evaluation':ev.get('models',{}).get(ev.get('selected_model')) if ev else None,'recent_predictions':prediction_service.history(1,5)['items']}
@app.post('/api/v1/predict/transaction')
def predict(req:Transaction):
    try:return prediction_service.predict(req.data)
    except RuntimeError as e: raise HTTPException(503,str(e))
    except ValueError as e: raise HTTPException(422,str(e))
@app.post('/api/v1/predict/phishing')
def predict_phishing(req:Transaction):
    try:return prediction_service.predict(req.data, 'phishing')
    except RuntimeError as e: raise HTTPException(503,str(e))
    except ValueError as e: raise HTTPException(422,str(e))
@app.post('/api/v1/analyze/url')
def analyze_url(req:URLAnalysis):
    try:
        features=extract_features(req.url)
        result=prediction_service.predict(features, 'phishing')
        if is_trusted_domain(req.url):
            result.update({'prediction':'Legitimate','is_fraud':0,'fraud_probability':0.01,'risk_level':'Low'})
            result['contributing_factors']=['Exact trusted-domain safeguard applied']
        elif features.get('is_ip'):
            result.update({'prediction':'Phishing','is_fraud':1,'fraud_probability':max(result.get('fraud_probability') or 0, 0.95),'risk_level':'High'})
            result['contributing_factors']=['Host is an IP address rather than a domain name']
        result['url']=req.url
        result['extracted_features']=features
        return result
    except RuntimeError as e: raise HTTPException(503,str(e))
    except Exception as e: raise HTTPException(400,f'URL analysis failed: {e}')
@app.get('/api/v1/predictions')
def predictions(page:int=Query(1,ge=1),page_size:int=Query(20,ge=1,le=100)): return prediction_service.history(page,page_size)
@app.get('/api/v1/predictions/{ident}')
def prediction(ident:int):
    value=prediction_service.detail(ident)
    if not value: raise HTTPException(404,'Prediction not found')
    return value
@app.delete('/api/v1/predictions/{ident}')
def remove_prediction(ident:int):
    if not prediction_service.delete(ident): raise HTTPException(404,'Prediction not found')
    return {'deleted':True}

FRONTEND_DIR=Path(__file__).resolve().parents[2] / 'frontend'
if FRONTEND_DIR.exists():
    app.mount('/', StaticFiles(directory=FRONTEND_DIR, html=True), name='frontend')
