#!/usr/bin/python3
import redis

import bConfig

class redisOp:
    def getRedis(self):
        db_config = bConfig.getconfig()
        db_config = db_config['redis']
        r = redis.Redis(host=db_config['host'], port=db_config['port'])
        return r

