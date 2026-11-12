import logging

from config.settings import settings
from cache.memory_cache import TTLCache

log = logging.getLogger("dermasense")
_cache = None


def get_cache():
    """Redis when REDIS_URL is set and reachable, otherwise an in-memory cache."""
    global _cache
    if _cache is None:
        if settings.redis_url:
            try:
                import redis

                client = redis.Redis.from_url(settings.redis_url, decode_responses=True, socket_connect_timeout=2)
                client.ping()
                _cache = client
            except Exception as exc:
                log.warning("Redis unavailable (%s); using in-memory cache", exc)
        if _cache is None:
            _cache = TTLCache()
    return _cache


def set_cache(cache) -> None:
    global _cache
    _cache = cache
