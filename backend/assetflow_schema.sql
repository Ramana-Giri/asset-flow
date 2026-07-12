-- =====================================================================
-- AssetFlow — Enterprise Asset & Resource Management System
-- Database Schema  |  PostgreSQL 13+
-- =====================================================================
-- Notes:
--  - Uses ENUM types for fixed-vocabulary fields (roles, statuses, etc.)
--  - Uses a GiST EXCLUDE constraint to guarantee no overlapping bookings
--    for the same resource at the database level (not just app logic).
--  - Uses a partial UNIQUE index to guarantee an asset can never have
--    two simultaneous "Active" allocations (no double-allocation).
--  - JSONB columns give asset categories flexible/optional custom
--    fields (e.g. "warranty_period" for Electronics) without needing
--    a separate EAV table pair.
-- =====================================================================

-- ---------------------------------------------------------------------
-- EXTENSIONS
-- ---------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- ---------------------------------------------------------------------
-- ENUM TYPES
-- ---------------------------------------------------------------------
CREATE TYPE user_role            AS ENUM ('Admin','Asset Manager','Department Head','Employee');
CREATE TYPE account_status       AS ENUM ('Active','Inactive');
CREATE TYPE asset_condition      AS ENUM ('Excellent','Good','Fair','Poor','Damaged');
CREATE TYPE asset_status         AS ENUM ('Available','Allocated','Reserved','Under Maintenance','Lost','Retired','Disposed');
CREATE TYPE allocation_target    AS ENUM ('Employee','Department');
CREATE TYPE allocation_status    AS ENUM ('Active','Returned');
CREATE TYPE transfer_status      AS ENUM ('Requested','Approved','Rejected','Completed');
CREATE TYPE booking_status       AS ENUM ('Upcoming','Ongoing','Completed','Cancelled');
CREATE TYPE maintenance_priority AS ENUM ('Low','Medium','High','Critical');
CREATE TYPE maintenance_status   AS ENUM ('Pending','Approved','Rejected','Technician Assigned','In Progress','Resolved');
CREATE TYPE audit_cycle_status   AS ENUM ('Planned','In Progress','Closed');
CREATE TYPE audit_result         AS ENUM ('Verified','Missing','Damaged');
CREATE TYPE resolution_status    AS ENUM ('Open','Resolved');

