# DevSecOps Demo

Минимальное FastAPI-приложение для РГР по DevSecOps.

## Запуск локально

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Откройте `http://127.0.0.1:8000`.

Демо-логин: `admin`  
Демо-пароль: `admin123`

## Docker

```powershell
docker build -t devsecops-demo .
docker run --rm -p 8000:8000 devsecops-demo
```

Что сделано по безопасности:

- базовый образ `python:3.12-slim`;
- приложение запускается от пользователя `appuser`, а не от root;
- в финальный образ копируется только приложение;
- открыт только порт `8000`;
- пароль проверяется по PBKDF2-хэшу;
- добавлены `X-Frame-Options`, `Content-Security-Policy`, `Strict-Transport-Security`;
- HTTPS-redirect включается переменной `FORCE_HTTPS=true`.
