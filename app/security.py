import base64
import hashlib
import hmac
import os


DEFAULT_ITERATIONS = 200_000


def hash_password(password: str, salt: bytes | None = None, iterations: int = DEFAULT_ITERATIONS) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return "pbkdf2_sha256${}${}${}".format(
        iterations,
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(digest).decode("ascii"),
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt, expected = password_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hash_password(
            password,
            base64.b64decode(salt.encode("ascii")),
            int(iterations),
        ).split("$", 3)[3]
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def security_headers() -> dict[str, str]:
    return {
        "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'; form-action 'self'",
        "Referrer-Policy": "no-referrer",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
    }
