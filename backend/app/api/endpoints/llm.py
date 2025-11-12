from fastapi import APIRouter, HTTPException
from app.schemas.llm import LLMRequest, TradeDecision
from app.services import vllm_service

router = APIRouter()

@router.post("/trade-decision", response_model=TradeDecision)
async def generate_trade_decision(request: LLMRequest):
    """
    사용자 데이터와 모델 이름을 받아 vLLM에 트레이딩 결정을 요청하고,
    검증된 JSON 형식의 트레이딩 결정을 반환합니다.
    """
    try:
        # 서비스 함수에 모델 이름과 프롬프트를 전달
        decision = await vllm_service.get_trade_decision(
            user_data_prompt=request.user_data_prompt,
            model_name=request.model_name
        )
        return decision
    except ValueError as e:
        # 서비스에서 발생한 특정 오류(예: JSON 파싱 실패) 처리
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # 기타 예외 처리
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")