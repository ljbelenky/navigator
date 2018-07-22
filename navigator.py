import numpy as np
import matplotlib.pyplot as plt

class node():
    def __init__(self):
        self.x = np.random.randint(1000)
        self.y = np.random.randint(1000)
        self.connections = {}
    def __repr__(self):
        return str(self.x) + " " + str(self.y)
    def add_connection(self, other):
        vector_x = self.x - other.x
        vector_y = self.y - other.y
        distance = (vector_x**2+vector_y**2)**.5
        self.connections[other] = distance * np.random.randint(100)

class map():
    def __init__(self, nodes, edges):
        self.nodes = [node() for _ in range(nodes)]
        for _ in range(edges):
            first = np.random.choice(self.nodes)
            second = np.random.choice(self.nodes)
            if first != second:
                first.add_connection(second)
                second.add_connection(first)
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

class car():
    def __init__(self, current_location, parent = None):
        if not parent:
            self.history = {}
            self.time = 0
        else:
            self.history = parent.history
            self.time = parent.time

        self.current_location = current_location
        self.arrived = False #changes to True when car arrives at destination
        self.children = [] #list of child cars
        self.parent = parent

    def move(self, connection):
        #move along a connection to the next node that is not in this car's history
        # record the node and arrival time in the history
        self.time += connection.distance
        self.history[node] = self.time

    def annihilate(self):
        # delete this car and all of its children
        pass


class fleet():
    def __init__(self, map):
        #make one car at start
        self.cars = [car(map.start)]

    def move_cars(self, map):
        #for each car on a node, spawn enough cars to travel to all unvisited nodes
        #move all cars to next node
        #delete any cars that are not first to arrive at a node
        pass

    def __str__(self):
        return 'This fleet contains {} cars'.format(len(self.cars))

if __name__ == '__main__':
    m = map(1000,500)
    for node in m.nodes:
        print(node.connections)
    print(m)
    m.plot()
    m.histogram()
