import time


class TTLCache:
    """Small in-process cache with expiry. Used when Redis is not configured."""

    def __init__(self):
        self._data: dict[str, tuple[float, str]] = {}

    def setex(self, key: str, ttl: int, value: str) -> None:
        self._data[key] = (time.monotonic() + ttl, value)

    def get(self, key: str):
        item = self._data.get(key)
        if not item:
            return None
        if item[0] < time.monotonic():
            self._data.pop(key, None)
            return None
        return item[1]

    def delete(self, key: str) -> None:
        self._data.pop(key, None)
