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
"""

import secrets

from passlib.context import CryptContext

from app.config import settings

# A single shared CryptContext, configured with the rounds from settings so
# BCRYPT_ROUNDS can be tuned per-environment (e.g. lower for local dev/tests)
# without touching this module.
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=settings.BCRYPT_ROUNDS)

# Length (in bytes, before URL-safe base64 encoding) of generated session
# tokens. 32 random bytes -> a 43-character token, comfortably fitting the
# VARCHAR(255) session_token column and providing ample entropy.