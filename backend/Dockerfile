# Python 3.11-slim 이미지를 기반으로 합니다.
FROM python:3.11-slim

# 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# requirements.txt 파일을 컨테이너의 /app 디렉토리로 복사합니다.
COPY requirements.txt .

# 복사된 requirements.txt 파일을 사용하여 의존성을 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# main.py 파일을 컨테이너의 /app 디렉토리로 복사합니다.
COPY main.py .

# 컨테이너의 8000번 포트를 외부에 노출합니다.
EXPOSE 8000

# uvicorn을 사용하여 FastAPI 애플리케이션을 실행합니다.
# 0.0.0.0 호스트를 사용하여 컨테이너 외부에서도 접근할 수 있도록 합니다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
