import random
from datetime import datetime, timedelta
from decimal import Decimal

import psycopg

random.seed(42)

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="retail",
    user="retail",
    password="retail_pw",
) as connection:
    with connection.cursor() as cursor:

        # 1. Find or create the Laptops category.
        cursor.execute("""
            SELECT category_id
            FROM categories
            WHERE category_name = 'Laptops'
            ORDER BY category_id
            LIMIT 1;
        """)
        row = cursor.fetchone()

        if row:
            category_id = row[0]
        else:
            cursor.execute("""
                INSERT INTO categories (category_name)
                VALUES ('Laptops')
                RETURNING category_id;
            """)
            category_id = cursor.fetchone()[0]

        # 2. Add products. Existing products remain unchanged.
        products = [
            (101, "Dell Laptop", Decimal("55000.00"), category_id),
            (102, "HP Laptop", Decimal("45000.00"), category_id),
            (103, "Lenovo Laptop", Decimal("60000.00"), category_id),
            (104, "Acer Laptop", Decimal("40000.00"), category_id),
            (105, "Asus Laptop", Decimal("65000.00"), category_id),
        ]

        cursor.executemany("""
            INSERT INTO products
                (product_id, product_name, product_price, category_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (product_id) DO NOTHING;
        """, products)

        # 3. Add three stores.
        stores = [
            (1, "Bengaluru", "Karnataka"),
            (2, "Mumbai", "Maharashtra"),
            (3, "Hyderabad", "Telangana"),
        ]

        cursor.executemany("""
            INSERT INTO stores (store_id, store_city, store_state)
            VALUES (%s, %s, %s)
            ON CONFLICT (store_id) DO NOTHING;
        """, stores)

        # 4. Add 50 fictional customers.
        customers = []

        for customer_id in range(1, 51):
            _, city, state = random.choice(stores)
            customers.append((
                customer_id,
                f"Customer {customer_id}",
                city,
                state,
                random.choice(["Regular", "Premium"]),
            ))

        cursor.executemany("""
            INSERT INTO customers (
                customer_id, customer_name,
                customer_city, customer_state, segment
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING;
        """, customers)

        # Read actual saved prices, including any existing products.
        cursor.execute("""
            SELECT product_id, product_price
            FROM products
            WHERE product_id BETWEEN 101 AND 105
              AND product_price IS NOT NULL
              AND product_price >= 0;
        """)
        saved_products = cursor.fetchall()

        # 5. Generate 1,000 orders, each with 1–3 different products.
        inserted_orders = 0
        inserted_items = 0
        now = datetime.now()

        for order_id in range(3001, 4001):
            customer_id = random.randint(1, 50)
            store_id = random.choice([1, 2, 3])
            status = random.choices(
                ["PENDING", "PAID", "CANCELLED"],
                weights=[15, 75, 10],
            )[0]

            created_at = now - timedelta(
                days=random.randint(1, 90),
                minutes=random.randint(0, 1439),
            )

            updated_at = (
                created_at
                if status == "PENDING"
                else created_at + timedelta(minutes=random.randint(1, 120))
            )

            cursor.execute("""
                INSERT INTO orders (
                    order_id, customer_id, store_id,
                    status, created_at, updated_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO NOTHING
                RETURNING order_id;
            """, (
                order_id, customer_id, store_id,
                status, created_at, updated_at,
            ))

            # Do not add items again if this order already exists.
            if cursor.fetchone() is None:
                continue

            selected_products = random.sample(
                saved_products,
                k=random.randint(1, min(3, len(saved_products))),
            )

            for product_id, price in selected_products:
                cursor.execute("""
                    INSERT INTO order_items (
                        order_id, product_id, quantity, unit_price
                    )
                    VALUES (%s, %s, %s, %s);
                """, (
                    order_id,
                    product_id,
                    random.randint(1, 3),
                    price,
                ))
                inserted_items += 1

            inserted_orders += 1

# Changes commit when the connection block finishes successfully.
print(f"Saved {inserted_orders} new orders.")
print(f"Saved {inserted_items} new order items.")
print("Existing records were preserved.")