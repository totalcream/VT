from pydantic import BaseModel, Field
from typing import Literal

# 사용 가능한 모델 이름들을 Literal 타입으로 정의
ModelName = Literal[
    "google/gemma-3-27b-it",
    "openai/gpt-oss-120b",
    "Qwen/Qwen3-30B-A3B-Thinking-2507-FP8",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
]

# LLM의 응답 JSON 구조를 검증하기 위한 Pydantic 모델
class TradeDecision(BaseModel):
    stop_loss: float
    signal: Literal["buy_to_enter", "sell_to_enter", "hold", "close_position"]
    leverage: int
    risk_usd: float
    profit_target: float
    quantity: float
    invalidation_condition: str
    justification: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    coin: str

# 우리 API가 받을 요청 본문의 구조 (model_name 추가)
class LLMRequest(BaseModel):
    user_data_prompt: str
    model_name: ModelName = "openai/gpt-oss-120b" # 기본값을 gpt-oss-120b로 설정