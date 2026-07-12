"""
File Upload Handling

Purpose
-------
Safely store uploaded files (asset photos/documents, maintenance photos) to disk under app/uploads/, with validation.

Responsibilities
-----------------
- save_upload(file, subfolder): validate file type/size, write to app/uploads/<subfolder>/, return a URL/path.
- Guard against path traversal and disallowed file types.

Interacts With
--------------
- services/asset_service.py -> upload_document().
- services/maintenance_service.py -> maintenance photo_url.
- config.py -> UPLOAD_PATH setting.
- lifespan.py -> ensures the target directories exist on startup.
"""

import re
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config import settings
from app.core.exceptions import ValidationError

# Extensions allowed for asset photos, invoices, manuals, maintenance photos, etc.
_ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".doc", ".docx"}
_MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB

# Only allow simple, predictable subfolder names (no path traversal via subfolder either).
_SAFE_SUBFOLDER_RE = re.compile(r"^[a-zA-Z0-9_-]+$")


async def save_upload(file: UploadFile, subfolder: str) -> str:
    """Validate and persist an uploaded file under app/uploads/<subfolder>/, returning its stored URL/path."""
    if not _SAFE_SUBFOLDER_RE.match(subfolder):
        raise ValidationError(f"Invalid upload subfolder: '{subfolder}'.")

    original_name = file.filename or ""
    extension = Path(original_name).suffix.lower()
    if extension not in _ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file type '{extension}'. Allowed types: {', '.join(sorted(_ALLOWED_EXTENSIONS))}."
        )

    contents = await file.read()
    if len(contents) > _MAX_UPLOAD_BYTES:
        raise ValidationError(f"File exceeds maximum allowed size of {_MAX_UPLOAD_BYTES // (1024 * 1024)} MB.")
    if not contents:
        raise ValidationError("Uploaded file is empty.")

    target_dir = Path(settings.UPLOAD_PATH) / subfolder
    target_dir.mkdir(parents=True, exist_ok=True)

    # Generate a collision-proof, traversal-proof filename; never trust the client's name.
    stored_name = f"{uuid.uuid4().hex}{extension}"
    target_path = target_dir / stored_name

    with open(target_path, "wb") as out_file:
        out_file.write(contents)

    return f"{subfolder}/{stored_name}"