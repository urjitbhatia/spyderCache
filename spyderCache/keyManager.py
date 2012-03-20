'''
Created on Mar 11, 2012

@author: urjit

Code adapted from :
http://amix.dk/blog/post/19367

'''

import md5
from utils import LogHelper

class KeyManager(object):
    '''
    This class manages the operations related to key distribution.
    It uses a simple consistent hashing approach for distributing data evenly amongst the available nodes.
    '''

    #default to using 3 replicas of each node - to improve distribution
    replicas = 3
    ring = dict()
    _sorted_keys = []

    logger = LogHelper.getLogger()

    def setupHashRing(self, connections, replicas=3):
        """Manages a hash ring.

        `nodes` is a list of objects that have a proper __str__ representation.
        `replicas` indicates how many virtual copies should be used per node,
        replicas are required to improve the distribution.
        """
        self.replicas = replicas

        '''
        Add your peers to the ring.
        '''
        if len(connections) > 0:
            for node in connections:
                self.add_node(node)

        self.logger.info(self._sorted_keys)

    def add_node(self, node):
        """Adds a `node` to the hash ring (including a number of replicas).
        """
        for i in xrange(0, self.replicas):
            key = self.gen_key('%s:%s' % (node, i)) #append the virtual copy number to mix the key
            self.ring[key] = node                   #append the virtual copy to the key ring
            self._sorted_keys.append(key)           #maintain a sorted list of keys
            self.logger.info("node: " + str(node) + " key: " + str(key))

        self._sorted_keys.sort()
        self.logger.info("node added " + str(node))

    def remove_node(self, node):
        """Removes `node` from the hash ring and its replicas.
        """
        for i in xrange(0, self.replicas):
            key = self.gen_key('%s:%s' % (node, i)) #remove the virtual copy for this node, same 'key' is generated as when adding the nodes
            try:
                del self.ring[key]                      #delete the node at the 'key' index                  
                self._sorted_keys.remove(key)           #delete the key from the list of sorted keys
            except:
                pass

    def get_node(self, string_key):
        """Given a string key a corresponding node in the hash ring is returned.

        If the hash ring is empty, `None` is returned.
        """
        return self.get_node_pos(string_key)[0]     #gets a tuple [node, node-pos] and returns the node from this tuple.     

    def get_node_pos(self, string_key):
        """Given a string key a corresponding node in the hash ring is returned
        along with it's position in the ring.

        If the hash ring is empty, (`None`, `None`) is returned.
        """
        if not self.ring:
            return None, None

        key = self.gen_key(string_key)              #generate the key

        nodes = self._sorted_keys                   #available nodes
        for i in xrange(0, len(nodes)):
            node = nodes[i]
            if key <= node:                         #first 'node key' that is gt or eq to the 'data key'
                return self.ring[node], i

        return self.ring[nodes[0]], 0

    def get_nodes(self, string_key):
        """Given a string key it returns the nodes as a generator that can hold the key.

        The generator is never ending and iterates through the ring
        starting at the correct position.
        """
        if not self.ring:
            yield None, None

        node, pos = self.get_node_pos(string_key)   #the starting position for this key
        for key in self._sorted_keys[pos:]:         #keep rotating forward
            yield self.ring[key]

        while True:
            for key in self._sorted_keys:
                yield self.ring[key]

    def gen_key(self, key):
        """Given a string key it returns a long value,
        this long value represents a place on the hash ring.

        md5 is currently used because it mixes well.
        """
        m = md5.new()
        m.update(key)
        return long(m.hexdigest(), 16)
