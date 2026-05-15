from app.security import hash_password, security_headers, verify_password


def test_password_hash_is_not_plain_text():
    password_hash = hash_password("secret", salt=b"fixed-test-salt")

    assert "secret" not in password_hash
    assert verify_password("secret", password_hash)
    assert not verify_password("wrong", password_hash)


def test_security_headers_include_clickjacking_protection():
    headers = security_headers()

    assert headers["X-Frame-Options"] == "DENY"
    assert "frame-ancestors 'none'" in headers["Content-Security-Policy"]
    assert headers["X-Content-Type-Options"] == "nosniff"
