'''
Created on Mar 16, 2012

@author: urjit

Using LRU Dictionary implementation class
thanks to: Dirk Esser

# -*- coding: utf-8 -*-
#
#  Deterministic Arts Utilities
#  Copyright (c) 2011 Dirk Esser
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

'''


missing = object()

class LRUDict(object):

    """Dictionary with LRU behaviour

    This class implements a dictionary, whose size is limited to a
    pre-defined capacity. Adding new elements to a full LRU dictionary
    will cause \"old\" elements to be evicted from the dictionary in
    order to make room for new elements.

    Instances of this class are not thread-safe; if an instance is
    to be shared across multiple concurrently running threads, the
    client application is responsible for providing proper synchronization.
    In particular, be aware, that even read-only operations on instances
    of this class might internally modify data structures, and thus,
    concurrent read-only access has to be synchronized as well.
    """

    __slots__ = (
        '__weakref__',
        '_LRUDict__index',
        '_LRUDict__first',
        '_LRUDict__last',
        '_LRUDict__capacity',
    )
    
    def __init__(self, capacity=1024):
        super(LRUDict, self).__init__()
        self.__index = dict()
        self.__first = None
        self.__last = None
        self.__capacity = self.__check_capacity(capacity)

    def __set_capacity(self, value):
        value = self.__check_capacity(value)
        if value > self.__capacity:
            self.__capacity = value
        else:
            if value < self.__capacity:
                self.__capacity = value
                self.__ensure_room(0)

    def capacity():
        def getter(self): 
            return self.__capacity
        def setter(self, value):
            self.__set_capacity(value)
        return property(getter, setter, doc="""Capacity

            This property holds an integer number, which defines the
            capacity of this dictionary (i.e., the maximum number of 
            elements it may hold at any time). Setting this property
            to a new value may cause elements to be evicted from the
            dictionary.""")

    capacity = capacity()

    def __check_capacity(self, value):
        if value < 1:
            raise ValueError("%r is not a valid capacity" % (value,))
        return value

    def clear(self):

        """Removes all entries
        """

        first = self.__first

        self.__index.clear()
        self.__first = self.__last = None

        # XXX: This code should be reconsidered. We clean up the
        # doubly-linked list primarily for the sake of CPython and
        # its reference-counting based memory management. However,
        # maybe we should just forget about this and rely on the 
        # GC to clean up the cycles here. There should not be any
        # __del__ methods involved here anyway (at least not in the
        # objects we are responsible for, i.e., the LRUItems)

        while first is not None:
            next = first._next
            first._key = first._value = None
            first._previous = first._next = None
            first = next

    def __len__(self):

        """Answers the current number of elements in this dictionary
        """

        return len(self.__index)
    
    def __contains__(self, key):

        """Tests, whether a key is contained

        This method returns true, if there is an entry with the
        given `key` in this dictionary. If so, the entry's priority
        will be boosted by the call, making it more unlikely, that
        the entry will be evicted when the dictionary needs to make
        room for new entries.
        """

        item = self.__index.get(key)
        if item is None:
            return False
        else:
            self.__make_first(item)
            return True

    def __iter__(self):

        """Iterator for all keys of this dictionary

        See `iterkeys`.
        """

        return self.__index.iterkeys()

    def iterkeys(self):

        """Iterator for all keys of this dictionary

        This method returns a generator, which yields all keys
        currently present in this dictionary. Note, that iterating
        over the elements of an LRU dictionary does not change
        the priorities of individual entries. Also note, that the
        order, in which entries are generated, is undefined. In
        particular, the order does usually *not* reflect the LRU 
        priority in any way.
        """

        return self.__index.iterkeys()

    def itervalues(self):

        """Iterator for all values of this dictionary

        This method returns a generator, which yields all values
        currently present in this dictionary. Note, that iterating
        over the elements of an LRU dictionary does not change
        the priorities of individual entries. Also note, that the
        order, in which entries are generated, is undefined. In
        particular, the order does usually *not* reflect the LRU 
        priority in any way.
        """

        for item in self.__index.itervalues():
            yield item._value

    def iteritems(self):

        """Iterator for all entries of this dictionary

        This method returns a generator, which yields all keys and
        values currently present in this dictionary as tuples of
        `key, value`. Note, that iterating over the elements of an 
        LRU dictionary does not change the priorities of individual 
        entries. Also note, that the order, in which entries are 
        generated, is undefined. In particular, the order does usually 
        *not* reflect the LRU priority in any way.
        """

        for key, item in self.__index.iteritems():
            yield key, item._value

    def __delitem__(self, key):

        """Removes an entry from this dictionary

        This method removes the entry identified by the given
        `key` from this dictionary. If no matching entry exists,
        this method raises a `KeyError` exception.

        This method does not affect the priorities of entries
        remaining in the dictionary.
        """

        item = self.__index.pop(key)
        self.__unlink(item)

    def pop(self, key, default=missing):

        """Removes an entry from this dictionary

        This method removes the entry identified by the given
        `key` from this dictionary, returning its associated
        value. If no matching entry exists, this method returns
        the value supplied as `default` or raises a `KeyError` 
        exception, if no default value was supplied.

        This method does not affect the priorities of entries
        remaining in the dictionary.
        """

        item = self.__index.pop(key, None)
        if item is None:
            if default is not missing:
                return default
            else:
                raise KeyError(key)
        else:
            self.__unlink(item)
            return item._value

    def get(self, key, default=None):
        
        """Obtains an entry's value

        This method returns the value associated with the given `key`
        in this dictionary. If no matching entry exists, the method
        returns the value of `default` instead.

        If a matching entry is found, this method will boost that
        entry's priority, making it more unlikely, that the entry
        will be evicted from the dictionary the next time, the dict
        needs to make room for a new entry.
        """

        item = self.__index.get(key)
        if item is None:
            return default
        else:
            self.__make_first(item)
            return item._value

    def peek(self, key, default=None):

        """Obtains an entry's value

        This method returns the value associated with the given `key`
        in this dictionary. If no matching entry exists, the method
        returns the value of `default` instead.

        This method differs from `get` in that it does not alter the
        priority of a matching entry, i.e., the likelyhood of the 
        entry being evicted the next time, the dict needs to make 
        room, is not affected by calls to this method.
        """

        item = self.__index.get(key)
        if item is None:
            return default
        else:
            return item._value

    def __getitem__(self, key):

        """Obtains an entry's value

        This method returns the value associated with the given `key`
        in this dictionary. If no matching entry exists, the method
        raises a `KeyError` instead.

        If a matching entry is found, this method will boost that
        entry's priority, making it more unlikely, that the entry
        will be evicted from the dictionary the next time, the dict
        needs to make room for a new entry.
        """

        item = self.__index.get(key)
        if item is None:
            raise KeyError(key)
        else:
            self.__make_first(item)
            return item._value

    def __setitem__(self, key, value):

        """Adds or modifies an entry

        This method sets the value associated with `key` in this
        dictionary to `value`. If there is no present entry for
        `key` in this dictionary, this method may need to evict
        entries from the dictionary in order to make room for the
        new entry.

        This method boosts the priority of the entry associated
        with `key` making it more unlikely, that the entry
        will be evicted from the dictionary the next time, the dict
        needs to make room for a new entry. 
        """

        present = self.__index.get(key)
        if present is not None:
            present._value = value
            self.__make_first(present)
        else:
            self.__ensure_room(1)
            item = LRUItem(key, value)
            item._previous = None
            item._next = self.__first
            if self.__first is None:
                self.__last = item
            else:
                self.__first._previous = item
            self.__index[key] = item
            self.__first = item

    def __ensure_room(self, size):
        
        """(internal)

        This method makes sure, that there is room for `size` 
        new elements in this dictionary, potentially evicting
        old elements.
        """
        
        index = self.__index
        capacity = self.__capacity
        if size > capacity:
            raise ValueError(size)
        else:
            while len(index) + size > capacity:
                last = self.__last
                del index[last._key]
                self.__unlink(last)
            return self

    def __unlink(self, item):

        """(internal)

        Unlink `item` from the doubly-linked list of LRU items
        maintained by this dictionary. Makes sure, that the 
        dictionary's `__first` and `__last` pointers are properly
        updated, if the item happens to be the first/last in
        the list.
        """

        p, n = item._previous, item._next
        if p is None:
            self.__first = n
        else:
            p._next = n
        if n is None:
            self.__last = p
        else:
            n._previous = p
        item._previous = None
        item._next = None
        return item

    def __make_first(self, item):

        """(internal)

        Boosts `item`'s priority by making it the first item of
        the doubly linked list of all items. Since the eviction
        process removes elements from the end of the list, the
        items closer to the head are more unlikely to be removed
        if we need to make room for new elements.
        """

        p, n = item._previous, item._next
        if p is None:
            assert item is self.__first, "no previous entry in %r, but first is %r" % (item, self.__first,)
            return item
        else:
            p._next = n
            if n is None:
                self.__last = p
            else:
                n._previous = p
            item._previous = None
            item._next = self.__first
            self.__first._previous = item
            self.__first = item
            return item

        
        
class LRUItem(object):

    """Element of the LRUDict

    Instances of this class are used internally to hold the entries
    of `LRUDict` instances. The entries form a doubly-linked list,
    and are also interned in a dictionary for fast look-up.
    """

    __slots__ = (
        '_previous',
        '_next',
        '_key',
        '_value',
    )

    def __init__(self, key, value):
        self._key = key
        self._value = value
        self._previous = None
        self._next = None

    def __str__(self):
        return "<LRUItem %r: %r>" % (self._key, self._value)

    def __repr__(self):
        return "LRUItem(%r, %r)" % (self._key, self._value)
