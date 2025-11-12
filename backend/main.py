from fastapi import FastAPI, APIRouter

# Import routers from the new structure
from app.api.endpoints import llm, market, trading

app = FastAPI(
    title="VT Backend API",
    description="API for vLLM, Upbit, and Trading functionalities",
    version="0.1.0",
)

# Create a main API router
api_router = APIRouter() # Removed prefix="/api" here, as it's handled by the main app.include_router

# Include specific routers
api_router.include_router(llm.router, prefix="/llm", tags=["LLM"])
api_router.include_router(market.router, prefix="/market", tags=["Market Data"])
api_router.include_router(trading.router, prefix="/trading", tags=["Trading"])

# Include the main API router in the FastAPI app
app.include_router(api_router, prefix="/api") # Added prefix="/api" here

# Root endpoint for health check or basic info
@app.get("/")
async def root():
    return {"message": "VT Backend API is running"}
