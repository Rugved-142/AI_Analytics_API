from app.core.security import create_access_token, create_refresh_token, decode_refresh_token, hash_password, verify_password


def test_password_hashing_round_trip() -> None:
    hashed = hash_password("password-123")
    assert verify_password("password-123", hashed)


def test_refresh_token_decode_round_trip() -> None:
    token = create_refresh_token("42")
    assert decode_refresh_token(token) == "42"


def test_access_token_creation() -> None:
    token = create_access_token("99")
    assert isinstance(token, str)
    assert len(token) > 10
