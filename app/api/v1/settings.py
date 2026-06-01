from fastapi import APIRouter
from pydantic import BaseModel
import app.agents.personal_chief as _agent_module

router = APIRouter()


class WebSearchToggle(BaseModel):
    enabled: bool


class SettingsResponse(BaseModel):
    web_search_enabled: bool


@router.get("/settings")
async def get_settings():
    return {"web_search_enabled": _agent_module.web_search_enabled}


@router.post("/settings/web-search")
async def toggle_web_search(body: WebSearchToggle):
    _agent_module.web_search_enabled = body.enabled
    return {"web_search_enabled": _agent_module.web_search_enabled}
