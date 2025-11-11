# VT (Vive Trading)
FastAPI(Backend)와 React(Frontend)를 사용하는 풀스택 애플리케이션입니다.

---

## 준비물
| 항목 | 내용 |
|---|---|
| OS | Ubuntu 24.04 (권장) |
| 필수 프로그램 | Docker, Docker Compose |
| 네트워크 | Port `3000`, `8000` 오픈 |

---

## 설치 및 실행 방법

### 1) 프로젝트 클론
```bash
git clone https://github.com/totalcream/VT.git
cd VT
```

### 2) 애플리케이션 실행
아래 명령어 하나로 백엔드와 프론트엔드 서비스가 모두 빌드되고 실행됩니다.
```bash
docker compose up --build -d
```

### 3) 실행 확인
```bash
docker compose ps
```

예시 출력:
```
NAME                IMAGE               COMMAND                  SERVICE             CREATED             STATUS              PORTS
fastapi_test_prj-backend-1    fastapi_test_prj-backend    "uvicorn main:app --…"   backend             2 minutes ago       Up 2 minutes        0.0.0.0:8000->8000/tcp
fastapi_test_prj-frontend-1   fastapi_test_prj-frontend   "nginx -g 'daemon of…"   frontend            2 minutes ago       Up 2 minutes        0.0.0.0:3000->80/tcp
```

---

## 접속 방법

| 환경 | 접속 URL |
|---|---|
| 로컬 접속 | http://localhost:3000 |
| 외부 IP 접속 | http://<서버-IP>:3000 |

---

## 컨테이너 관리

| 작업 | 명령어 |
|---|---|
| 전체 서비스 중지 | `docker compose stop` |
| 전체 서비스 내리기 (중지 및 컨테이너 삭제) | `docker compose down` |
| 전체 서비스 로그 확인 | `docker compose logs -f` |
| 특정 서비스 로그 확인 (예: frontend) | `docker compose logs -f frontend` |
