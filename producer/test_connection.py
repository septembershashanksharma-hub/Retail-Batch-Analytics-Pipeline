import psycopg

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="retail",
    user="retail",
    password="retail_pw"
) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT product_id, product_name FROM products;")
        print(cursor.fetchall())