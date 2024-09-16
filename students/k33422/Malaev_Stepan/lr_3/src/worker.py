from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from . import config

result_backend = RedisAsyncResultBackend(config.redis.url)  # type: ignore[var-annotated]
broker = ListQueueBroker(config.redis.url, result_backend=result_backend)
