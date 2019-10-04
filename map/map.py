import numpy as np
import pandas as pd 
from copy import deepcopy, copy 
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
        return self.earliest_arrival is not np.inf

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

    def other_end(self, node):
        if (node.i, node.j) == (self.nodes[0].i, self.nodes[0].j):
            return self.nodes[1], (self.nodes[1].i, self.nodes[1].j)
        else: return self.nodes[0], (self.nodes[0].i, self.nodes[0].j)


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

        for edge in self.edges:
            x = [edge.nodes[0].x, edge.nodes[1].x]
            y = [edge.nodes[0].y, edge.nodes[1].y]
            plt.plot(x,y, color = 'gray')

        x = [node.x for node in self.nodes]
        y = [node.y for node in self.nodes]
        colors = [{True:'green',False:'red'}[node.visited] for node in self.nodes]
        plt.scatter(x,y, c= colors)


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
    def __init__(self, initial_position = None):
        if initial_position:
            self.history = OrderedDict({initial_position:0})

    @property
    def odometer(self):
        return max(self.history.values())

    def drive(self, edge):
        new_car = Car()
        new_car.history = OrderedDict({node:odo for node, odo in self.history.items()})
        
        destination, _ = edge.other_end(self.current_position)
        
        new_car.history[destination] = new_car.odometer + edge.length
        destination.earliest_arrival = min(destination.earliest_arrival, new_car.odometer)
        return new_car

    @property
    def is_first_at_every_node(self):
        for node, odometer in self.history.items():
            if odometer > node.earliest_arrival:
                return False
        return True

    @property
    def index_history(self):
        return [(node.x, node.y) for node in self.history.keys()]

    @property
    def current_position(self):
        return list(self.history.keys())[-1]


if __name__ == '__main__':
    m = Map(100,100,70,70)
    # Check that we have a valid map

    if m.start.edges == []:
        print('No roads lead away from start')
    elif m.finish.edges == []:
        print('No roads lead to finish')
    elif m.start == m.finish:
        print('Start and Finish are the same')

    else:
        print("Let's get started...")



        finished_cars = []
        # nodes_visited = {m.start}
        
        #start by making one car at the starting nodezz
        active_cars = [Car(m.start)]

        iteration = 0

        while len(active_cars) > 0:
            print(iteration)
            iteration += 1

            new_cars = []
            for car in [car for car in active_cars if car.is_first_at_every_node and (car.odometer < m.finish.earliest_arrival)]:
                for edge in [edge for edge in car.current_position.edges if edge.other_end(car.current_position)[1] not in car.index_history]:
                    new_car = car.drive(edge)

                    if (new_car.current_position.i, new_car.current_position.j) == (m.finish.i, m.finish.j):
                        print('A car has finished!')
                        finished_cars.append(new_car)
                    elif new_car.is_first_at_every_node and (new_car.odometer < m.finish.earliest_arrival):
                            new_cars.append(new_car)
                    else:
                        del new_car

            active_cars = deepcopy(new_cars)
            print(f'number of active cars: {len(active_cars)}')

        
        best_odo = min([car.odometer for car in finished_cars])
        best_car = [car for car in finished_cars if car.odometer == best_odo][0]
        best_path = list(best_car.history.keys())

        m.plot()
        for n in best_path:
            plt.scatter(n.x, n.y, color = 'blue', s = 100)








