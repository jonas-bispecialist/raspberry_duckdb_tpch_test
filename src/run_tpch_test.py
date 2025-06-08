import duckdb
from pathlib import Path
import time
import math
import gc
import datetime

def get_scale_factor() -> int:
    """Get and validate scale factor from user input."""
    while True:
        try:
            scale = int(input("Enter scale factor: "))
            if scale > 0:
                return scale
            print("Scale factor must be positive")
        except ValueError:
            print("Please enter a valid number")

def setup_folders(scale_factor: int):
    """Sets up folder paths for the given scale factor."""
    current_dir = Path.cwd()
    raw_folder = current_dir / "raw" / f"{scale_factor:02d}"
    duckdb_folder = current_dir / "duckdb" / f"{scale_factor:02d}"  # e.g., duckdb/05
    processed_folder = current_dir / "processed" / f"{scale_factor:02d}"

    # Create folders if they don't exist
    raw_folder.mkdir(parents=True, exist_ok=True)
    duckdb_folder.mkdir(parents=True, exist_ok=True)
    processed_folder.mkdir(parents=True, exist_ok=True)

    return current_dir, raw_folder, duckdb_folder, processed_folder

def setup_database(duckdb_folder: Path, raw_folder: Path) -> duckdb.DuckDBPyConnection:
    db_path = duckdb_folder / "tpch.duckdb"
    db_exists = db_path.exists()
    if db_exists:
        db_path.unlink()
    conn = duckdb.connect(str(db_path))
    
    # Mount all Parquet files as views
    for parquet_file in raw_folder.glob("*.parquet"):
        view_name = parquet_file.stem
        conn.execute(f"CREATE VIEW {view_name} AS SELECT * FROM read_parquet('{parquet_file}')")
    
    return conn

def execute_query(i: int, 
                  current_dir: Path, 
                  processed_folder: Path, 
                  conn: duckdb.DuckDBPyConnection) -> float:
    
    query_path = current_dir / "query" / f"tpch_q{i:02d}.sql"
    output_path = processed_folder / f"tpch_q{i:02d}.parquet"
    
    with open(query_path, 'rb') as file:
        query = file.read().decode('utf-8').strip().rstrip(";")
    
    start = time.time()
    conn.execute(f"COPY ({query}) TO '{output_path}' (FORMAT PARQUET)")
    duration = math.floor((time.time() - start) * 10) / 10
    
    return duration


def run_tpch_benchmark(scale_factor: int, 
                       conn: duckdb.DuckDBPyConnection, 
                       current_dir: Path, 
                       processed_folder: Path) -> None:
    """Run the complete TPC-H benchmark suite."""

    total_start = time.time()
    print(f"\n--------- START TCP-H with scale factor {scale_factor:02d} ---------")
    
    for i in range(1, 23):
        print(f"Query {i:02d} running...", end='\r', flush=True)
        duration = execute_query(i, current_dir, processed_folder, conn)
        print(f"Query {i:02d} finished in {duration}s")
        
    # Print summary
    total_duration = time.time() - total_start
    elapsed = datetime.timedelta(seconds=int(total_duration))
    print(f"--------- END TCP-H in {str(elapsed)} ---------")
    
    # Close connection and checkpoint
    conn.execute("CHECKPOINT")    
    conn.close
if __name__ == "__main__":
    scale_factor = get_scale_factor()
    current_dir, raw_folder, duckdb_folder, processed_folder = setup_folders(scale_factor)
    
    # Get connection from the combined setup function
    conn = setup_database(duckdb_folder, raw_folder)

    run_tpch_benchmark(scale_factor, conn, current_dir, processed_folder)