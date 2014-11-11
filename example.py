#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Author:cleverdeng
    E-mail:clverdeng@gmail.com
"""

from lru import CachedFunction


@CachedFunction(100)
def test_fn(x,y):
    return x,y

print test_fn(1,2)
print test_fn(1,2)
print test_fn(3,4)
print 'get key:test value:%s' % test_fn.get("test1") 
test_fn.put('test1', 1)
test_fn.put("test2", 2)
test_fn.put("test3", 3)
test_fn.put("test4", 4)
test_fn.put("test5", 5)
print 'get key:test value:%s' % test_fn.get("test1") 
test_fn.put("test6", 6)
test_fn.put("test7", 7) 
print 'get key:test6 value:%s' % test_fn.get("test6") 
print 'get key:test3 value:%s' % test_fn.get("test3") 
test_fn.status()   
