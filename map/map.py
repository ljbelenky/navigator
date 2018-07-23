import numpy as np
import matplotlib.pyplot as plt

class Node():
    def __init__(self):
        self.x = np.random.randint(1000)
        self.y = np.random.randint(1000)
        self.connections = {}
    def __repr__(self):
        return str(self.x) + " " + str(self.y)
    def add_connection(self, other, factor):
        vector_x = self.x - other.x
        vector_y = self.y - other.y
        distance = (vector_x**2+vector_y**2)**.5
        self.connections[other] = distance * factor
    def status(self, status):
        '''start, stop, unvisited, visited, on-route'''
        self.status = status

class Map():
    def __init__(self, nodes, connections):
        # Make nodes
        self.nodes = [Node() for _ in range(nodes)]
        self.make_connections(connections)

    def make_connections(self,connections):
        for _ in range(connections):
            first = np.random.choice(self.nodes)
            second = np.random.choice(self.nodes)
            if first != second:
                distance_factor = np.random.randint(100)
                first.add_connection(second, distance_factor)
                second.add_connection(first, distance_factor)
        # delete any nodes with 0 connections
        self.nodes = [node for node in self.nodes if len(node.connections)>0]

        # pick start and stop node
        self.start = self.nodes[0]
        self.stop = self.nodes[-1]

    def __repr__(self):
        total_connections = 0
        for node in self.nodes:
            total_connections += len(node.connections)
        total_connections /= 2
        return "map with {} nodes and {} connections".format(len(self.nodes), total_connections)

    def plot(self):
        for node in self.nodes:
            if node == self.start or node == self.stop:
                c = 'red'
            else:
                c = 'gray'
            plt.scatter(node.x, node.y, marker = 'o', c=c)
            for connection in node.connections:
                xx = [node.x, connection.x]
                yy = [node.y, connection.y]
                plt.plot(xx,yy, c= 'gray', alpha = .2)
        plt.show()

    def histogram(self):
        data = [len(node.connections) for node in self.nodes]
        plt.hist(data)
        plt.show()
