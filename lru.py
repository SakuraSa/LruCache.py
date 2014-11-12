#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Author:cleverdeng
    E-mail:clverdeng@gmail.com
"""

__version__ = '0.2'
__all__ = [
    'LruCache', 
    'Cached',
    'DecorationMode', 
    'CachedFunction', 
    'CachedStaticFunction', 
    'CachedClassFunction', 
    'CachedInstanceFunction'
]


import threading

NONE = object()

class LruCache(object):
    def __init__(self, item_max=100):
        if item_max <=0:
             raise ValueError('item_max must be > 0')
        self.lock = threading.Lock()
        self.item_max = item_max
        self.clear()

    def clear(self):
        self.hits = 0
        self.miss = 0
        self.cache = {}
        self.keys = []
        self.used = 0
        self.remove = 0

    def __getitem__(self, key):
        return self.get(key)


    def __setitem__(self, key, value):
        self.put(key, value)

    def __contains__(self, key):
        return key in self.cache

    def get(self, key, default=NONE):
        with self.lock:
            if key in self.cache:
                self.hits += 1
                self.__lru_key(old_key=key, new_key=key)
                return self.cache[key]
            else:
                self.miss += 1
                return default


    def put(self, key, val):
        with self.lock:
            if self.used == self.item_max:
                r_key = self.keys[-1]
                self.cache.pop(r_key)
                self.cache[key] = val
                self.remove += 1
                self.__lru_key(old_key=r_key, new_key=key)
            else:
                self.used += 1
                self.cache[key] = val
                self.__lru_key(old_key=key, new_key=key)


    def __lru_key(self, old_key=None, new_key=None):
        if old_key in self.keys:
            self.keys.remove(old_key)
        self.keys.insert(0, new_key)


    def status(self):
        used_status = """
Single process cache used status:
    max:%s
    used:%s
    key:%s
    miss:%s
    hits:%s
    remove:%s
""" % (self.item_max, self.used, ','.join(self.keys), self.miss, self.hits, self.remove)
        print used_status


class DecorationMode(object):
    Function = 0
    StaticFunction = 1
    ClassFunction = 2
    InstanceFunction = 3

class Cached(LruCache):
    def __init__(self, func, mode=0, item_max=100):
        LruCache.__init__(self, item_max)
        self.mode = mode
        self.func = func
        self.obj = None
        self.cls = None

    def cached_func(self, *args, **kwagrs):
        if self.mode == DecorationMode.InstanceFunction:
            args = (self.obj, ) + args
        elif self.mode == DecorationMode.ClassFunction:
            args = (self.cls, ) + args
        key = repr(args) + repr(kwagrs)
        if key in self:
            return self[key]
        else:
            value = self[key] = self.func(*args, **kwagrs)
            return value

    def __call__(self, *args, **kwargs):
        return self.cached_func(*args, **kwargs)

    def __get__(self, obj, cls):
        if obj is None:
            if self.mode == DecorationMode.ClassFunction:
                self.cls = cls
        else:
            if self.mode == DecorationMode.InstanceFunction:
                self.obj = obj
        return self


def CachedFunction(item_max=100):
    def Decoration(func):
        return Cached(func, DecorationMode.Function, item_max)
    return Decoration


def CachedStaticFunction(item_max=100):
    def Decoration(func):
        return Cached(func, DecorationMode.StaticFunction, item_max)
    return Decoration


def CachedClassFunction(item_max=100):
    def Decoration(func):
        return Cached(func, DecorationMode.ClassFunction, item_max)
    return Decoration


def CachedInstanceFunction(item_max=100):
    def Decoration(func):
        return Cached(func, DecorationMode.InstanceFunction, item_max)
    return Decoration
    