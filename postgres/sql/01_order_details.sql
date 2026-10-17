SELECT
    o.order_id,
    c.customer_name,
    s.store_city,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS item_total,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN stores s ON o.store_id = s.store_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;