from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # vLLM 서버의 base URL. 환경 변수에서 읽어옵니다.
    # 예: VLLM_BASE_URL="https://unmummied-keshia-feelingly.ngrok-free.dev/v1"
    VLLM_BASE_URL: str = "https://unmummied-keshia-feelingly.ngrok-free.dev/v1"
    
    # vLLM API 키 (필요한 경우). 현재는 비워둡니다.
    VLLM_API_KEY: str = ""

    # .env 파일을 읽도록 설정 (선택 사항)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

# 설정 객체 생성
settings = Settings()
