

CREATE TABLE warehouses (
    warehouse_id       SERIAL PRIMARY KEY,
    factory_id             INTEGER NOT NULL REFERENCES factories(factory_id) ON DELETE CASCADE,
    warehouse_name           VARCHAR(150) NOT NULL,
    warehouse_code             VARCHAR(30) UNIQUE NOT NULL,
    capacity_units                NUMERIC(12,2)
);

CREATE TABLE materials (
    material_id          SERIAL PRIMARY KEY,
    material_code            VARCHAR(30) UNIQUE NOT NULL,
    material_name              VARCHAR(150) NOT NULL,
    category                     VARCHAR(100),
    unit_of_measure                VARCHAR(20) DEFAULT 'units',
    reorder_level                    NUMERIC(12,2) DEFAULT 0,
    reorder_quantity                   NUMERIC(12,2) DEFAULT 0
);

CREATE TABLE inventory (
    inventory_id          SERIAL PRIMARY KEY,
    warehouse_id              INTEGER NOT NULL REFERENCES warehouses(warehouse_id) ON DELETE CASCADE,
    material_id                  INTEGER NOT NULL REFERENCES materials(material_id) ON DELETE CASCADE,
    quantity_on_hand                NUMERIC(12,2) NOT NULL DEFAULT 0,
    last_updated                       TIMESTAMP DEFAULT NOW(),
    UNIQUE(warehouse_id, material_id)
);

CREATE TABLE stock_movements (
    stock_movement_id      SERIAL PRIMARY KEY,
    warehouse_id                INTEGER NOT NULL REFERENCES warehouses(warehouse_id) ON DELETE CASCADE,
    material_id                    INTEGER NOT NULL REFERENCES materials(material_id) ON DELETE CASCADE,
    movement_type                     VARCHAR(20) NOT NULL, -- inbound, outbound, adjustment
    quantity                             NUMERIC(12,2) NOT NULL,
    reference_type                         VARCHAR(50), -- purchase_order, production_order, manual
    reference_id                             INTEGER,
    movement_date                              TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_inventory_warehouse ON inventory(warehouse_id);
CREATE INDEX idx_inventory_material ON inventory(material_id);
CREATE INDEX idx_stock_movements_date ON stock_movements(movement_date);