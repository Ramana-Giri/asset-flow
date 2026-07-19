# Requirements and it's purpose
| Package | Purpose |
|---|---|
| `fastapi` | The web framework itself |
| `uvicorn` | The actual server that *runs* your FastAPI app |
| `sqlalchemy` | The ORM — lets Python talk to Postgres without raw SQL strings everywhere |
| `psycopg2-binary` | The low-level driver that actually connects Python to Postgres (SQLAlchemy uses this underneath) |
| `python-jose` | Creates and verifies JWT tokens (for login) |
| `passlib[bcrypt]` | Securely hashes passwords (never store plain-text passwords, remember) |
| `python-multipart` | Needed for FastAPI to parse form data (login forms, etc.) |
