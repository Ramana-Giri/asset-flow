"""
Asset Categories Router

Purpose
-------
HTTP endpoints for the Asset Categories module, mounted under prefix "/asset-categories".

Responsibilities
-----------------
- Receive the HTTP request and validate it against the Pydantic schema.
- Delegate ALL business logic to AssetCategoryService - routers never contain business rules or SQL.
- Translate domain exceptions (core/exceptions.py) into HTTP error responses.
- Wrap successful results in the standard {success, message, data} envelope (core/responses.py).

Interacts With
--------------
- schemas/asset_categories.py -> request/response models.
- services/asset_categories_service.py -> AssetCategoryService, injected via dependencies.py.
- dependencies.py -> get_current_user() / role-guard dependencies applied per-route as needed.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/asset-categories", tags=["Asset Categories"])

# Role-guard dependencies (from dependencies.py: get_current_user,
# get_current_admin, get_current_asset_manager, get_current_department_head)
# would be added per-route via `Depends(...)` where the requirements
# specify a role restriction (see docstrings below).


@router.get("")
async def list_categories():
    """
    List asset categories (Screen 3, Tab B).

    Flow: receive request -> validate schema -> call AssetCategoryService.list_categories() -> return standard envelope.
    """
    pass

@router.get("/{category_id}")
async def get_category():
    """
    Fetch a single category.

    Flow: receive request -> validate schema -> call AssetCategoryService.get_category() -> return standard envelope.
    """
    pass

@router.post("")
async def create_category():
    """
    Admin-only: create a category incl. custom_field_schema.

    Flow: receive request -> validate schema -> call AssetCategoryService.create_category() -> return standard envelope.
    """
    pass

@router.put("/{category_id}")
async def update_category():
    """
    Admin-only: edit a category.

    Flow: receive request -> validate schema -> call AssetCategoryService.update_category() -> return standard envelope.
    """
    pass

@router.delete("/{category_id}")
async def delete_category():
    """
    Admin-only: delete an unused category.

    Flow: receive request -> validate schema -> call AssetCategoryService.delete_category() -> return standard envelope.
    """
    pass
