import json
import redis
from typing import Any, Optional
from app.core.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)


def get_redis():
    return redis_client


class CacheService:
    def __init__(self, client: redis.Redis):
        self.client = client

    def get(self, key: str) -> Optional[Any]:
        value = self.client.get(key)
        return json.loads(value) if value else None

    def set(self, key: str, value: Any, ttl: int = 300):
        self.client.setex(key, ttl, json.dumps(value, default=str))

    def delete(self, key: str):
        self.client.delete(key)

    def delete_pattern(self, pattern: str):
        keys = self.client.keys(pattern)
        if keys:
            self.client.delete(*keys)
