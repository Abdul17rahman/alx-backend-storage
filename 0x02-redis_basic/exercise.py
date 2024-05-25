#!/usr/bin/env python3

"""
Cache class for redis database
"""

import redis
import uuid as v4
from typing import Union, Callable

class Cache:
	""" Cache class created"""
	def __init__(self):
		self._redis = redis.Redis()
		self._redis.flushdb()

	def store(self, data: Union[str, bytes, int, float]) -> str:
		"""
		Stores the passed in data using uuid as keys
		"""
		key: str = str(v4.uuid4())
		self._redis.set(key, data)
		return key

	def get(self, key: str,  fn: Callable[[bytes], None]) -> Union[str, bytes, int, float]:
		""" retrieves a val from db"""
		val = self._redis.get(key)

		if fn is None:
			return val
		return fn(val)
	
	def get_str(self, key:str) -> str:
		""" Parametirize Cache.get for a string val"""
		return self.get(key, lambda X: X.decode('utf-8'))

	def get_int(self, key:int) -> int:
		""" Paraterize Cache.get for int val"""
		return self.get(key, int)