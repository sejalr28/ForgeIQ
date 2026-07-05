

CREATE TABLE kpis (
    kpi_id                SERIAL PRIMARY KEY,
    factory_id                 INTEGER NOT NULL REFERENCES factories(factory_id) ON DELETE CASCADE,
    kpi_name                      VARCHAR(100) NOT NULL, -- e.g. OEE, throughput, defect_rate
    kpi_scope                        VARCHAR(50), -- factory, line, machine
    scope_reference_id                  INTEGER, -- id of the line/machine, nullable if factory-level
    kpi_value                              NUMERIC(14,4) NOT NULL,
    kpi_date                                  DATE NOT NULL,
    created_at                                   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE forecasts (
    forecast_id            SERIAL PRIMARY KEY,
    forecast_type                VARCHAR(50) NOT NULL, -- production, inventory_demand
    entity_type                     VARCHAR(50) NOT NULL, -- production_line, material
    entity_id                          INTEGER NOT NULL,
    forecast_date                         DATE NOT NULL,
    predicted_value                          NUMERIC(14,4) NOT NULL,
    lower_bound                                 NUMERIC(14,4),
    upper_bound                                    NUMERIC(14,4),
    model_version                                     VARCHAR(50),
    created_at                                           TIMESTAMP DEFAULT NOW()
);

-- Alerts double as the "recommendation engine" output:
-- explains what's happening + recommends an action, not just a raw threshold breach.
CREATE TABLE alerts (
    alert_id               SERIAL PRIMARY KEY,
    factory_id                  INTEGER NOT NULL REFERENCES factories(factory_id) ON DELETE CASCADE,
    alert_type                      VARCHAR(50) NOT NULL, -- production_anomaly, low_inventory, supplier_delay, quality_spike, energy_spike
    severity                           VARCHAR(20) NOT NULL DEFAULT 'medium', -- low, medium, high, critical
    entity_type                           VARCHAR(50), -- production_line, warehouse, supplier, machine
    entity_id                                INTEGER,
    title                                        VARCHAR(255) NOT NULL,
    explanation                                    TEXT NOT NULL,   -- "what's happening"
    recommendation                                    TEXT,          -- "what action to take"
    is_resolved                                          BOOLEAN DEFAULT FALSE,
    created_at                                              TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_kpis_factory_date ON kpis(factory_id, kpi_date);
CREATE INDEX idx_forecasts_entity ON forecasts(entity_type, entity_id, forecast_date);
CREATE INDEX idx_alerts_factory ON alerts(factory_id);
CREATE INDEX idx_alerts_unresolved ON alerts(is_resolved) WHERE is_resolved = FALSE;