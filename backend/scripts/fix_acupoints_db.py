#!/usr/bin/env python3
"""
Fix Acupoints Database
修复穴位数据库问题 - 重新创建数据库
"""
import sys
import os
from pathlib import Path
import glob

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from api.database import engine, SessionLocal, Base
from api.models import Acupoint
from api.data.acupoints_comprehensive import ACUPOINTS_DATA


def fix_database():
    """Fix the database by recreating it from scratch"""
    print("=" * 50)
    print("[+] Fixing Acupoints Database")
    print("=" * 50)

    # Step 1: Find and delete all database files
    print("\n[1] Finding database files...")
    db_files = glob.glob(str(Path(__file__).parent.parent / "*.db"))
    db_files += glob.glob(str(Path(__file__).parent.parent / "*.db-*"))
    print(f"   Found {len(db_files)} database files")

    for db_file in db_files:
        try:
            os.remove(db_file)
            print(f"   [OK] Deleted: {db_file}")
        except Exception as e:
            print(f"   [WARN] Could not delete {db_file}: {e}")

    # Step 2: Drop and recreate acupoints table with fresh schema
    print("\n[2] Dropping and recreating acupoints table...")
    Acupoint.__table__.drop(engine, checkfirst=True)
    Acupoint.__table__.create(engine, checkfirst=True)
    print("   [OK] Acupoints table created successfully")

    # Step 3: Seed acupoints data
    print("\n[3] Seeding acupoints data...")
    db = SessionLocal()

    try:
        count = 0
        for a_data in ACUPOINTS_DATA:
            acupoint = Acupoint(
                name=a_data["name"],
                code=a_data["code"],
                meridian=a_data["meridian"],
                body_part=a_data["body_part"],
                location=a_data["location"],
                simple_location=a_data["simple_location"],
                efficacy=a_data["efficacy"],
                indications=a_data["indications"],
                massage_method=a_data["massage_method"],
                image_url=a_data["image_url"],
                anatomical_image_url=a_data.get("anatomical_image_url"),
                model_3d_url=a_data.get("model_3d_url", "")
            )
            db.add(acupoint)
            count += 1

        db.commit()
        print(f"   [OK] Seeded {count} acupoints")

        # Verify
        total = db.query(Acupoint).count()
        print(f"   [OK] Verified: {total} acupoints in database")

        # Show sample
        sample = db.query(Acupoint).limit(3).all()
        print("\n   Sample acupoints:")
        for a in sample:
            print(f"      - {a.code} {a.name} ({a.meridian})")

    except Exception as e:
        print(f"\n   [ERROR] Failed to seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

    print("\n" + "=" * 50)
    print("[OK] Database fix completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    fix_database()
