"""
Password Security Helpers

Purpose
-------
Password hashing and verification only. NOTE: This project uses session-token based auth, NOT JWT - so no token-signing logic lives here or anywhere else in the app.

Responsibilities
-----------------
- hash_password(): bcrypt-hash a plaintext password (passlib).
- verify_password(): compare a plaintext password against a stored bcrypt hash.
- generate_session_token(): produce a cryptographically random, opaque session token string.
- This file should never perform database operations.

Interacts With
--------------
- services/auth_service.py -> the only caller of these helpers.
- config.py -> BCRYPT_ROUNDS setting.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using bcrypt (passlib CryptContext)."""
    pass


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify a plaintext password against its stored bcrypt hash."""
    pass


def generate_session_token() -> str:
    """Generate a cryptographically random, URL-safe opaque session token (NOT a JWT)."""
    pass
