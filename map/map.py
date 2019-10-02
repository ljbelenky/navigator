import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from collections import OrderedDict

class Node:
    '''A Node is a point on a graph that has X,Y coordinates and is connected to zero or more edges. It also records the lowest odomter of cars that visit it.'''

    def __init__(self, x, y, street_map):
        #i and j are logical positions, x and y are physical position
        self.x = self.i = x
        self.y = self.j = y
        self.earliest_arrival = np.inf
        self.map = street_map

    @property
    def visited(self):
        return self.earliest_arrival is not None

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
        self._start = None
        self._finish = None

        # for _ in range(1):
        #     self._reposition()

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
                    if (node2.i == i and node2.j == j+1) or (node2.i == i+1 and node2.j==j) or (node2.i == i+1 and node2.j == j+1) or (node2.i == i-1 and node2.j == j+1):
                        edges.append(Edge(node1, node2, 2*np.random.random()))
            self._edges = np.random.choice(edges, int(self.percent_connected/100*len(edges)), replace = False)
        return self._edges

    @property
    def start(self):
        if self._start is None:
            self._start = np.random.choice(self.nodes)
            self._start.earliest_arrival = 0
        return self._start

    @property
    def finish(self):
        if self._finish is None:
            self._finish = np.random.choice(self.nodes)
        return self._finish


    def plot(self, show = True):
        x = [node.x for node in self.nodes]
        y = [node.y for node in self.nodes]
        plt.scatter(x,y)

        for edge in self.edges:
            x = [edge.nodes[0].x, edge.nodes[1].x]
            y = [edge.nodes[0].y, edge.nodes[1].y]
            plt.plot(x,y, color = 'gray')

        plt.scatter(self.start.x, self.start.y, s = 400, marker = 'X', color = 'green')
        plt.scatter(self.finish.x, self.finish.y, s = 400, marker = 'X', color = 'red')
        if show:
            plt.show()

    def __repr__(self):
        return f'a Map with {len(self.nodes)} nodes and {len(self.edges)} edges'

    def _reposition(self):
        lr = .5
        for edge in self.edges:
            center_x = (edge.nodes[0].x + edge.nodes[1].x)/2
            center_y = (edge.nodes[0].y + edge.nodes[1].y)/2

            actual_length = ((edge.nodes[0].x - edge.nodes[1].x)**2 + (edge.nodes[0].y - edge.nodes[1].y)**2)**.5
            desired_length = edge.length

            adjustment = (desired_length - actual_length) * lr

            for node in edge.nodes:
                delta_x = abs(center_x - node.x) * adjustment
                delta_y = abs(center_y - node.y) * adjustment
                if node.x < center_x: 
                    node.x -= delta_x
                else:
                    node.x += delta_x

                if node.y < center_y:
                    node.y -= delta_y
                else:
                    node.y += delta_y
                    
class Car:
    def __init__(self, initial_position):
        self.odometer = 0
        self.history = OrderedDict({initial_position:0})

    def drive(self, edge):
        self.odometer += edge.length
        destination = list(set(edge.nodes)-{self.current_position})[0]
        destination.earliest_arrival = min(destination.earliest_arrival, self.odometer)
        self.history[destination] = self.odometer
        return deepcopy(self)

    @property
    def is_first_at_every_node(self):

        result = True
        for node, odometer in self.history.items():
            if odometer > node.earliest_arrival:
                result = False
                break

        return result

    def arrived(self, finish):
        return self.current_position == finish


    @property
    def current_position(self):
        return list(self.history.keys())[-1]

def best_finishing_odometer(finished_cars):
    try:
        return min([car.odometer for car in finished_cars])
    except:
        return np.inf


if __name__ == '__main__':
    # plt.xkcd()
    m = Map(6,6,100,100)
    # Check that we have a valid map

    if m.start.edges == []:
        print('No roads lead away from start')
    elif m.finish.edges == []:
        print('No roads lead to finish')
    elif m.start == m.finish:
        print('Start and Finish are the same')

    else:
        print("Let's get started...")

        m.plot()

        finished_cars = []
        
        #start by making one car at the starting node
        active_cars = [Car(m.start)]

        iteration = 0

        while len(active_cars) > 0:
            print(iteration)
            iteration += 1

            new_cars = []
            for car in active_cars:
                for edge in car.current_position.edges:
                    new_car = car.drive(edge)

                    if new_car.current_position == m.finish:
                        print('A car has finished!')
                        finished_cars.append(new_car)
                    elif new_car.is_first_at_every_node:
                        print('is first')
                        if (new_car.odometer < best_finishing_odometer(finished_cars)):
                            new_cars.append(new_car)

            active_cars = deepcopy(new_cars)
            print(f'number of active cars: {len(active_cars)}')

        print(len(finished_cars))








