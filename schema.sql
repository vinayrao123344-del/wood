CREATE TABLE IF NOT EXISTS wood_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS wood_subtypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    price_per_sqft REAL NOT NULL,
    FOREIGN KEY (type_id) REFERENCES wood_types (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS labor_cost (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image_url TEXT,
    description TEXT
);

-- Insert initial labor cost if not exists
INSERT OR IGNORE INTO labor_cost (id, amount) VALUES (1, 50.0);
