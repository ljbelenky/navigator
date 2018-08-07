import pickle
import numpy as np

with open('m.pkl', 'rb') as f:
    map = pickle.load(f)


class Car():
    def __init__(self, map, origin = 0, destination = 499):
        self.origin = origin
        self.destination = destination
        self.path = [origin]
        self.milage = 0
        self.map = map

    def location(self):
        return self.path[-1]

    def __bool__(self):
        return self.location() == self.destination

    def __len__(self):
        return len(self.path)-1

    def __str__(self):
        return 'This car has driven {} miles over {} roads and {} at its destination.'.format(round(self.milage,2), len(self), {True:'is',False:'is not'}[self.__bool__()])

    def drive_random_path(self):
        paths = []
        for path, milage in self.map.items():
            if self.location() in path:
                paths.append([path, milage])
        paths = np.array(paths)
        rows = paths.shape[0]
        selection = paths[np.random.randint(rows), :]
        destination,  = (selection[0] - {self.location()})
        distance = selection[1]
        self.path.append(destination)
        self.milage += distance

if __name__ == '__main__':
    c = Car(map)
    while not c:
        c.drive_random_path()
        print(c)
