

CREATE TABLE energy_meters (
    energy_meter_id      SERIAL PRIMARY KEY,
    factory_id                INTEGER NOT NULL REFERENCES factories(factory_id) ON DELETE CASCADE,
    meter_code                   VARCHAR(30) UNIQUE NOT NULL,
    meter_type                     VARCHAR(20) NOT NULL -- electricity, water, gas
);

CREATE TABLE energy_usage (
    energy_usage_id       SERIAL PRIMARY KEY,
    energy_meter_id            INTEGER NOT NULL REFERENCES energy_meters(energy_meter_id) ON DELETE CASCADE,
    usage_date                    DATE NOT NULL,
    quantity_used                    NUMERIC(14,4) NOT NULL, -- kWh, liters, m3 depending on meter_type
    estimated_cost                     NUMERIC(12,2)
);

CREATE INDEX idx_energy_usage_meter_date ON energy_usage(energy_meter_id, usage_date);