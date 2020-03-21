def redisConnection(hostname):
    """
    redisConnection: Make a redis connection object

    Args:
        hostname (str): redis hostname IP or URL

    Returns:
        redis.client.Redis : Connection instance
    """
    import redis
    import sys
    rcon = redis.Redis(host=hostname, port=6379)
    try:
        rcon.ping()
    except:
        print("connectionError")
        sys.exit(1)
    return rcon
