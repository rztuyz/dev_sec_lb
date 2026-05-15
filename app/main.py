import os

from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.security import security_headers, verify_password


DEMO_USER = os.getenv("DEMO_USER", "admin")
DEMO_PASSWORD_HASH = os.getenv(
    "DEMO_PASSWORD_HASH",
    "pbkdf2_sha256$200000$ZGV2c2VjLWRlbW8tc2FsdA==$0NhPUD+/J3BVjk9kPHzwLNiIywpURoTKBh5FqntV9s4=",
)

app = FastAPI(title="DevSecOps Demo")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        for name, value in security_headers().items():
            response.headers[name] = value
        return response


app.add_middleware(SecurityHeadersMiddleware)


@app.middleware("http")
async def https_redirect(request: Request, call_next):
    if os.getenv("FORCE_HTTPS", "false").lower() == "true" and request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(str(url), status_code=status.HTTP_308_PERMANENT_REDIRECT)
    return await call_next(request)


def page(message: str = "") -> str:
    return f"""
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DevSecOps Demo</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f5f7fb; color: #172033; }}
    main {{ max-width: 760px; margin: 48px auto; padding: 0 18px; }}
    section {{ background: white; border: 1px solid #d8dee9; border-radius: 8px; padding: 24px; }}
    label {{ display: block; margin-top: 14px; font-weight: 700; }}
    input {{ width: 100%; box-sizing: border-box; padding: 10px; margin-top: 6px; border: 1px solid #b8c0cc; border-radius: 6px; }}
    button {{ margin-top: 18px; padding: 10px 16px; border: 0; border-radius: 6px; background: #1957a6; color: white; cursor: pointer; }}
    .msg {{ margin-top: 16px; padding: 10px; background: #eef5ff; border-left: 4px solid #1957a6; }}
    ul {{ line-height: 1.7; }}
  </style>
</head>
<body>
  <main>
    <section>
      <h1>DevSecOps Demo</h1>
      <p>Простое FastAPI-приложение для демонстрации требований РГР.</p>
      <ul>
        <li>пароль хранится как PBKDF2-хэш;</li>
        <li>ответы содержат security headers против кликджекинга;</li>
        <li>HTTPS-redirect включается через FORCE_HTTPS=true;</li>
        <li>контейнер запускается от непривилегированного пользователя.</li>
      </ul>
      <form method="post" action="/login">
        <label for="username">Логин</label>
        <input id="username" name="username" value="admin" autocomplete="username">
        <label for="password">Пароль</label>
        <input id="password" name="password" type="password" placeholder="admin123" autocomplete="current-password">
        <button type="submit">Войти</button>
      </form>
      {f'<div class="msg">{message}</div>' if message else ''}
    </section>
  </main>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return page()


@app.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    if username == DEMO_USER and verify_password(password, DEMO_PASSWORD_HASH):
        return page("Успешный вход. Пароль был проверен по хэшу, открытый пароль не хранится.")
    return page("Неверный логин или пароль.")


@app.get("/health")
async def health():
    return {"status": "ok"}
