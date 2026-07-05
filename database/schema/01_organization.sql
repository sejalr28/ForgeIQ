

CREATE TABLE factories (
    factory_id          SERIAL PRIMARY KEY,
    factory_name        VARCHAR(150) NOT NULL,
    location_city        VARCHAR(100),
    location_state       VARCHAR(100),
    location_country     VARCHAR(100),
    timezone             VARCHAR(50) DEFAULT 'Asia/Kolkata',
    is_active            BOOLEAN DEFAULT TRUE,
    created_at           TIMESTAMP DEFAULT NOW(),
    updated_at           TIMESTAMP DEFAULT NOW()
);

CREATE TABLE departments (
    department_id        SERIAL PRIMARY KEY,
    factory_id            INTEGER NOT NULL REFERENCES factories(factory_id) ON DELETE CASCADE,
    department_name       VARCHAR(150) NOT NULL,
    department_type       VARCHAR(50), -- production, quality, warehouse, maintenance, admin
    created_at            TIMESTAMP DEFAULT NOW()
);

CREATE TABLE production_lines (
    production_line_id    SERIAL PRIMARY KEY,
    factory_id             INTEGER NOT NULL REFERENCES factories(factory_id) ON DELETE CASCADE,
    department_id          INTEGER REFERENCES departments(department_id) ON DELETE SET NULL,
    line_name               VARCHAR(150) NOT NULL,
    line_code                VARCHAR(30) UNIQUE NOT NULL,
    rated_capacity_per_hour  NUMERIC(10,2), -- units/hour
    is_active                BOOLEAN DEFAULT TRUE,
    created_at                TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_departments_factory ON departments(factory_id);
CREATE INDEX idx_production_lines_factory ON production_lines(factory_id);