import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database import SessionLocal
from api.models import Acupoint

def check_acupoints():
    db = SessionLocal()
    count = db.query(Acupoint).count()
    print(f"Total Acupoints in DB: {count}")
    
    # List first 5
    print("Sample Acupoints:")
    for p in db.query(Acupoint).limit(5).all():
        print(f"- {p.name} ({p.code}): {p.meridian}")

if __name__ == "__main__":
    check_acupoints()
