from dataclasses import dataclass
from typing import Callable, Awaitable
from app.common.logger import logger


@dataclass
class Skill:
    name: str
    display_name: str
    description: str
    handler: Callable[..., Awaitable[str]]
    enabled: bool = True
    requires_recipe_db: bool = False


class SkillRegistry:
    """Singleton registry for pluggable agent skills."""
    _instance: "SkillRegistry | None" = None

    def __new__(cls) -> "SkillRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._skills: dict[str, Skill] = {}
        return cls._instance

    def register(self, skill: Skill) -> None:
        self._skills[skill.name] = skill

    def unregister(self, name: str) -> bool:
        if name in self._skills:
            del self._skills[name]
            return True
        return False

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name)

    def list_all(self) -> list[Skill]:
        return list(self._skills.values())

    def list_enabled(self) -> list[Skill]:
        return [s for s in self._skills.values() if s.enabled]

    def toggle(self, name: str, enabled: bool) -> bool:
        skill = self._skills.get(name)
        if skill is None:
            return False
        skill.enabled = enabled
        logger.info(f"Skill '{name}' {'enabled' if enabled else 'disabled'}")
        return True

    def get_available_skills_text(self) -> str:
        enabled = self.list_enabled()
        if not enabled:
            return "No specialized skills are currently available."
        lines = []
        for s in enabled:
            lines.append(f"- {s.name}: {s.display_name} -- {s.description}")
        return "\n".join(lines)


skill_registry = SkillRegistry()
