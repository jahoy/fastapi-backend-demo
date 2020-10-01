import aioredis
from utils.config import TESTING, TEST_REDIS_URL


redis = None


async def check_test_redis():
    global redis
    if TESTING:
        redis = await aioredis.create_redis_pool(TEST_REDIS_URL)
