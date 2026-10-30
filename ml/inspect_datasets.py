import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.app.services.dataset_service import write_report
if __name__=='__main__': print(write_report())
