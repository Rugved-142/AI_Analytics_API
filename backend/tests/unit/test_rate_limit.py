import pytest

from app.core.errors import ProblemException
from app.services import rate_limit


def test_rate_limit_blocks_when_over_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rate_limit.settings, "rate_limit_per_minute", 1)
    rate_limit.enforce_rate_limit("test-key")
    with pytest.raises(ProblemException):
        rate_limit.enforce_rate_limit("test-key")
