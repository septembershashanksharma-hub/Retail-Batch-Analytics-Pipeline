SELECT
    SUM(oi.quantity * oi.unit_price) AS total_sales
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'PAID';