import pandas as pd
import sqlite3
import os

# === Step 1 & 2: Infer Schema and Create Table ===

def infer_sql_type(dtype):
    if pd.api.types.is_integer_dtype(dtype): return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype): return "REAL"
    else: return "TEXT"

def log_error(msg):
    with open("error_log.txt", "a") as log:
        log.write(msg + "\n")

def create_table_from_csv(csv_path, table_name, conn):
    try:
        df = pd.read_csv(csv_path)
        cursor = conn.cursor()

        table_exists = cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (table_name,)
        ).fetchone()

        if table_exists:
            print(f"Table '{table_name}' already exists.")
            action = input("Overwrite (o), Rename (r), or Skip (s)? ").strip().lower()

            if action == 's':
                print(f"Skipped '{table_name}'.")
                return
            elif action == 'r':
                new_name = input("Enter new table name: ").strip()
                table_name = new_name
            elif action == 'o':
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            else:
                print("Invalid input. Skipping.")
                return

        columns = ", ".join([f"'{col}' {infer_sql_type(df[col])}" for col in df.columns])
        cursor.execute(f"CREATE TABLE {table_name} ({columns});")
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Table '{table_name}' created.")
    except Exception as e:
        log_error(f"Error loading {csv_path}: {e}")
        print("Error loading CSV. Check error_log.txt.")

# === Step 3: List Tables and Run Queries ===

def list_tables(conn):
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    if not tables:
        print("No tables found.")
    else:
        print("Tables:")
        for (name,) in tables:
            print(f" - {name}")

def run_sql_query(conn):
    try:
        query = input("Enter SQL query:\n> ")
        df = pd.read_sql_query(query, conn)
        print(df)
    except Exception as e:
        log_error(f"Query error: {e}")
        print("Error running query. Check error_log.txt.")

# === Step 4: Schema Inspection ===

def get_schema(conn):
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    schema = {}
    for (table_name,) in tables:
        cols = conn.execute(f"PRAGMA table_info({table_name});").fetchall()
        schema[table_name] = [(col[1], col[2]) for col in cols]
    return schema

# === Step 5: Simulated AI SQL Generation ===

def simulate_ai(user_input, schema):
    if "employees" in user_input and "age" in user_input and ">" in user_input:
        return "SELECT * FROM employees WHERE age > 30;"
    if "departments" in user_input:
        return "SELECT * FROM departments;"
    return "SELECT 'Simulated AI could not parse the input.';"

def run_ai_query(conn):
    try:
        user_input = input("Ask something in plain English:\n> ")
        schema = get_schema(conn)
        sql = simulate_ai(user_input, schema)
        print(f"\nGenerated SQL: {sql}")
        df = pd.read_sql_query(sql, conn)
        print(df)
    except Exception as e:
        log_error(f"AI query error: {e}")
        print("Error during AI query. Check error_log.txt.")

# === Step 4: CLI Loop ===

def run_cli():
    conn = sqlite3.connect("/mnt/data/chat_spreadsheet.db")
    print("Welcome to the CLI Assistant.")
    while True:
        print("\nOptions:")
        print("1. Load CSV file")
        print("2. Run SQL query")
        print("3. List tables")
        print("4. Ask in plain English (AI)")
        print("5. Exit")
        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            path = input("Enter CSV file path: ").strip()
            if os.path.exists(path):
                name = os.path.splitext(os.path.basename(path))[0]
                create_table_from_csv(path, name, conn)
            else:
                print("File not found.")
        elif choice == '2':
            run_sql_query(conn)
        elif choice == '3':
            list_tables(conn)
        elif choice == '4':
            run_ai_query(conn)
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    run_cli()


# === OPTIONAL: Auto-generate test CSVs for convenience ===
os.makedirs("/mnt/data/csvs", exist_ok=True)

pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35]
}).to_csv("/mnt/data/csvs/employees.csv", index=False)

pd.DataFrame({
    "dept_id": [101, 102],
    "dept_name": ["HR", "Engineering"]
}).to_csv("/mnt/data/csvs/departments.csv", index=False)

print("Sample CSV files created in /mnt/data/csvs/")
