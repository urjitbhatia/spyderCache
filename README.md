**author**: urjit singh bhatia    
**url**:	about.me/urjitbhatia    
**email**:  urjitsb87@gmail.com    

####SpyderCache is a distributed cache written in python.####

#####There are 3 main parts:#####

1. **Topology Layer**    
    This layer is responsible for knowing where its peers are and talking to them over a 'peer-channel'.
    A sub-system of this layer is the KeyManager which is an implementation of consistent hashing (Thanks http://amix.dk/blog/post/19367 for the boiler-plate code).

2. **Communication Layer**    
    This layer is responsible for gathering requests from clients and using appropriate layers in the system to accomplish the requested tasks. This layer runs cocooned in a thin web-server - currently CherryPy based on some benchmarks here: http://nichol.as/benchmark-of-python-web-servers.

3. **Caching Layer**    
	This layer is responsible for storing the data in memory. 
    Support for recovery from disk is available, 
    which will allow a dead node to recover its last known state.

Installing dependencies:
	
	Python Version:
	This was built using python 2.7.2. on Ubuntu 11.10 [GCC 4.6.1]

	Use a package manager like pip and install the following packages:
	1. python-msgpack
	2. cherrypy

Features available currently:

1. Simple file based configuration of the system. Explanation of a complete config file follows.
2. If a node goes down on the fly, other nodes assume responsibility for the data. Bringing a node back to life is very easy. It starts caching its share of data as soon as it can.    

*Example:	This is the configuration file.*

	[local]
	node_id = 1				
	#this is the id of the node which this file will drive. Any string is valid    
    
	node_port = 8001			
	#the port at which this node should communicate. valid entry regex \:[0-9]{4,5}$    
    
	reconstruct = False			
	#should the node read the events journal to restore last known state? valid: True/False    
    
	cache_size = 1000			
	#Maximum number of keys this cache is allowed to hold. After this limit is hit,    
	#the cache will start evicting keys using an LRU mechanism    
    
	[network]					
	#simply the list of peers this node should connect to.    
    
	peer = 127.0.0.1:8002,		
			127.0.0.1:8003		
	#it is a comma separated list of the form <ipv4address>:<port>    
	#valid entry regex is: ^([0-9]{1,3}\.){3}[0-9]{1,3}\:[0-9]{4,5}$    

	This file will fire node 8001 and instruct it to connect to nodes 8002 and 8003 as its distribution partners.    


TODO:

[DONE] Add support for journaling to disk so that we can reinstate a node to its last known state.    
Add cache invalidation message from peer nodes.    
[DONE] Add heartbeat monitoring and thin master to maintain the system.    


#####Command scripts:#####
	
	See utils directory for some standalone command scripts.
	Example:
	
	use put.py to put a key value pair onto a node
	python put.py key value 127.0.0.1 8001
	
	This will put the key 'key' and its value 'value' on the appropriate node.
	
	Scripts:
	
	connect.py - Connect to a given node on the fly
	get.py - Get a key
	put.py - Put a key-value data item
	delete.py - Delete a key
	fake_death.py - Kill a node	
	reconstruct.py - Reconstruct a node from its data log

