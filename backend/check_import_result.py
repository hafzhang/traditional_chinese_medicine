"""
Check import results
"""
from api.database import SessionLocal
from api.models import Recipe

db = SessionLocal()
total = db.query(Recipe).count()
db.close()

print(f"Total recipes in database: {total}")
print(f"Expected: 12,784")
print(f"Difference: {12784 - total}")
