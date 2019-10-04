import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict


class Node:
    '''A Node is a point on a graph that has X,Y coordinates and is connected to zero or more edges. It also records the lowest odomter of cars that visit it.'''

    def __init__(self, x, y, street_map):
        # i and j are logical positions, x and y are physical position
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
        if node == self.nodes[0]:
            return self.nodes[1]
        return self.nodes[0]


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

    @property
    def nodes(self):
        if self._nodes is None:
            nodes = [Node(x, y, self) for x in range(self.rows)
                     for y in range(self.columns)]
            self._nodes = np.random.choice(nodes, int(
                self.percent_extant/100*len(nodes)), replace=False)
        return self._nodes

    @property
    def edges(self):
        '''if a node has a neighbor directly right or directly above, an edge exists'''
        if self._edges is None:
            edges = []
            for node1 in self.nodes:
                i, j = node1.i, node1.j
                for node2 in self.nodes:
                    if (node2.i == i and node2.j == j+1) or (node2.i == i+1 and node2.j == j) or (node2.i == i+1 and node2.j == j+1) or (node2.i == i-1 and node2.j == j+1):
                        edges.append(Edge(node1, node2, 2*np.random.random()))
            self._edges = np.random.choice(edges, int(
                self.percent_connected/100*len(edges)), replace=False)
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
            while True:
                self._finish = np.random.choice(self.nodes)
                if self._finish != self.start:
                    break
        return self._finish

    def plot(self, show=True):

        for edge in self.edges:
            x = [edge.nodes[0].x, edge.nodes[1].x]
            y = [edge.nodes[0].y, edge.nodes[1].y]
            plt.plot(x, y, color='gray', alpha=.5)

        x = [node.x for node in self.nodes]
        y = [node.y for node in self.nodes]
        colors = [{True: 'green', False: 'red'}[node.visited]
                  for node in self.nodes]
        plt.scatter(x, y, c=colors, s=20)

        plt.scatter(self.start.x, self.start.y,
                    s=400, marker='X', color='green')
        plt.scatter(self.finish.x, self.finish.y,
                    s=400, marker='X', color='red')
        if show:
            plt.show()

    def __repr__(self):
        return f'a Map with {len(self.nodes)} nodes and {len(self.edges)} edges'


class Car:
    def __init__(self, initial_position=None):
        if initial_position:
            self.history = OrderedDict({initial_position: 0})

    def has_visited(self, node):
        # return node in self.node_history
        return node in self.history.keys()

    @property
    def unvisited_edges(self):
        return [edge for edge in self.current_position.edges if not self.has_visited(edge.other_end(self.current_position))]

    @property
    def odometer(self):
        # return self.odometer_history[-1]
        return list(self.history.values())[-1]

    def drive(self, edge):
        new_car = Car()
        destination = edge.other_end(self.current_position)
        new_car.history = OrderedDict(
            {node: odo for node, odo in self.history.items()})
        new_car.history[destination] = new_car.odometer + edge.length
        destination.earliest_arrival = min(
            destination.earliest_arrival, new_car.odometer)
        return new_car

    @property
    def is_first_at_every_node(self):
        return all([odometer == node.earliest_arrival for node, odometer in self.history.items()])

    @property
    def current_position(self):
        # return self.node_history[-1]
        return list(self.history.keys())[-1]

    def plot(self, color):
        x = [node.x for node in self.history.keys()]
        y = [node.y for node in self.history.keys()]

        plt.plot(x, y, color=color, lw=5)

    def __repr__(self):
        return f'A Car located at {self.current_position}'


if __name__ == '__main__':
    m = Map(100, 100, 60, 70)

    print("Let's get started...")

    finished_cars = []
    active_cars = [Car(m.start)]
    iteration = 1

    while len(active_cars) > 0:
        print('Iteration: ', iteration)
        iteration += 1
        new_cars = []
        for car in active_cars:
            for edge in car.unvisited_edges:
                new_car = car.drive(edge)
                if new_car.current_position == m.finish:
                    print('A car has finished!')
                    finished_cars.append(new_car)
                else:
                    new_cars.append(new_car)

        active_cars = [car for car in new_cars if car.is_first_at_every_node and (
            car.odometer < m.finish.earliest_arrival)]
        print(f'number of active cars: {len(active_cars)}')

    m.plot()

    if finished_cars == []:
        print('There is no path from start to finish')
    else:
        [car.plot('orange') for car in finished_cars if car.odometer !=
         m.finish.earliest_arrival]
        [car.plot('blue') for car in finished_cars if car.odometer ==
         m.finish.earliest_arrival]
