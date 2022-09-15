import redis

def redis_conn():
    return redis.StrictRedis(
        host='localhost',
        port=6379,
        encoding='utf8',
        db=0, 
        decode_responses=True
    )