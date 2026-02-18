# Local Data Governance Sandbox: Unity Catalog & DuckDB

Detta projekt demonstrerar uppsättningen av en modern, lokal dataplattform med fokus på **Data Governance**. Genom att använda Unity Catalog (OSS) som metadata-lager och DuckDB som compute engine, skapas en "Cloud-Ready" miljö för automatiserad hantering av data och rättigheter.

## 🏗 Arkitektur & Stack

Projektet är byggt i en isolerad miljö för att efterlikna en produktionsfärdig dataplattform:

- **OS:** WSL2 (Ubuntu 24.04)
- **Infrastruktur:** Docker & Docker Compose
- **Governance:** Unity Catalog (Open Source Software)
- **Pakethantering:** `uv` (Rust-baserad Python-manager)
- **Compute & Integration:** DuckDB & Pandas
- **Dataformat:** Apache Parquet (Medallion Architecture - Bronze Layer)



## 🚀 Nyckelfunktioner

- **Governance-as-Code:** Programmatisk provisionering av kataloger, scheman och tabeller via REST API.
- **Access Control Simulation:** Implementering av RBAC-logik (Role-Based Access Control) direkt i Python-skripten.
- **Decoupled Architecture:** Separation av metadata (Unity Catalog) från den fysiska lagringen och beräkningskraften (DuckDB).
- **Deterministisk miljö:** Fullständig reproducerbarhet genom `uv.lock` och Docker-containrar.

## 💡 Technical Insights: Specifikation vs. Implementering

En central del av projektet har varit att navigera i gränslandet mellan API-standarder och faktiska implementeringar:

- **Cloud-Ready kod:** Projektet följer den officiella Unity Catalog-standarden. Skripten är skrivna för att vara kompatibla med en molnbaserad Databricks-miljö.
- **OSS-observationer:** Under utvecklingen noterades att vissa avancerade endpoints (såsom `/history` och vissa `/permissions`) returnerar `404 Not Found` i den nuvarande OSS-versionen. Detta demonstrerar en förståelse för att open-source-versioner ofta fungerar som en kärna där vissa Enterprise-funktioner hanteras annorlunda.

## 🛠 Installation & Körning

### 1. Förutsättningar
Se till att du har Docker och `uv` installerat:
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

### 2. Starta infrastrukturen
```bash
docker compose up -d
```

### 3. Initiera miljön och kör flödet
```bash
# Synka bibliotek (requests, duckdb, pandas)
uv sync

# 1. Konfigurera metadata & Access Control
uv run setup_uc_metadata.py

# 2. Generera lokal data (Parquet)
uv run generate_data.py

# 3. Konsumera data via UC & DuckDB
uv run consume_data.py
```

## Resultat
Efter körning finns tabellen user_logs registrerad i Unity Catalog. Genom att anropa UC:s API hämtar vi tabellens fysiska plats och läser in den i en Pandas DataFrame via DuckDB, helt styrt av den centrala governance-modellen.