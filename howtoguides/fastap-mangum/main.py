from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum
from typing import Dict

app = FastAPI(title="Role Configuration Service")
# Mangum handler will be used by Lambda
handler = Mangum(app)


# 🌟 New welcome endpoint
@app.get("/", summary="Welcome")
async def welcome():
    return {"message": "Welcome to the Role Configuration Service!"}


# In-memory “database”
DB: Dict[str, "RoleConfig"] = {}


class RoleConfig(BaseModel):
    roleId: str
    role: str
    accountId: str
    environment: str


@app.get("/role_configuration", response_model=list[RoleConfig])
async def list_role_configurations():
    return list(DB.values())


@app.get("/role_configuration/{role_id}", response_model=RoleConfig)
async def get_role_configuration(role_id: str):
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
    existing = DB.get(role_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Role configuration not found")
    if patch.roleId != role_id:
        raise HTTPException(
            status_code=400, detail="Path role_id must match body.roleId"
        )
    DB[role_id] = patch
    return patch
