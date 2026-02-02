"""
Check database schema
"""
import sqlite3
from api.database import engine
from api.models import Base

print("Database:", engine.url)
print("Tables:", list(Base.metadata.tables.keys()))

# Get database file path
db_path = str(engine.url).replace('sqlite:///', '')
print("Database file:", db_path)

# Check recipes table schema
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(recipes)')
print("\nRecipes schema:")
for row in cursor.fetchall():
    print(row)

conn.close()
