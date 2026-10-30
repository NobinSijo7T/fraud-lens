from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = (ROOT / os.getenv('DATASET_DIR', 'datasets')).resolve()
ARTIFACT_DIR = (ROOT / os.getenv('ARTIFACT_DIR', 'artifacts')).resolve()
REPORT_DIR = (ROOT / os.getenv('REPORT_DIR', 'reports')).resolve()
DATABASE_PATH = ROOT / os.getenv('DATABASE_PATH', 'app.db')
ORIGIN = os.getenv('FRONTEND_ORIGIN', 'http://localhost:8000')
for path in (ARTIFACT_DIR, REPORT_DIR): path.mkdir(parents=True, exist_ok=True)
