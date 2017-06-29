DiskCache 

1. What to use to serialize data and write to the journal log.

	Option 1: 
		http://docs.python.org/library/marshal.html
		
		This is very good in terms of speed:
		Tests for speed with pickle and marshal shows marshal is a clear win. (See comment: http://stackoverflow.com/questions/9662757/python-performance-comparison-of-using-pickle-or-marshal-and-using-re)
		
		However, the above docs say that we should not unmarshal untrusted code since it can contain some python code as this module is used for handling .pyc files.
		
	Option 2:
		http://jmoiron.net/blog/python-serialization/
		
		This blog entry indicates that msgpack is something worth considering, as well as cJson and cPickle.
		My tests indicate cPickle is 10x faster than pure pickle.
		
		timeit.timeit("cPickle.dumps([1,2,3])", "import cPickle", number=1000)
		timeit.timeit("pickle.dumps([1,2,3])", "import pickle", number=1000)
		timeit.timeit("msgpack.dumps([1,2,3])", "import msgpack", number=1000)
		
		Data from some test runs...
		
		cPickle					pickle				msgPack
		0.0015628337860107422	                0.01938796043395996		0.001889944076538086
		0.0023589134216308594	                0.022350788116455078	        0.0014629364013671875
		
		Seems like msgPack wins for now. It has quite a good community and multi-language support. Seems promising.

2. We have a hard limit on the number of keys that a node can store. This is probably not 
	ideal. We want to have a spill over system such that we can use the disk to extend
	the cache.
	
	Cassandra uses Bloom Filters for this:
		http://en.wikipedia.org/wiki/Bloom_filter
		
		We can add this into the diskCache such that we have data files and
		indices managed by the Bloom Filter. 
