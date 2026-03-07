from app.core.config import settings
from app.providers.mock_provider import MockProvider


def get_market_provider():
    return MockProvider() if settings.demo_mode else MockProvider()
