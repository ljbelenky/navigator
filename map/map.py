import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Node():
    def __init__(self, id):
        self.id = id
        self.x = np.random.random()
        self.y = np.random.random()
        # self.status = 'unvisited'
        # self.connections = {}
    def __repr__(self):
        return "Node {}".format(self.id)
        # " ".join(['Node:', str(self.x), str(self.y)])

    # def add_connection(self, other, factor):
    #     # vector_x = self.x - other.x
    #     # vector_y = self.y - other.y
    #     # distance = (vector_x**2+vector_y**2)**.5
    #     self.connections[other] = distance * factor
    #
    # def distance(self,other):
    #     a = np.array([self.x, self.y])
    #     b = np.array([other.x, other.y])
    #     return np.linalg.norm(a-b)


class Map():
    def __init__(self, n_nodes, n_connections):
        # Make nodes
        self.nodes = [Node(i) for i in range(n_nodes)]
        self.make_connections(n_connections)

    def make_connections(self, n_connections, extra_connections = 20):
        '''Connections are a dictionary with
        key = frozenset of two node.ids
        value = distance
        '''
        self.connections = {}
        for _ in range(n_connections):
            key = np.random.choice(self.nodes, size = 2, replace = False)
            key0 = key[0].id
            key1 = key[1].id
            key = frozenset([key0,key1])
            self.connections[key] = np.random.random()

        for key0 in [self.nodes[0].id, self.nodes[-1].id]:
            for _ in range(extra_connections):
                key1 = np.random.choice(self.nodes, size = 1)[0].id
                key = frozenset([key0,key1])
                self.connections[key] = np.random.random()


    # def _remove_unconnected_nodes(self):
    #     # remove any unconnected nodes
    #     connected_nodes = set()
    #     for n1, n2 in self.connections:
    #         connected_nodes |= set([n1, n2])
    #
    #     self.nodes = [node for node in self.nodes if node in connected_nodes]
    #
    # def pick_start_and_stop(self):
    #     # pick start and stop node
    #     self.start = self.nodes[0]
    #     self.start.status = 'start'
    #     self.stop = self.nodes[-1]
    #     self.stop.status = 'stop'

    def __repr__(self):
        return "map with {} nodes and {} connections".format(len(self.nodes), len(self.connections))

    def plot(self):
        x = []
        y = []
        start_stop_x =[]
        start_stop_y = []
        for node in self.nodes:
            if node == self.start or node == self.stop:
                start_stop_x.append(node.x)
                start_stop_y.append(node.y)
            else:
                x.append(node.x)
                y.append(node.y)
        plt.scatter(x,y, marker = 'o', c = 'gray', alpha = .3)
        plt.scatter(start_stop_x, start_stop_y, marker = 'o', c = 'red')
        for n1, n2 in self.connections:
            plt.plot([n1.x, n2.x],[n1.y, n2.y], c= 'gray', alpha = .2)
        plt.show()

    def histogram(self):
        data = [len(node.connections) for node in self.nodes]
        plt.hist(data)
        plt.show()


    # def trim(self, verbose = False):
    #     '''iteratively remove isolated and dead-end nodes until stable configuration remains'''
    #     nodes = len(self.nodes)
    #     while True:
    #         self._remove_unconnected_nodes()
    #         self._remove_dead_ends()
    #         if nodes == len(self.nodes):
    #             break
    #         else:
    #             nodes = len(self.nodes)
    #             if verbose:
    #                 print(self)
    #                 self.plot()

    # def _remove_dead_ends(self):
    # # remove any nodes with 1 connection that are not start or stop
    #     from collections import Counter
    #     #make repetitive list of all nodes in connections
    #     connected_nodes = []
    #     for n1, n2 in self.connections:
    #         connected_nodes.extend([n1,n2])
    #     counter = Counter(connected_nodes)
    #     #make list of all dead ends that have 1 connection and are not start or stop
    #     dead_ends = []
    #     for node, count in counter.items():
    #         if node.status not in ['start','stop'] and count == 1:
    #             dead_ends.append(node)
    #     self.nodes = list(set(self.nodes) - set(dead_ends))
    #     # delete all connections that don't have both ends in nodes
    #     culled_connections = {}
    #     for (n1, n2), values in self.connections.items():
    #         if n1 in self.nodes and n2 in self.nodes:
    #             culled_connections[(n1,n2)]=values
    #     self.connections = culled_connections




    #     '''for each node, find vector to all connected points, apply connected force
    #     find vector to all unconnected points, apply unconnected force'''
    '''Connected Force:
    x<2d: force = 1-x/d
    x>2d: force = -1
    Unconnected Force:
    x<1: force = 1-x
    x>1 force = 0
    '''
    #
    #     for node in self.nodes:
    #         for connection in node.connections:
    #
    #         # connected_nodes = pd.DataFrame()
    #
    #         # unconnected_nodes = pd.DataFrame()
    #         node.x += delta_connected_x + delta_unconnected_x
    #         node.y += delta_connected_y + delta_unconnected_y
