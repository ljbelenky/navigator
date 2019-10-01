import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Node:
    '''A Node is a point on a graph that has X,Y coordinates and is connected to zero or more edges. It also records the lowest odomter of cars that visit it.'''

    def __init__(self, x, y, street_map):
        #i and j are logical positions, x and y are physical position
        self.x = self.i = x
        self.y = self.j = y
        self.earliest_arrival = None
        self.map = street_map

    @property
    def edges(self):
        '''The collection of all edges that connect to this node'''
        return [edge for edge in self.map.edges if self in edge.nodes]

    @property
    def neighbors(self):
        '''The nodes that are connected to the edges connected to this node'''
        return set([edge.nodes for edge in self.edges]) - {self}

    def __repr__(self):
        return f'A node located at {self.x,self.y}'

class Edge:
    '''An edge is a line segment that connects two nodes and has a length'''
    def __init__(self, Node1, Node2, length):
        '''Note: Edge is bi-directional. Node1 and Node2 are interchangeable'''
        self.nodes = [Node1, Node2]
        self.length = length or np.random.random()*100

    def __repr__(self):
        return f'An edge of length {self.length} between {self.nodes}'


class Map:
    def __init__(self, rows, columns, percent_extant, percent_connected):
        '''Create a map with (rows*columns) nodes in which percent_extant 
        of the nodes and ercent_connected of the edges exist.'''
        
        self.rows = rows
        self.columns = columns
        self.percent_extant = percent_extant
        self.percent_connected = percent_connected
        self._edges = None
        self._nodes = None

    @property
    def nodes(self):
        if self._nodes is None:
            nodes = [Node(x,y, self) for x in range(self.rows) for y in range(self.columns)]
            self._nodes = np.random.choice(nodes, int(self.percent_extant/100*len(nodes)), replace = False)
        return self._nodes

    @property
    def edges(self):
        '''if a node has a neighbor directly right or directly above, an edge exists'''
        if self._edges is None:
            edges = []
            for node1 in self.nodes:
                i,j = node1.i, node1.j
                for node2 in self.nodes:
                    if (node2.i == i and node2.j == j+1) or (node2.i == i+1 and node2.j==j):
                        edges.append(Edge(node1, node2, np.random.randint(1,100)))
            self._edges = np.random.choice(edges, int(self.percent_connected/100*len(edges)), replace = False)
        return self._edges


    def show(self):
        x = [node.x for node in self.nodes]
        y = [node.y for node in self.nodes]

        plt.scatter(x,y)
        plt.show()

    def __repr__(self):
        return f'a Map with {len(self.nodes)} nodes and {len(self.edges)} edges'


if __name__ == '__main__':
    m = Map(4,4,70,70)
    m.show()

