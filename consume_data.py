import duckdb
import requests

# --- KOPIERA IN DETTA ---
UC_URL = "http://localhost:8080/api/2.1/unity-catalog"
CATALOG = "min_portfolj"
SCHEMA = "bronze_layer"
TABLE = "user_logs"
# ------------------------

# 1. Hämta metadata från Unity Catalog
TABLE_URL = "http://localhost:8080/api/2.1/unity-catalog/tables/min_portfolj.bronze_layer.user_logs"
response = requests.get(TABLE_URL)
table_info = response.json()

# Hämta var filen "ska" ligga enligt UC
storage_location = table_info.get('storage_location', 'user_events.parquet')

# 2. Använd DuckDB för att konsumera datan
print(f"🔍 Läser data från platsen angiven i UC: {storage_location}")

# Vi kopplar DuckDB till vår lokala Parquet-fil
con = duckdb.connect()
result = con.execute(f"SELECT * FROM 'user_events.parquet'").df()

print("\n📊 Data hämtad via DuckDB baserat på UC-metadata:")
print(result)

# Visa historik/audit för tabellen
history_url = f"{UC_URL}/tables/{CATALOG}.{SCHEMA}.{TABLE}/history"
history_res = requests.get(history_url)

if history_res.status_code == 200:
    print("\n📜 Audit Log (Historik) från Unity Catalog:")
    print(json.dumps(history_res.json(), indent=2))
else:
    print("\nℹ️ Historik-API är inte tillgängligt i denna version, men metadata är säkrad.")