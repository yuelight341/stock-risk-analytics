from pathlib import Path
import duckdb

SQL_DIR = Path("sql")
OUT_DIR = Path("output/results")
DB_PATH = "stock_data.db"
SKIP = {"schema.sql"}

def connect():
    conn = duckdb.connect()
    conn.execute("INSTALL sqlite;")
    conn.execute("LOAD sqlite;")
    conn.execute(f"ATTACH '{DB_PATH}' AS s (TYPE SQLITE);")
    return conn

def get_benchmark_from_db(conn):
    query = "SELECT DISTINCT ticker FROM s.daily_prices WHERE is_benchmark = 1"
    
    try:
        result = conn.query(query).fetchone()
        if result:
            return result[0]
    except Exception:
        pass
        
    print("[WARNING] Could not find the benchmark flag. Defaulting to '^GSPC'.")
    return "^GSPC"

def run_sql_file(conn, path: Path, benchmark: str):
    sql = path.read_text()
    return conn.query(sql).df()

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = connect()

    benchmark = get_benchmark_from_db(conn)
    print(f"--- Detected Benchmark: {benchmark} ---\n")

    views = SQL_DIR / "views.sql"
    if views.exists():
        views_sql = views.read_text()
        conn.execute(views_sql)

    for sql_file in sorted(SQL_DIR.glob("*.sql")):
        if sql_file.name in SKIP or sql_file.name == "views.sql":
            continue
        try:
            df = run_sql_file(conn, sql_file, benchmark)
        except Exception as e:
            print(f"[FAIL] {sql_file.name}: {e}")
            continue
        
        out = OUT_DIR / f"{sql_file.stem}.csv"
        df.to_csv(out, index=False)
        print(f"--- {sql_file.stem} ---")
        print(df.to_string(index=False))
        print("\n")

if __name__ == "__main__":
    main()