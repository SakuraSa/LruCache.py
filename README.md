LruCache.py
======

Implements LRU(Last-recently-used) cache algorithm, Support the thread safe, With Python


Example:

    from lru import CachedFunction

    @CachedFunction(100)
    def test_fn(x,y):
        return x,y
