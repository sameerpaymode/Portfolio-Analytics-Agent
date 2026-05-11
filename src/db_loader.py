import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "database/portfolio_database.db"
SCHEMA_PATH = "database/database_schema.sql"
DATA_DIR = "data"


def create_database():

    conn = sqlite3.connect(DB_PATH)

    print("Connected to SQLite DB")

    # Execute schema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)

    print("Schema created successfully")

    # CSV loading order matters because of foreign keys
    csv_files = [
        ("sectors", "sectors.csv"),
        ("securities", "securities.csv"),
        ("benchmarks", "benchmarks.csv"),
        ("portfolios", "portfolios.csv"),
        ("holdings", "holdings.csv"),
        ("transactions", "transactions.csv"),
        ("historical_prices", "historical_prices.csv"),
        ("portfolio_performance", "portfolio_performance.csv"),
        ("risk_metrics", "risk_metrics.csv"),
    ]

    for table_name, file_name in csv_files:

        file_path = Path(DATA_DIR) / file_name

        print(f"Loading {file_name}...")

        df = pd.read_csv(file_path)

        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )

        print(f"Loaded {len(df)} rows into {table_name}")

    conn.commit()
    conn.close()

    print("\nDatabase setup completed successfully!")


if __name__ == "__main__":
    create_database()