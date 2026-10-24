import pytest


@pytest.fixture(autouse=True)
def no_real_kakao(monkeypatch):
    # The daily run environment holds real Kakao credentials; tests must never message the phone.
    for name in ["KAKAO_REST_API_KEY", "KAKAO_REFRESH_TOKEN", "KAKAO_CLIENT_SECRET"]:
        monkeypatch.delenv(name, raising=False)
