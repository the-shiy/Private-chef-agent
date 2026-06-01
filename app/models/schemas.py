from typing import Optional
from pydantic import BaseModel


# --- Chat ---
class ChatRequest(BaseModel):
    message: str
    image_url: Optional[str] = None
    thread_id: str


# --- Recipe CRUD ---
class RecipeCreate(BaseModel):
    id: str
    name: str
    ingredients: str
    cuisine: str = "Western"
    difficulty: str = "easy"
    cooking_time: int = 0
    nutrition: str = ""
    steps: str = ""
    tags: str = ""


class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    ingredients: Optional[str] = None
    cuisine: Optional[str] = None
    difficulty: Optional[str] = None
    cooking_time: Optional[int] = None
    nutrition: Optional[str] = None
    steps: Optional[str] = None
    tags: Optional[str] = None


class RecipeResponse(BaseModel):
    id: str
    name: str
    ingredients: str
    cuisine: str
    difficulty: str
    cooking_time: int
    nutrition: str
    steps: str
    tags: str
    created_at: str = ""
    updated_at: str = ""


class RecipeListResponse(BaseModel):
    total: int
    recipes: list[RecipeResponse]


# --- Skills ---
class SkillInfo(BaseModel):
    name: str
    display_name: str
    description: str
    enabled: bool


class SkillListResponse(BaseModel):
    skills: list[SkillInfo]


class SkillToggleRequest(BaseModel):
    enabled: bool