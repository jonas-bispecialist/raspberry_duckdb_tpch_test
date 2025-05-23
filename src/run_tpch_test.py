import duckdb
from pathlib import Path
import time
import math
import gc
import datetime

# Get the current directory where the script is located
current_dir = Path(__file__).resolve().parent

# Set scale factor
scale_factor = int(input("Enter scale factor: "))

# Set and verify the raw folder
raw_folder = current_dir / "raw" / f"{scale_factor:02d}"

if not raw_folder.exists():
    raise FileNotFoundError(f"Raw folder not found: {raw_folder}")

# Create paths so we can find all data tables.
table_paths = {
    name: raw_folder / f"{name}.parquet"
    for name in ["nation", "region", "part", "supplier", "partsupp", "customer", "orders", "lineitem"]
}

# To save memory run DuckDB from file.
tempdb_path = current_dir / "temp" / "tempdb.duckdb"

if tempdb_path.exists():
    tempdb_path.unlink()

# Connect to DuckDB (creates file if it does not exist)
conn = duckdb.connect(tempdb_path)
print("Connected to DuckDB")

# Optional settings for memory management
#conn.execute("PRAGMA threads = 2")
#conn.execute("PRAGMA memory_limit = '196MB'")

# Create views for all the tables in the `table_paths` dictionary
for table_name, table_path in table_paths.items():
    conn.execute(f"CREATE VIEW {table_name} AS SELECT * FROM '{table_path}'")

total_start = time.time()

print(f"--------- START TCP-H with scale factor  {scale_factor:02d} ---------")

# Iterate over the files from tcph_q01.sql to tcph_q22.sql
for i in range(1, 23):



    start = time.time()

    query_file_name = f'tpch_q{i:02d}.sql'  # Format the query number as two digits (01, 02, ..., 22)
    query_file_path = current_dir / "query" / query_file_name
    output_path = current_dir / "processed" / f'tpch_q{i:02d}.parquet'
        
    print(f"Query {i:02d} running...", end='\r', flush=True)

    with open(query_file_path, 'rb') as file:
        query = file.read().decode('utf-8').strip().rstrip(";")

    # Remove unused variables
    gc.collect()

    # Execute the query and store the result in a Parquet file using COPY   
    conn.execute(f"COPY ({query}) TO '{output_path}' (FORMAT PARQUET)")

    duration = time.time() - start
    duration_floored = math.floor(duration * 10) / 10
    
    print(f"Query {i:02d} finished in {duration_floored}s")

total_duration = time.time() - total_start
elapsed = datetime.timedelta(seconds=int(total_duration))
print(f"--------- END TCP-H in {str(elapsed)} ---------")