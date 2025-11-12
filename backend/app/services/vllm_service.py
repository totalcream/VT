import json
from openai import OpenAI
from app.core.config import settings
from app.schemas.llm import TradeDecision

# 1. OpenAI 클라이언트 초기화 (설정 파일 사용)
client = OpenAI(
    base_url=settings.VLLM_BASE_URL,
    api_key=settings.VLLM_API_KEY,
)

# 2. 시스템 프롬프트 (규칙)
# 사용자가 제공한 프롬프트를 상수로 정의
SYSTEM_PROMPT = """
You are an expert AI trading analyst. Your goal is to analyze the market data provided and decide on a single, actionable trade.

You MUST follow this exact process:

1.  **Think (Chain-of-Thought):**
    First, think step-by-step about the provided data. Your thought process must be private, inside <thinking>...</thinking> tags.
    Your analysis MUST cover:
    - Current Position Analysis: Review any existing positions, PnL, and invalidation conditions.
    - Market Analysis: Analyze the provided data for BTC and other major coins (ETH, SOL, etc.).
    - Strategic Assessment: Synthesize all data to find the best trading opportunity.
    - Actionable Decision: Formulate a specific, justified trade with risk parameters.

2.  **Act (JSON Output):**
    After your <thinking> block, you MUST output ONLY a single JSON object with the trade decision.
    Do NOT write any other text or explanation outside the JSON block.
    The JSON structure MUST be:

    {{
        "stop_loss": <float>,
        "signal": "<buy_to_enter | sell_to_enter | hold | close_position>",
        "leverage": <int>,
        "risk_usd": <float>,
        "profit_target": <float>,
        "quantity": <float>,
        "invalidation_condition": "<string>",
        "justification": "<string - a brief summary of your CoT rationale>",
        "confidence": <float between 0.0 and 1.0>,
        "coin": "<string, e.g., BTC, ETH>"
    }}
"""

# 3. vLLM 호출 및 결과 파싱/검증을 위한 서비스 함수
async def get_trade_decision(user_data_prompt: str, model_name: str) -> TradeDecision:
    """
    vLLM에 접속하여 트레이딩 결정을 요청하고, 결과를 검증하여 반환합니다.
    """
    try:
        completion = client.chat.completions.create(
            model=model_name, # 전달받은 모델 이름 사용
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_data_prompt}
            ],
            temperature=0.0
        )
        
        raw_content = completion.choices[0].message.content
        
        # <thinking> 태그와 JSON 부분 분리
        # LLM이 항상 JSON만 출력하도록 제어하는 것이 가장 좋지만,
        # CoT가 포함될 경우를 대비하여 JSON 부분만 추출합니다.
        json_part = raw_content
        if "</thinking>" in raw_content:
            json_part = raw_content.split("</thinking>")[-1].strip()
            
        # JSON 파싱
        decision_data = json.loads(json_part)
        
        # Pydantic 모델로 데이터 유효성 검증
        validated_decision = TradeDecision(**decision_data)
        
        return validated_decision

    except json.JSONDecodeError as e:
        # LLM이 유효한 JSON을 반환하지 않은 경우
        print(f"JSON Decode Error: {e}")
        print(f"Raw LLM output: {raw_content}")
        raise ValueError("LLM did not return valid JSON.")
    except Exception as e:
        # 기타 API 호출 오류 등
        print(f"An error occurred while communicating with vLLM: {e}")
        raise
