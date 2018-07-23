import numpy as np
import matplotlib.pyplot as plt

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