-- =====================================================================
-- 1. DEPARTMENTS
-- =====================================================================
CREATE TABLE departments (
    id                    SERIAL PRIMARY KEY,
    name                  VARCHAR(150) NOT NULL UNIQUE,
    parent_department_id  INT REFERENCES departments(id) ON DELETE SET NULL,
    head_user_id          INT,                       -- FK added below, after users exists
    status                account_status NOT NULL DEFAULT 'Active',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================================
-- 2. ASSET CATEGORIES
-- =====================================================================
CREATE TABLE asset_categories (
    id                   SERIAL PRIMARY KEY,
    name                 VARCHAR(100) NOT NULL UNIQUE,
    description          TEXT,
    custom_field_schema  JSONB NOT NULL DEFAULT '[]'::jsonb,  -- e.g. [{"field":"warranty_period","type":"number","unit":"months"}]
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================================
-- 3. USERS  (Employee Directory + Authentication)
-- =====================================================================
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(150) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    role            user_role NOT NULL DEFAULT 'Employee',   -- signup always creates 'Employee'
    department_id   INT REFERENCES departments(id) ON DELETE SET NULL,
    status          account_status NOT NULL DEFAULT 'Active',
    promoted_by     INT REFERENCES users(id) ON DELETE SET NULL,  -- Admin who promoted this user
    promoted_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE departments
    ADD CONSTRAINT fk_departments_head
    FOREIGN KEY (head_user_id) REFERENCES users(id) ON DELETE SET NULL;

CREATE INDEX idx_users_department ON users(department_id);
CREATE INDEX idx_users_role       ON users(role);

-- =====================================================================
-- 4. PASSWORD RESET TOKENS  (forgot-password flow)
-- =====================================================================
CREATE TABLE password_reset_tokens (
    id          SERIAL PRIMARY KEY,
    user_id     INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token       VARCHAR(255) NOT NULL UNIQUE,
    expires_at  TIMESTAMPTZ NOT NULL,
    used        BOOLEAN NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================================
-- 5. USER SESSIONS  (session validation)
-- =====================================================================
CREATE TABLE user_sessions (
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_token   VARCHAR(255) NOT NULL UNIQUE,
    ip_address      VARCHAR(64),
    user_agent      TEXT,
    expires_at      TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_active_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================================
-- 6. ASSETS
-- =====================================================================
CREATE SEQUENCE asset_tag_seq START 1;

CREATE TABLE assets (
    id                    SERIAL PRIMARY KEY,
    asset_tag             VARCHAR(20) UNIQUE,          -- auto-generated, e.g. AF-0001
    name                  VARCHAR(150) NOT NULL,
    category_id           INT NOT NULL REFERENCES asset_categories(id),
    serial_number         VARCHAR(100) UNIQUE,
    acquisition_date      DATE,
    acquisition_cost      NUMERIC(12,2),               -- reporting/ranking only, not linked to accounting
    condition             asset_condition NOT NULL DEFAULT 'Good',
    location              VARCHAR(150),
    department_id         INT REFERENCES departments(id) ON DELETE SET NULL,  -- owning department
    status                asset_status NOT NULL DEFAULT 'Available',
    is_bookable           BOOLEAN NOT NULL DEFAULT FALSE,   -- shared/bookable flag
    qr_code               VARCHAR(150) UNIQUE,
    custom_field_values   JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by            INT REFERENCES users(id),
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_assets_status     ON assets(status);
CREATE INDEX idx_assets_category   ON assets(category_id);
CREATE INDEX idx_assets_department ON assets(department_id);
CREATE INDEX idx_assets_serial     ON assets(serial_number);
CREATE INDEX idx_assets_bookable   ON assets(is_bookable) WHERE is_bookable = TRUE;

-- =====================================================================
-- 7. ASSET DOCUMENTS / PHOTOS
-- =====================================================================
CREATE TABLE asset_documents (
    id            SERIAL PRIMARY KEY,
    asset_id      INT NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    file_url      VARCHAR(500) NOT NULL,
    file_type     VARCHAR(50),                -- Photo, Invoice, Manual, etc.
    uploaded_by   INT REFERENCES users(id),
    uploaded_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================================
-- 8. ASSET STATUS HISTORY  (full lifecycle audit trail)
-- =====================================================================
CREATE TABLE asset_status_history (
    id              SERIAL PRIMARY KEY,
    asset_id        INT NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    old_status      asset_status,
    new_status      asset_status NOT NULL,
    changed_by      INT REFERENCES users(id),
    reason          VARCHAR(255),
    reference_type  VARCHAR(50),               -- Allocation, Maintenance, Audit, Manual
    reference_id    INT,
    changed_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_status_history_asset ON asset_status_history(asset_id);

-- =====================================================================
-- 9. ALLOCATIONS
-- =====================================================================
CREATE TABLE allocations (
    id                          SERIAL PRIMARY KEY,
    asset_id                    INT NOT NULL REFERENCES assets(id),
    allocated_to_type           allocation_target NOT NULL,
    allocated_to_user_id        INT REFERENCES users(id),
    allocated_to_department_id  INT REFERENCES departments(id),
    allocated_by                INT NOT NULL REFERENCES users(id),   -- Asset Manager
    allocation_date             DATE NOT NULL DEFAULT CURRENT_DATE,
    expected_return_date        DATE,
    actual_return_date          DATE,
    return_condition_notes      TEXT,
    returned_by                 INT REFERENCES users(id),
    status                      allocation_status NOT NULL DEFAULT 'Active',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_allocation_target CHECK (
        (allocated_to_type = 'Employee'   AND allocated_to_user_id       IS NOT NULL AND allocated_to_department_id IS NULL)
        OR
        (allocated_to_type = 'Department' AND allocated_to_department_id IS NOT NULL AND allocated_to_user_id      IS NULL)
    )
);

-- Core business rule: an asset can only have ONE active allocation at a time
CREATE UNIQUE INDEX uq_one_active_allocation_per_asset
    ON allocations(asset_id) WHERE (status = 'Active');

CREATE INDEX idx_allocations_asset  ON allocations(asset_id);
CREATE INDEX idx_allocations_user   ON allocations(allocated_to_user_id);
CREATE INDEX idx_allocations_status ON allocations(status);
CREATE INDEX idx_allocations_overdue ON allocations(expected_return_date) WHERE status = 'Active';

-- =====================================================================
-- 10. TRANSFER REQUESTS
-- =====================================================================
CREATE TABLE transfer_requests (
    id                  SERIAL PRIMARY KEY,
    asset_id            INT NOT NULL REFERENCES assets(id),
    from_allocation_id  INT REFERENCES allocations(id),
    requested_by        INT NOT NULL REFERENCES users(id),
    to_user_id          INT REFERENCES users(id),
    to_department_id    INT REFERENCES departments(id),
    reason              TEXT,
    status              transfer_status NOT NULL DEFAULT 'Requested',
    approved_by         INT REFERENCES users(id),      -- Asset Manager / Department Head
    approved_at         TIMESTAMPTZ,
    new_allocation_id   INT REFERENCES allocations(id),  -- set once re-allocated
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_transfer_target CHECK (to_user_id IS NOT NULL OR to_department_id IS NOT NULL)
);

CREATE INDEX idx_transfer_asset  ON transfer_requests(asset_id);
CREATE INDEX idx_transfer_status ON transfer_requests(status);

-- =====================================================================
-- 11. RESOURCE BOOKINGS
-- =====================================================================
CREATE TABLE resource_bookings (
    id             SERIAL PRIMARY KEY,
    asset_id       INT NOT NULL REFERENCES assets(id),
    booked_by      INT NOT NULL REFERENCES users(id),
    department_id  INT REFERENCES departments(id),      -- booked on behalf of
    start_time     TIMESTAMPTZ NOT NULL,
    end_time       TIMESTAMPTZ NOT NULL,
    purpose        VARCHAR(255),
    status         booking_status NOT NULL DEFAULT 'Upcoming',
    cancelled_by   INT REFERENCES users(id),
    cancelled_at   TIMESTAMPTZ,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_booking_time CHECK (end_time > start_time)
);

-- Core business rule: no two overlapping bookings for the same resource
-- (half-open interval '[)' means a 10:00-11:00 booking does NOT
-- conflict with an existing 9:00-10:00 booking, matching the spec example)
ALTER TABLE resource_bookings
    ADD CONSTRAINT excl_no_overlapping_bookings
    EXCLUDE USING gist (
        asset_id WITH =,
        tstzrange(start_time, end_time, '[)') WITH &&
    ) WHERE (status IN ('Upcoming','Ongoing'));

CREATE INDEX idx_bookings_asset_time ON resource_bookings(asset_id, start_time, end_time);

-- =====================================================================
-- 12. MAINTENANCE REQUESTS
-- =====================================================================
CREATE TABLE maintenance_requests (
    id                      SERIAL PRIMARY KEY,
    asset_id                INT NOT NULL REFERENCES assets(id),
    raised_by               INT NOT NULL REFERENCES users(id),
    issue_description       TEXT NOT NULL,
    priority                maintenance_priority NOT NULL DEFAULT 'Medium',
    photo_url               VARCHAR(500),
    status                  maintenance_status NOT NULL DEFAULT 'Pending',
    reviewed_by             INT REFERENCES users(id),     -- Asset Manager
    reviewed_at             TIMESTAMPTZ,
    rejection_reason        TEXT,
    technician_name         VARCHAR(150),
    technician_contact      VARCHAR(100),
    technician_assigned_at  TIMESTAMPTZ,
    in_progress_at          TIMESTAMPTZ,
    resolved_at             TIMESTAMPTZ,
    resolution_notes        TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_maintenance_asset  ON maintenance_requests(asset_id);
CREATE INDEX idx_maintenance_status ON maintenance_requests(status);

-- =====================================================================
-- 13. AUDIT CYCLES
-- =====================================================================
CREATE TABLE audit_cycles (
    id                   SERIAL PRIMARY KEY,
    name                 VARCHAR(150) NOT NULL,
    scope_department_id  INT REFERENCES departments(id),
    scope_location       VARCHAR(150),
    start_date           DATE NOT NULL,
    end_date             DATE NOT NULL,
    status               audit_cycle_status NOT NULL DEFAULT 'Planned',
    created_by           INT NOT NULL REFERENCES users(id),
    closed_by            INT REFERENCES users(id),
    closed_at            TIMESTAMPTZ,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_audit_dates CHECK (end_date >= start_date)
);

-- =====================================================================
-- 14. AUDIT CYCLE AUDITORS  (junction: many auditors per cycle)
-- =====================================================================
CREATE TABLE audit_cycle_auditors (
    id              SERIAL PRIMARY KEY,
    audit_cycle_id  INT NOT NULL REFERENCES audit_cycles(id) ON DELETE CASCADE,
    auditor_id      INT NOT NULL REFERENCES users(id),
    assigned_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (audit_cycle_id, auditor_id)
);

-- =====================================================================
-- 15. AUDIT ITEMS  (per-asset verification + discrepancy tracking)
-- =====================================================================
CREATE TABLE audit_items (
    id                 SERIAL PRIMARY KEY,
    audit_cycle_id     INT NOT NULL REFERENCES audit_cycles(id) ON DELETE CASCADE,
    asset_id           INT NOT NULL REFERENCES assets(id),
    auditor_id         INT REFERENCES users(id),
    result             audit_result,                -- NULL until checked; Verified/Missing/Damaged
    remarks            TEXT,
    checked_at         TIMESTAMPTZ,
    resolution_status  resolution_status NOT NULL DEFAULT 'Open',  -- relevant when result <> Verified
    resolved_by        INT REFERENCES users(id),     -- Asset Manager
    resolved_at        TIMESTAMPTZ,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (audit_cycle_id, asset_id)
);

CREATE INDEX idx_audit_items_cycle    ON audit_items(audit_cycle_id);
CREATE INDEX idx_audit_items_flagged  ON audit_items(result) WHERE result IN ('Missing','Damaged');

-- =====================================================================
-- 16. NOTIFICATIONS
-- =====================================================================
CREATE TABLE notifications (
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type            VARCHAR(50) NOT NULL,   -- Asset Assigned, Maintenance Approved, Booking Reminder, etc.
    title           VARCHAR(150) NOT NULL,
    message         TEXT NOT NULL,
    reference_type  VARCHAR(50),            -- Allocation, Booking, Maintenance, Transfer, Audit
    reference_id    INT,
    is_read         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_notifications_user_read ON notifications(user_id, is_read);

-- =====================================================================
-- 17. ACTIVITY LOGS  (full audit log of who did what, when)
-- =====================================================================
CREATE TABLE activity_logs (
    id           SERIAL PRIMARY KEY,
    user_id      INT REFERENCES users(id) ON DELETE SET NULL,
    action       VARCHAR(100) NOT NULL,     -- e.g. CREATE_ASSET, APPROVE_MAINTENANCE
    entity_type  VARCHAR(50) NOT NULL,
    entity_id    INT,
    details      JSONB,
    ip_address   VARCHAR(64),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_activity_entity ON activity_logs(entity_type, entity_id);
CREATE INDEX idx_activity_user   ON activity_logs(user_id);

-- =====================================================================
-- TRIGGER FUNCTIONS
-- =====================================================================

-- Auto-maintain updated_at on every UPDATE
CREATE OR REPLACE FUNCTION set_updated_at() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_departments_updated_at   BEFORE UPDATE ON departments        FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_categories_updated_at    BEFORE UPDATE ON asset_categories   FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_users_updated_at         BEFORE UPDATE ON users              FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_assets_updated_at        BEFORE UPDATE ON assets             FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_allocations_updated_at   BEFORE UPDATE ON allocations        FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_transfers_updated_at     BEFORE UPDATE ON transfer_requests  FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_bookings_updated_at      BEFORE UPDATE ON resource_bookings  FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_maintenance_updated_at   BEFORE UPDATE ON maintenance_requests FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_audit_cycles_updated_at  BEFORE UPDATE ON audit_cycles       FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER trg_audit_items_updated_at   BEFORE UPDATE ON audit_items        FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Auto-generate Asset Tag on insert, e.g. AF-0001, AF-0002 ...
CREATE OR REPLACE FUNCTION generate_asset_tag() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.asset_tag IS NULL THEN
        NEW.asset_tag := 'AF-' || LPAD(nextval('asset_tag_seq')::text, 4, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_generate_asset_tag BEFORE INSERT ON assets
    FOR EACH ROW EXECUTE FUNCTION generate_asset_tag();

-- Auto-log every asset lifecycle status change (Available <-> Under Maintenance, etc.)
CREATE OR REPLACE FUNCTION log_asset_status_change() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status IS DISTINCT FROM OLD.status THEN
        INSERT INTO asset_status_history(asset_id, old_status, new_status, reference_type, changed_at)
        VALUES (NEW.id, OLD.status, NEW.status, 'Manual', now());
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_asset_status_change AFTER UPDATE ON assets
    FOR EACH ROW EXECUTE FUNCTION log_asset_status_change();

-- =====================================================================
-- CONVENIENCE VIEWS (optional, power the Dashboard KPI cards)
-- =====================================================================

-- Allocations that are still Active but past their expected return date
CREATE OR REPLACE VIEW v_overdue_allocations AS
SELECT a.*
FROM allocations a
WHERE a.status = 'Active'
  AND a.expected_return_date IS NOT NULL
  AND a.expected_return_date < CURRENT_DATE;

-- Upcoming bookings starting soon (useful for reminder notifications)
CREATE OR REPLACE VIEW v_upcoming_bookings AS
SELECT b.*
FROM resource_bookings b
WHERE b.status = 'Upcoming'
  AND b.start_time > now();

-- Dashboard KPI counts
CREATE OR REPLACE VIEW v_dashboard_kpis AS
SELECT
    (SELECT COUNT(*) FROM assets WHERE status = 'Available')              AS assets_available,
    (SELECT COUNT(*) FROM assets WHERE status = 'Allocated')              AS assets_allocated,
    (SELECT COUNT(*) FROM maintenance_requests
        WHERE status IN ('Approved','Technician Assigned','In Progress')
        AND (technician_assigned_at::date = CURRENT_DATE OR in_progress_at::date = CURRENT_DATE)) AS maintenance_today,
    (SELECT COUNT(*) FROM resource_bookings WHERE status IN ('Upcoming','Ongoing')) AS active_bookings,
    (SELECT COUNT(*) FROM transfer_requests WHERE status = 'Requested')   AS pending_transfers,
    (SELECT COUNT(*) FROM allocations
        WHERE status = 'Active' AND expected_return_date >= CURRENT_DATE
        AND expected_return_date <= CURRENT_DATE + INTERVAL '7 days')     AS upcoming_returns,
    (SELECT COUNT(*) FROM v_overdue_allocations)                          AS overdue_returns;

-- =====================================================================
-- END OF SCHEMA
-- =====================================================================
