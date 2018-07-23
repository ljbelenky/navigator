from map import map


m = map.Map(50, 20)
for node in m.nodes:
    print(node.connections)
print(m)
m.plot()
m.histogram()
