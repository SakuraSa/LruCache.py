#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Author:cleverdeng
    E-mail:clverdeng@gmail.com
"""

__version__ = '0.1'
__all__ = ['LruCache']


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


    def fn_cache(self, fn):
        def warp(*args, **kwargs):
            key = "%s%s" % (fn.func_name, repr((args, kwargs)))
            result = self[key]
            if not result is NONE:
                return result
            else:
                result = fn(*args, **kwargs)
                self[key] = result
                return result
        return warp


    def __getitem__(self, key):
        return self.get(key)


    def __setitem__(self, key, value):
        self.put(key, value)


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

class CachedFunc(LruCache):
    def __init__(self, func, im_self, im_cls , item_max=100):
        LruCache.__init__(self, item_max=item_max)
        self.func = func
        self.im_self = im_self
        self.imcls = im_cls

    def __call__(self, *args, **kwargs):
        key = "%s%s" % (self.func.__name__, repr((args, kwargs)))
        result = self[key]
        if not result is NONE:
            return result
        else:
            self[key] = result = self.func(self.im_self, *args, **kwargs)
            return result

def Cache(item_max=100):
    class wrapper(object):
        def __init__(self, func):
            object.__init__(self)
            self.func = func

        def __get__(self, obj, cls):
            if obj is None:
                return self.func
            value = obj.__dict__[self.func.__name__] = CachedFunc(self.func, obj, cls, item_max)
            return value
    return wrapper