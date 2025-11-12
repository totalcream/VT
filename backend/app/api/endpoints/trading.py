from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_trading_root():
    return {"message": "Trading endpoint root"}

@router.post("/order")
async def place_order():
    return {"message": "Placing a trade order"}
