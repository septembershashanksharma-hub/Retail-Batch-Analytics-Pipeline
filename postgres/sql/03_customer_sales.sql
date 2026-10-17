SELECT
    c.customer_id,
    c.customer_name,
    SUM(oi.quantity * oi.unit_price) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'PAID'
GROUP BY c.customer_id, c.customer_name;