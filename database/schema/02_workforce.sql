

CREATE TABLE roles (
    role_id           SERIAL PRIMARY KEY,
    role_name          VARCHAR(100) UNIQUE NOT NULL,
    role_level         VARCHAR(50) -- operator, supervisor, manager, technician
);

CREATE TABLE shifts (
    shift_id           SERIAL PRIMARY KEY,
    factory_id          INTEGER NOT NULL REFERENCES factories(factory_id) ON DELETE CASCADE,
    shift_name           VARCHAR(50) NOT NULL, -- Morning, Evening, Night
    start_time            TIME NOT NULL,
    end_time               TIME NOT NULL
);

CREATE TABLE employees (
    employee_id         SERIAL PRIMARY KEY,
    factory_id            INTEGER NOT NULL REFERENCES factories(factory_id) ON DELETE CASCADE,
    department_id         INTEGER REFERENCES departments(department_id) ON DELETE SET NULL,
    role_id                INTEGER REFERENCES roles(role_id) ON DELETE SET NULL,
    employee_code           VARCHAR(30) UNIQUE NOT NULL,
    full_name                VARCHAR(150) NOT NULL,
    date_joined                DATE,
    is_active                  BOOLEAN DEFAULT TRUE,
    created_at                  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE employee_shift_assignments (
    assignment_id         SERIAL PRIMARY KEY,
    employee_id             INTEGER NOT NULL REFERENCES employees(employee_id) ON DELETE CASCADE,
    shift_id                 INTEGER NOT NULL REFERENCES shifts(shift_id) ON DELETE CASCADE,
    production_line_id        INTEGER REFERENCES production_lines(production_line_id) ON DELETE SET NULL,
    work_date                   DATE NOT NULL,
    UNIQUE(employee_id, work_date)
);

CREATE INDEX idx_employees_factory ON employees(factory_id);
CREATE INDEX idx_shift_assignments_date ON employee_shift_assignments(work_date);