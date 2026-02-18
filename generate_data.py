import duckdb

# Skapa en enkel dataset och spara som Parquet
data = """
SELECT 1 as user_id, 'login' as event_type, TIMESTAMP '2024-03-27 10:00:00' as event_time
UNION ALL
SELECT 2, 'click', TIMESTAMP '2024-03-27 10:05:00'
"""
duckdb.query(data).write_parquet('user_events.parquet')
print("✅ Filen 'user_events.parquet' har skapats lokalt.")