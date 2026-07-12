"""
QR Code Generator

Purpose
-------
Generate a QR code identifying an asset (encoding, at minimum, the asset_tag/id) for the Asset Registration screen.

Responsibilities
-----------------
- generate_qr_code(asset_tag): produce a QR code image/payload and return a storable reference (qr_code column, and/or an image file path).

Interacts With
--------------
- services/asset_service.py -> called during register_asset().
- utils/file_upload.py -> may be used to persist the generated QR image.
"""

from pathlib import Path

import qrcode

from app.config import settings

_QR_SUBFOLDER = "qr"


def generate_qr_code(asset_tag: str) -> str:
    """Generate a QR code for the given asset_tag and return a reference string (a relative file path).

    The QR payload is the bare asset_tag (e.g. "AF-0001"), which scanners
    can resolve via the asset lookup screen/API. The image is written to
    <UPLOAD_PATH>/qr/<asset_tag>.png and the relative path is returned for
    storage in assets.qr_code.
    """
    qr_dir = Path(settings.UPLOAD_PATH) / _QR_SUBFOLDER
    qr_dir.mkdir(parents=True, exist_ok=True)

    image = qrcode.make(asset_tag)

    safe_name = asset_tag.replace("/", "_").replace("\\", "_")
    file_path = qr_dir / f"{safe_name}.png"
    image.save(file_path)

    return f"{_QR_SUBFOLDER}/{safe_name}.png"