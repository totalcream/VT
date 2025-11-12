from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_llm_root():
    return {"message": "LLM endpoint root"}

@router.post("/generate")
async def generate_text():
    return {"message": "Generate text with LLM"}
