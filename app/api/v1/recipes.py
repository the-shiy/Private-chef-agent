from fastapi import APIRouter, HTTPException, Query

from app.models.schemas import (
    RecipeCreate, RecipeUpdate, RecipeResponse, RecipeListResponse
)
from app.db import recipes_db
from app.rag.vector_store import RecipeVectorStore
import os

router = APIRouter()


def _get_vector_store() -> RecipeVectorStore:
    db_path = os.path.join(os.path.dirname(__file__), "..", "..", "db", "personal_chief.db")
    return RecipeVectorStore(
        db_path=db_path,
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )


@router.get("/recipes", response_model=RecipeListResponse)
async def list_recipes(
    cuisine: str = None,
    difficulty: str = None,
    search: str = None,
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0)
):
    recipes = recipes_db.list_all(
        cuisine=cuisine, difficulty=difficulty,
        search=search, limit=limit, offset=offset
    )
    total = recipes_db.count()
    return RecipeListResponse(total=total, recipes=recipes)


@router.get("/recipes/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: str):
    recipe = recipes_db.get_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/recipes", status_code=201, response_model=RecipeResponse)
async def create_recipe(recipe: RecipeCreate):
    data = recipe.model_dump()
    if not recipes_db.insert(data):
        raise HTTPException(status_code=409, detail="Recipe ID already exists")
    store = _get_vector_store()
    store.add_recipe(data)
    store.close()
    return recipes_db.get_by_id(recipe.id)


@router.put("/recipes/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(recipe_id: str, recipe: RecipeUpdate):
    existing = recipes_db.get_by_id(recipe_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Recipe not found")
    # Merge: update only provided fields
    update_data = recipe.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    recipes_db.update(recipe_id, update_data)
    # Re-sync vector index
    updated = recipes_db.get_by_id(recipe_id)
    store = _get_vector_store()
    store.update_recipe(recipe_id, updated)
    store.close()
    return updated


@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: str):
    if not recipes_db.delete(recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")
    store = _get_vector_store()
    store.delete_recipe(recipe_id)
    store.close()
    return {"success": True}


@router.post("/recipes/seed")
async def seed_recipes():
    from app.rag.recipes_seed import SEED_RECIPES
    count = recipes_db.seed_from_dicts(SEED_RECIPES)
    store = _get_vector_store()
    store.rebuild(recipes_db.get_all_as_dicts())
    store.close()
    return {"seeded": count, "total": recipes_db.count()}
