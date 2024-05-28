#!/usr/bin/env python3

"""
Cache class for redis database
"""

import redis
import uuid as v4
from typing import Union, Callable
import functools


def count_calls(method: Callable) -> Callable:
	""" Decorator to count calls to Cache methods"""
	@functools.wraps(method)
	def wrapper(self, *args, **kwargs):
		key = method.__qualname__
		self._redis.incr(key)
		return method(self, *args, **kwargs)
	return wrapper


def call_history(method: Callable) -> Callable:
	"""Stores input and output history"""
	@functools.wraps(method)
	def wrapper(self, *args, **kwargs):
		key_in = f"{method.__qualname__}:inputs"
		key_out = f"{method.__qualname__}:outputs"
		self._redis.rpush(key_in, str(args))
		data = method(self, *args, **kwargs)
		self._redis.rpush(key_out, str(data))
		return data
	return wrapper


def replay(method: Callable) -> None:
	""" displays history of calls """
	name = method.__qualname__
	cache = redis.Redis()
	calls = cache.get(name).decode("utf-8")
	print("{} was called {} times:".format(name, calls))
	inputs = cache.lrange(name + ":inputs", 0, -1)
	outputs = cache.lrange(name + ":outputs", 0, -1)
	for i, o in zip(inputs, outputs):
		print("{}(*{}) -> {}".format(name, i.decode("utf-8"),
                                     o.decode("utf-8")))


class Cache:
	""" Cache class created"""
	def __init__(self):
		self._redis = redis.Redis()
		self._redis.flushdb()

	@count_calls
	@call_history
	def store(self, data: Union[str, bytes, int, float]) -> str:
		"""
		Stores the passed in data using uuid as keys
		"""
		key: str = str(v4.uuid4())
		self._redis.set(key, data)
		return key

	def get(self, key: str,  fn: Union[Callable, None] = None) -> Union[str, bytes, int, float]:
		""" retrieves a val from db"""
		val = self._redis.get(key)

		if fn is not None:
			return fn(val)

		return val
	
	def get_str(self, key: str) -> str:
		""" Parametirize Cache.get for a string val"""
		return self.get(key, lambda x: x.decode('utf-8') if x else None)

	def get_int(self, key: str) -> int:
		""" Paraterize Cache.get for int val"""
		return self.get(key, lambda a: int(a) if a else None)