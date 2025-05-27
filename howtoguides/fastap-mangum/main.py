from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum
from typing import Dict

app = FastAPI(title="Role Configuration Service")

# In-memory “database”
DB: Dict[str, "RoleConfig"] = {}


class RoleConfig(BaseModel):
    roleId: str
    role: str
    accountId: str
    environment: str


@app.get("/role_configuration", response_model=list[RoleConfig])
async def list_role_configurations():
    """
    Return all role configurations.
    """
    return list(DB.values())


@app.get("/role_configuration/{role_id}", response_model=RoleConfig)
async def get_role_configuration(role_id: str):
    """
    Return a single RoleConfig by its roleId.
    """
    cfg = DB.get(role_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Role configuration not found")
    return cfg


@app.post(
    "/role_configuration/{role_id}",
    status_code=201,
    response_model=RoleConfig,
)
async def create_role_configuration(role_id: str, config: RoleConfig):
    """
    Create a new RoleConfig. The path role_id must match the body.roleId.
    """
    if role_id in DB:
        raise HTTPException(status_code=400, detail="Role configuration already exists")
    if config.roleId != role_id:
        raise HTTPException(
            status_code=400, detail="Path role_id must match body.roleId"
        )
    DB[role_id] = config
    return config


@app.patch("/role_configuration/{role_id}", response_model=RoleConfig)
async def update_role_configuration(role_id: str, patch: RoleConfig):
    """
    Update an existing RoleConfig. Only existing entries can be patched.
    """
    existing = DB.get(role_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Role configuration not found")
    if patch.roleId != role_id:
        raise HTTPException(
            status_code=400, detail="Path role_id must match body.roleId"
        )
    # Overwrite fields
    DB[role_id] = patch
    return patch


# Mangum handler will be used by Lambda
handler = Mangum(app)
