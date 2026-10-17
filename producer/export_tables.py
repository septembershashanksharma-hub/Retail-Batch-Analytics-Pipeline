from pathlib import Path

import psycopg
from psycopg import sql

output_folder = Path(__file__).resolve().parent.parent / "exports"
output_folder.mkdir(exist_ok=True)

tables = [
    "categories",
    "products",
    "stores",
    "customers",
    "orders",
    "order_items",
]

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="retail",
    user="retail",
    password="retail_pw",
) as connection:
    with connection.cursor() as cursor:
        # Keep all six exports consistent with the same database snapshot.
        cursor.execute(
            "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY"
        )

        for table in tables:
            file_path = output_folder / f"{table}.csv"

            query = sql.SQL(
                "COPY {} TO STDOUT WITH (FORMAT CSV, HEADER TRUE)"
            ).format(sql.Identifier(table))

            with file_path.open("wb") as file:
                with cursor.copy(query) as copy:
                    for chunk in copy:
                        file.write(chunk)

            print(f"Exported: {file_path}")

print("All six tables exported.")