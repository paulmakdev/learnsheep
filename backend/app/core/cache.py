import json
import redis
from typing import Any, Optional, Set
from app.core.config import settings

redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True,
    # So we don't hang
    socket_connect_timeout=3,
    socket_timeout=3,
    retry_on_timeout=True,
    health_check_interval=30,
)


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

    def delete_pattern(self, pattern: str, batch_size: int = 100):
        cursor = 0
        while True:
            cursor, keys = self.client.scan(cursor, match=pattern, count=batch_size)
            if keys:
                self.client.delete(*keys)
            if cursor == 0:
                break

    def set_preserve_ttl(self, key: str, value: Any):
        ttl = self.client.ttl(key)

        # if no TTL, we don't want to set anything
        if ttl > 0:
            # Key has TTL → preserve it
            self.client.setex(key, ttl, json.dumps(value, default=str))

    # -- Set Operations --

    def sadd(self, key: str, *values: Any, ttl: int | None = None) -> int:
        exists = self.client.exists(key)

        self.client.sadd(key, *values)

        if ttl is not None and exists == 0:
            self.client.expire(key, ttl)

    def srem(self, key: str, *values: Any) -> int:
        self.client.srem(key, *values)

    def smembers(self, key: str) -> Optional[Set[Any]]:
        value = self.client.smembers(key)
        return value if value else None
