-- ===============================
-- SCHEMA
-- ===============================

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    total_amount NUMERIC(10,2),
    status TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_name TEXT,
    quantity INT,
    price NUMERIC(10,2)
);

-- ===============================
-- SEED DATA
-- ===============================

INSERT INTO customers (name, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com'),
('Charlie', 'charlie@example.com');

INSERT INTO orders (customer_id, total_amount, status) VALUES
(1, 120.50, 'completed'),
(2, 89.99, 'pending'),
(1, 45.00, 'completed');

INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
(1, 'Keyboard', 1, 50.00),
(1, 'Mouse', 1, 20.50),
(2, 'Monitor', 1, 89.99),
(3, 'USB Cable', 3, 15.00);

-- ===============================
-- READ-ONLY HARDENING
-- ===============================

REVOKE ALL ON SCHEMA public FROM readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO readonly_user;

ALTER ROLE readonly_user SET search_path TO public;
