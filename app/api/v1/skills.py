from fastapi import APIRouter, HTTPException
from app.models.schemas import SkillInfo, SkillListResponse, SkillToggleRequest
from app.skills.registry import skill_registry

router = APIRouter()


@router.get("/skills", response_model=SkillListResponse)
async def list_skills():
    all_skills = skill_registry.list_all()
    return SkillListResponse(skills=[
        SkillInfo(
            name=s.name,
            display_name=s.display_name,
            description=s.description,
            enabled=s.enabled
        )
        for s in all_skills
    ])


@router.post("/skills/{name}/toggle")
async def toggle_skill(name: str, req: SkillToggleRequest):
    if not skill_registry.toggle(name, req.enabled):
        raise HTTPException(status_code=404, detail="Skill not found")
    skill = skill_registry.get(name)
    return {
        "success": True,
        "skill": {
            "name": skill.name,
            "display_name": skill.display_name,
            "enabled": skill.enabled
        }
    }
