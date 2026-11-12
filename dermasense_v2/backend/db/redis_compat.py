"""Compatibility shim: Redis access lives in cache.redis_client."""
from cache.redis_client import get_cache  # noqa: F401
