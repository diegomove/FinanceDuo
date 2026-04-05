-- People (seeded, never changes)
CREATE TABLE IF NOT EXISTS people (
    id              INTEGER PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    password_hash   TEXT
);

-- Months
CREATE TABLE IF NOT EXISTS months (
    id          INTEGER PRIMARY KEY,
    year        INTEGER NOT NULL,
    month       INTEGER NOT NULL,
    is_closed   INTEGER NOT NULL DEFAULT 0,
    UNIQUE(year, month)
);

-- Categories
CREATE TABLE IF NOT EXISTS categories (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    type        TEXT NOT NULL
        CHECK (type IN ('fixed', 'variable', 'extra'))
);

-- Income entries per month per person
CREATE TABLE IF NOT EXISTS income (
    id          INTEGER PRIMARY KEY,
    month_id    INTEGER NOT NULL REFERENCES months(id),
    person_id   INTEGER NOT NULL REFERENCES people(id),
    amount      REAL NOT NULL,
    description TEXT,
    UNIQUE(month_id, person_id)
);

-- Expected (budgeted) expenses per month per category
CREATE TABLE IF NOT EXISTS expected_expenses (
    id          INTEGER PRIMARY KEY,
    month_id    INTEGER NOT NULL REFERENCES months(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    amount      REAL NOT NULL,
    notes       TEXT,
    paid_by     TEXT NOT NULL DEFAULT 'split'
        CHECK (paid_by IN ('split', 'person1', 'person2', 'personal_person1', 'personal_person2')),
    UNIQUE(month_id, category_id)
);

-- Initial balance (starting bank balance when first using the app)
CREATE TABLE IF NOT EXISTS initial_balance (
    id          INTEGER PRIMARY KEY,
    person_id   INTEGER NOT NULL REFERENCES people(id),
    amount      REAL NOT NULL DEFAULT 0,
    UNIQUE(person_id)
);

-- Actual expenses (the TriCount-like log)
CREATE TABLE IF NOT EXISTS actual_expenses (
    id              INTEGER PRIMARY KEY,
    month_id        INTEGER NOT NULL REFERENCES months(id),
    category_id     INTEGER NOT NULL REFERENCES categories(id),
    paid_by         INTEGER NOT NULL REFERENCES people(id),
    amount          REAL NOT NULL,
    description     TEXT,
    date            TEXT NOT NULL,
    split_mode      TEXT NOT NULL DEFAULT '50/50'
        CHECK (split_mode IN ('50/50', 'person1_only', 'person2_only', 'custom', 'personal')),
    custom_ratio_person1 REAL DEFAULT 50,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Extra income (Bizums, refunds, etc.)
CREATE TABLE IF NOT EXISTS extra_income (
    id          INTEGER PRIMARY KEY,
    month_id    INTEGER NOT NULL REFERENCES months(id),
    person_id   INTEGER NOT NULL REFERENCES people(id),
    amount      REAL NOT NULL,
    description TEXT,
    date        TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_extra_income_month ON extra_income(month_id);

-- Expense templates (quick-add recurring expenses)
CREATE TABLE IF NOT EXISTS expense_templates (
    id              INTEGER PRIMARY KEY,
    category_id     INTEGER NOT NULL REFERENCES categories(id),
    paid_by         INTEGER NOT NULL REFERENCES people(id),
    amount          REAL NOT NULL,
    description     TEXT,
    split_mode      TEXT NOT NULL DEFAULT '50/50'
        CHECK (split_mode IN ('50/50', 'person1_only', 'person2_only', 'custom', 'personal')),
    custom_ratio_person1 REAL DEFAULT 50,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Settlements (record when a debt was paid back)
CREATE TABLE IF NOT EXISTS settlements (
    id          INTEGER PRIMARY KEY,
    month_id    INTEGER NOT NULL REFERENCES months(id),
    paid_by     INTEGER NOT NULL REFERENCES people(id),
    paid_to     INTEGER NOT NULL REFERENCES people(id),
    amount      REAL NOT NULL,
    description TEXT,
    date        TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_settlements_month ON settlements(month_id);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_actual_month ON actual_expenses(month_id);
CREATE INDEX IF NOT EXISTS idx_actual_category ON actual_expenses(month_id, category_id);
CREATE INDEX IF NOT EXISTS idx_expected_month ON expected_expenses(month_id);
