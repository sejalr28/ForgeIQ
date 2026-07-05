

CREATE TABLE products (
    product_id         SERIAL PRIMARY KEY,
    product_code          VARCHAR(30) UNIQUE NOT NULL,
    product_name           VARCHAR(150) NOT NULL,
    category                 VARCHAR(100),
    unit_of_measure           VARCHAR(20) DEFAULT 'units',
    standard_cycle_time_sec    NUMERIC(10,2), -- expected seconds per unit
    is_active                   BOOLEAN DEFAULT TRUE
);

CREATE TABLE machines (
    machine_id          SERIAL PRIMARY KEY,
    production_line_id     INTEGER NOT NULL REFERENCES production_lines(production_line_id) ON DELETE CASCADE,
    machine_code              VARCHAR(30) UNIQUE NOT NULL,
    machine_name                VARCHAR(150) NOT NULL,
    machine_type                  VARCHAR(100),
    installed_date                 DATE,
    is_active                       BOOLEAN DEFAULT TRUE
);

CREATE TABLE machine_status (
    machine_status_id     SERIAL PRIMARY KEY,
    machine_id               INTEGER NOT NULL REFERENCES machines(machine_id) ON DELETE CASCADE,
    status                     VARCHAR(30) NOT NULL, -- running, idle, breakdown, maintenance
    status_start                TIMESTAMP NOT NULL,
    status_end                    TIMESTAMP,
    reason                          VARCHAR(255)
);

CREATE TABLE production_orders (
    production_order_id    SERIAL PRIMARY KEY,
    factory_id                INTEGER NOT NULL REFERENCES factories(factory_id) ON DELETE CASCADE,
    product_id                  INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    production_line_id            INTEGER NOT NULL REFERENCES production_lines(production_line_id) ON DELETE CASCADE,
    order_number                    VARCHAR(50) UNIQUE NOT NULL,
    planned_quantity                  NUMERIC(12,2) NOT NULL,
    planned_start_date                  DATE,
    planned_end_date                      DATE,
    status                                  VARCHAR(30) DEFAULT 'planned', -- planned, in_progress, completed, cancelled
    created_at                               TIMESTAMP DEFAULT NOW()
);

CREATE TABLE production_records (
    production_record_id    SERIAL PRIMARY KEY,
    production_order_id        INTEGER NOT NULL REFERENCES production_orders(production_order_id) ON DELETE CASCADE,
    production_line_id           INTEGER NOT NULL REFERENCES production_lines(production_line_id) ON DELETE CASCADE,
    shift_id                       INTEGER REFERENCES shifts(shift_id) ON DELETE SET NULL,
    record_date                      DATE NOT NULL,
    units_produced                     NUMERIC(12,2) NOT NULL DEFAULT 0,
    units_rejected                       NUMERIC(12,2) NOT NULL DEFAULT 0,
    downtime_minutes                       NUMERIC(10,2) DEFAULT 0,
    created_at                               TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_machines_line ON machines(production_line_id);
CREATE INDEX idx_machine_status_machine ON machine_status(machine_id);
CREATE INDEX idx_production_orders_line ON production_orders(production_line_id);
CREATE INDEX idx_production_records_date ON production_records(record_date);
CREATE INDEX idx_production_records_line_date ON production_records(production_line_id, record_date);