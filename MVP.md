Register user
Authenticate user (login)
List all assets
Search assets (by name/category — pending your confirmation on A vs B)
Add asset
Book asset
Return asset


AssetFlow MVP — API Design (Final)
Auth
POST /auth/register
  Body:     { name, email, password }
  Response: 201 { message, emp_id, name, email }

POST /auth/login
  Body:     { email, password }
  Response: 200 { token, emp_id, name }
Assets
GET /assets
GET /assets?category=...
GET /assets?name=...
  (one endpoint, optional query params for filtering)
  Response: 200 [ { asset_id, name, category, status, assigned_to }, ... ]

POST /assets
  Body:     { name, category }
  Response: 201 { asset_id, name, category, status: "not assigned", assigned_to: null }

PATCH /assets/{asset_id}/book
  Auth:     JWT → emp_id
  Body:     none
  Response: 200 { asset_id, name, category, status: "assigned", assigned_to: emp_id }
  Errors:   404 (asset not found)
            409 { message: "Currently held by <name>", assigned_to }

PATCH /assets/{asset_id}/return
  Auth:     JWT → emp_id
  Body:     none
  Response: 200 { asset_id, name, category, status: "not assigned", assigned_to: null }
  Errors:   404 (asset not found)
            403 (not the current holder)
            409 (asset already not assigned)