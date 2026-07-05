

CREATE TABLE defect_categories (
    defect_category_id   SERIAL PRIMARY KEY,
    category_name              VARCHAR(100) UNIQUE NOT NULL,
    severity                      VARCHAR(20) -- minor, major, critical
);

CREATE TABLE quality_inspections (
    quality_inspection_id  SERIAL PRIMARY KEY,
    production_order_id         INTEGER NOT NULL REFERENCES production_orders(production_order_id) ON DELETE CASCADE,
    inspector_employee_id          INTEGER REFERENCES employees(employee_id) ON DELETE SET NULL,
    inspection_date                   DATE NOT NULL,
    units_inspected                      NUMERIC(12,2) NOT NULL,
    units_passed                            NUMERIC(12,2) NOT NULL,
    units_failed                               NUMERIC(12,2) NOT NULL,
    created_at                                   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE defects (
    defect_id             SERIAL PRIMARY KEY,
    quality_inspection_id      INTEGER NOT NULL REFERENCES quality_inspections(quality_inspection_id) ON DELETE CASCADE,
    defect_category_id            INTEGER NOT NULL REFERENCES defect_categories(defect_category_id) ON DELETE CASCADE,
    quantity                         NUMERIC(12,2) NOT NULL DEFAULT 1,
    notes                               TEXT
);

CREATE INDEX idx_quality_inspections_date ON quality_inspections(inspection_date);
CREATE INDEX idx_defects_category ON defects(defect_category_id);