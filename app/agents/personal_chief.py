from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessageChunk, AIMessage
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from app.common.logger import logger
from app.rag.vector_store import RecipeVectorStore
from app.skills.registry import skill_registry
import os
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# Initialize checkpointer
db_path = os.path.join(os.path.dirname(__file__), "..", "db", "personal_chief.db")
checkpointer = SqliteSaver(sqlite3.connect(db_path, check_same_thread=False))
checkpointer.setup()

# RAG local recipe knowledge base
_rag_store = RecipeVectorStore(
    db_path=db_path,
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    api_key=os.getenv("DASHSCOPE_API_KEY")
)


@tool
def search_recipe_knowledge(query: str) -> str:
    """Search the local healthy recipe knowledge base for recipes matching the query.

    Use this tool FIRST before web_search when looking for recipes. The knowledge base
    contains curated healthy recipes with nutrition info, difficulty, cooking time,
    and step-by-step instructions. If results are insufficient or don't match the
    user's ingredients, then fall back to web_search.

    Args:
        query: A search query describing the desired recipe, ingredients, or cuisine.
               Examples: "high protein chicken dinner", "low carb vegetarian lunch",
               "quick Mediterranean breakfast".
    """
    try:
        results = _rag_store.search(query, top_k=5)
        if not results:
            return "No matching recipes found in the local knowledge base. Try web_search instead."

        output_parts = []
        for i, r in enumerate(results, 1):
            output_parts.append(
                f"{i}. **{r['name']}** [{r['cuisine']}] "
                f"(Difficulty: {r['difficulty']}, Time: {r['cooking_time']}min)\n"
                f"   Ingredients: {r['ingredients']}\n"
                f"   Nutrition: {r['nutrition']}\n"
                f"   Tags: {r['tags']}\n"
                f"   Steps: {r['steps']}\n"
            )
        return "=== LOCAL RECIPE KNOWLEDGE BASE RESULTS ===\n\n" + "\n".join(output_parts)
    except Exception as e:
        logger.error(f"RAG search failed: {e}")
        return f"Recipe knowledge search error: {e}. Please use web_search instead."


@tool
async def use_skill(skill_name: str, input_text: str) -> str:
    """Execute a specialized skill for recipe-related tasks.

    Use this tool when the user requests nutrition analysis, shopping lists,
    meal planning, or ingredient substitutions. First call with
    skill_name="__list__" to see all available skills and their descriptions.

    Args:
        skill_name: The name of the skill. Use "__list__" to list all skills.
        input_text: The input for the skill (recipe name, ingredients, preferences).
    """
    if skill_name == "__list__":
        available = skill_registry.get_available_skills_text()
        return f"AVAILABLE SKILLS:\n{available}\n\nTo use a skill, call use_skill again with the desired skill_name and your input_text."

    skill = skill_registry.get(skill_name)
    if skill is None:
        available = skill_registry.get_available_skills_text()
        return f"Unknown skill '{skill_name}'.\n\nAVAILABLE SKILLS:\n{available}"

    if not skill.enabled:
        return f"Skill '{skill_name}' is currently disabled. Use __list__ to see enabled skills."

    try:
        result = await skill.handler(input_text)
        return result
    except Exception as e:
        logger.error(f"Skill '{skill_name}' failed: {e}")
        return f"Skill '{skill_name}' error: {str(e)}"


# Web search toggle (module-level, can be changed via API)
web_search_enabled = True

# Underlying Tavily search engine
_tavily_search = TavilySearch(
    max_results=3,
    topic="general"
)


@tool
def web_search(query: str) -> str:
    """Search the web for recipes and food information.

    Use this tool to find recipes, nutritional information, and cooking tips
    from the internet. This is a fallback after the local recipe knowledge base.
    If web search is disabled, you will be informed and should rely on the
    local knowledge base instead.

    Args:
        query: The search query for finding recipes or food information online.
    """
    if not web_search_enabled:
        return (
            "Web search is currently DISABLED by the user. "
            "Please rely on the local recipe knowledge base (search_recipe_knowledge) "
            "and your own knowledge instead. Do not attempt web_search again."
        )
    try:
        return _tavily_search.invoke(query)
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return f"Web search error: {e}. Please use local knowledge base instead."


# Multimodal model
model = init_chat_model(
    model="qwen3-omni-flash",
    model_provider="openai",
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    api_key=os.getenv("DASHSCOPE_API_KEY")
)


# Agent system prompt
system_prompt = """
You are a personal chef. When the user provides ingredient photos or a list, follow this workflow:

1. Identify and assess ingredients: If a photo is provided, first identify all visible ingredients.
   Based on their appearance, assess freshness and quantity, and compile a list of available ingredients.

2. Smart recipe search (two-step):
   a. FIRST call search_recipe_knowledge to search the local healthy recipe knowledge base
      using the available ingredients. The local database contains curated fitness/healthy recipes
      with nutrition values and difficulty ratings.
   b. If local results are insufficient or don't match the user's ingredients, THEN fall back to
      web_search for supplementary web results.

3. Multi-dimensional evaluation and ranking: Score candidate recipes on nutrition value and
   cooking difficulty. Rank by score, prioritizing easy-to-make and nutritious recipes.

4. Structured output: Present the ranked recipes as a clear recommendation report, including
   recipe info, scores, reasons for recommendation, and reference images.

5. Specialized skills: You have access to a use_skill tool. Call use_skill with
   skill_name="__list__" first to discover available skills. Use skills for nutrition
   analysis, shopping list generation, meal planning, and ingredient substitutions
   when the user's request matches a skill's purpose.

Always follow the priority: local knowledge base first, then web search.
"""

# Create agent
agent = create_agent(
    model=model,
    tools=[search_recipe_knowledge, web_search, use_skill],
    checkpointer=checkpointer,
    system_prompt=system_prompt
)


# Streaming chat
async def search_recipes(prompt: str, image: str, thread_id: str):
    """Invoke agent to search recipes"""
    logger.info(f"[user]: {prompt}, image: {image}, thread_id: {thread_id}")
    try:
        if not image or image.strip() == "":
            message = HumanMessage(content=prompt)
        else:
            message = HumanMessage(content=[
                {"type": "image", "url": image},
                {"type": "text", "text": prompt}
            ])

        for chunk, metadata in agent.stream(
            {"messages": [message]},
            {"configurable": {"thread_id": thread_id}},
            stream_mode="messages"
        ):
            if isinstance(chunk, AIMessageChunk) and chunk.content:
                yield chunk.content

    except Exception as e:
        logger.error(f"\n[error]: {str(e)}")
        yield "Search failed, try entering your ingredient list manually?"


# Clear session
def clear_messages(thread_id: str):
    """Clear chat history"""
    logger.info(f"Clearing history, thread_id: {thread_id}")
    checkpointer.delete_thread(thread_id)


# Query session history
def get_messages(thread_id: str) -> list[dict[str, str]]:
    """Get chat history"""
    logger.info(f"Getting history, thread_id: {thread_id}")

    checkpoint = checkpointer.get({"configurable": {"thread_id": thread_id}})

    if not checkpoint:
        return []

    channel_values = checkpoint.get("channel_values")
    if not channel_values:
        return []

    messages = channel_values.get("messages", [])
    if not messages:
        return []

    result = []
    for msg in messages:
        if not msg.content:
            continue

        if isinstance(msg, HumanMessage):
            result.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            result.append({"role": "assistant", "content": msg.content})

    return result
