

CREATE TABLE suppliers (
    supplier_id          SERIAL PRIMARY KEY,
    supplier_name             VARCHAR(150) NOT NULL,
    supplier_code               VARCHAR(30) UNIQUE NOT NULL,
    contact_email                  VARCHAR(150),
    contact_phone                    VARCHAR(30),
    country                             VARCHAR(100),
    rating                                 NUMERIC(3,2), -- 0-5
    is_active                                BOOLEAN DEFAULT TRUE
);

CREATE TABLE purchase_orders (
    purchase_order_id      SERIAL PRIMARY KEY,
    supplier_id                  INTEGER NOT NULL REFERENCES suppliers(supplier_id) ON DELETE CASCADE,
    factory_id                     INTEGER NOT NULL REFERENCES factories(factory_id) ON DELETE CASCADE,
    order_number                     VARCHAR(50) UNIQUE NOT NULL,
    order_date                          DATE NOT NULL,
    expected_delivery_date                 DATE,
    actual_delivery_date                     DATE,
    status                                      VARCHAR(30) DEFAULT 'pending', -- pending, shipped, delivered, delayed, cancelled
    created_at                                    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE purchase_order_items (
    purchase_order_item_id  SERIAL PRIMARY KEY,
    purchase_order_id            INTEGER NOT NULL REFERENCES purchase_orders(purchase_order_id) ON DELETE CASCADE,
    material_id                     INTEGER NOT NULL REFERENCES materials(material_id) ON DELETE CASCADE,
    quantity_ordered                   NUMERIC(12,2) NOT NULL,
    quantity_received                     NUMERIC(12,2) DEFAULT 0,
    unit_price                               NUMERIC(12,2)
);

CREATE INDEX idx_purchase_orders_supplier ON purchase_orders(supplier_id);
CREATE INDEX idx_purchase_orders_status ON purchase_orders(status);
CREATE INDEX idx_po_items_po ON purchase_order_items(purchase_order_id);