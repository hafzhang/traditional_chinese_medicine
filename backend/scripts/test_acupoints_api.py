#!/usr/bin/env python3
"""
Test Acupoints API
测试穴位API - 确保后端正常工作
"""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database import SessionLocal
from api.models import Acupoint


def test_database():
    """Test database connection and data"""
    print("=" * 50)
    print("[1] Testing Database Connection")
    print("=" * 50)

    db = SessionLocal()
    try:
        # Count acupoints
        count = db.query(Acupoint).count()
        print(f"   [OK] Database connected")
        print(f"   [OK] Found {count} acupoints")

        # Test meridian list
        meridians = db.query(Acupoint.meridian).distinct().all()
        meridian_list = [m[0] for m in meridians if m[0]]
        print(f"   [OK] Found {len(meridian_list)} meridians")

        # Test getting acupoints
        acupoints = db.query(Acupoint).limit(3).all()
        print(f"   [OK] Sample acupoints:")
        for a in acupoints:
            print(f"      - {a.code} {a.name}")

        # Format response as API would
        print("\n" + "=" * 50)
        print("[2] API Response Format Test")
        print("=" * 50)

        # Test meridian list response
        meridian_response = {
            "code": 0,
            "message": "success",
            "data": [{"value": m, "label": m} for m in meridian_list]
        }
        print("GET /api/v1/acupoints/meridians/list")
        print(json.dumps(meridian_response, ensure_ascii=False, indent=2)[:500] + "...")

        # Test acupoints list response
        acupoints_data = db.query(Acupoint).order_by(Acupoint.code).limit(3).all()
        acupoints_response = {
            "code": 0,
            "message": "success",
            "data": {
                "total": count,
                "items": [
                    {
                        "id": a.id,
                        "name": a.name,
                        "code": a.code,
                        "meridian": a.meridian,
                        "body_part": a.body_part,
                        "location": a.simple_location,
                        "efficacy": a.efficacy,
                        "image_url": a.image_url
                    }
                    for a in acupoints_data
                ]
            }
        }
        print("\nGET /api/v1/acupoints?limit=3")
        print(json.dumps(acupoints_response, ensure_ascii=False, indent=2)[:800] + "...")

        return True

    except Exception as e:
        print(f"   [ERROR] {e}")
        return False
    finally:
        db.close()


def test_api_router_import():
    """Test that the API router can be imported"""
    print("\n" + "=" * 50)
    print("[3] Testing API Router Import")
    print("=" * 50)

    try:
        from api.routers.acupoints import router
        print(f"   [OK] Router imported successfully")
        print(f"   [OK] Router has {len(router.routes)} routes")

        for route in router.routes:
            print(f"      - {route.methods} {route.path}")

        return True
    except Exception as e:
        print(f"   [ERROR] {e}")
        return False


def main():
    print("\n" + "=" * 50)
    print("Acupoints API Test Suite")
    print("=" * 50)

    results = []

    # Test 1: Database
    results.append(("Database", test_database()))

    # Test 2: API Router
    results.append(("API Router", test_api_router_import()))

    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)

    all_passed = True
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"   {status} {name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n" + "=" * 50)
        print("[OK] All tests passed!")
        print("=" * 50)
        print("\nTo start the backend server:")
        print("   cd backend")
        print("   python main.py")
        print("\nThen visit: http://localhost:8000/docs")
        print("=" * 50)
        return 0
    else:
        print("\n[ERROR] Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
