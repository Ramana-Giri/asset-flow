# AssetFlow Backend (Skeleton)

Generated FastAPI project structure for the AssetFlow Enterprise Asset &
Resource Management System, following the layered architecture:

```
Router -> Service -> Repository -> Database
```

## Scope of this scaffold

Every `.py` file in this tree contains **structure and documentation
only**: module docstrings (Purpose / Responsibilities / Interactions),
class and function signatures, and per-function docstrings describing
the exact orchestration steps derived from the functional requirements.
Method bodies are intentionally left as `pass` - no business logic, SQL,
or validation code has been implemented, per generation scope.

## Key architectural notes

- **No JWT.** Authentication is session-token based, backed by the
  `user_sessions` table in `assetflow_schema.sql`. `core/security.py`
  only hashes/verifies passwords and generates opaque session tokens;
  `dependencies.py` resolves the current user from that token.
- **`assetflow_schema.sql` is the source of truth** for tables, enums,
  constraints (partial-unique no-double-allocation index, GiST
  EXCLUDE no-overlapping-bookings constraint, asset-tag trigger,
  status-history trigger) - the ORM models mirror it, they do not
  redefine it.
- **Routers never contain business logic.** All rules (allocation
  conflicts, overlap checks, approval workflows, audit closure, etc.)
  are documented step-by-step inside the relevant `services/*.py`
  method docstrings.

## Layout

```
app/
  main.py, lifespan.py, config.py, dependencies.py
  core/        security, permissions, enums, constants, exceptions, responses, logging
  db/          engine/session, declarative base, models/ (one file per table)
  api/v1/      one router per module
  schemas/     one module per business capability (Create/Update/Response/List/Filter)
  repositories/one repository per major entity
  services/    one service per module (business rules live here)
  utils/       pagination, filters, validators, qr_generator, file_upload, date_utils
  uploads/     assets/, maintenance/
alembic/       migration environment (schema.sql-first; wired for future changes)
```

## Next steps to make this runnable

1. Fill in `db/models/*.py` with `Mapped`/`mapped_column`/`relationship`
   definitions matching `assetflow_schema.sql`.
2. Fill in `schemas/*.py` field declarations + validation.
3. Implement `repositories/*.py` query methods.
4. Implement `services/*.py` orchestration per the docstrings.
5. Wire `dependencies.py`, `core/security.py`, `core/responses.py`,
   `core/exceptions.py`.
6. Implement router bodies in `api/v1/*.py` and mount them in
   `api/router.py`.
