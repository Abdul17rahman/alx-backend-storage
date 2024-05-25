#!/usr/bin/env python3

"""
Cache class for redis database
"""

import redis
import uuid as v4

class Cache:
	""" Cache class created"""
	def __init__(self):
		self._redis = redis.Redis()
		self._redis.flushdb()

	def store(self, data):
		"""
		Stores the passed in data using uuid as keys
		"""
		key = str(v4.uuid4())
		self._redis.set(key, data)
		return key
