CREATE TABLE categories
(
    category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_name VARCHAR(30) NOT NULL,
    parent_category_id INT REFERENCES categories(category_id)
);

CREATE TABLE products
(
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50) NOT NULL,
    product_price NUMERIC(10,2),
    category_id INT,

    FOREIGN KEY(category_id)
    REFERENCES categories(category_id)
    
);

CREATE TABLE stores 
(
    store_id INT PRIMARY KEY,
    store_city VARCHAR(20) NOT NULL,
    store_state VARCHAR(20) NOT NULL
);

CREATE TABLE customers
(
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50), 
    customer_city VARCHAR(20) NOT NULL,
    customer_state VARCHAR(20) NOT NULL,
    segment VARCHAR(10) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

   INSERT INTO categories VALUES (1, 'Electronics', NULL);
   INSERT INTO categories VALUES (2, 'Laptops', 1);
   INSERT INTO categories VALUES (3, 'Ghost', 999);