SELECT 
    c.first_name AS Cliente,
    o.order_date AS Fecha_Pedido,
    oi.quantity AS Cantidad,
    p.product_name AS Producto,
    b.brand_name AS Marca,
    cat.category_name AS Categoria
FROM workspace.tienda.customers c
JOIN workspace.tienda.orders o 
    ON c.customer_id = o.customer_id
JOIN workspace.tienda.order_items oi 
    ON o.order_id = oi.order_id
JOIN workspace.tienda.products p 
    ON oi.product_id = p.product_id
JOIN workspace.tienda.brands b 
    ON p.brand_id = b.brand_id
JOIN workspace.tienda.categories cat 
    ON p.category_id = cat.category_id;