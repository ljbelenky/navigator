from map import map


m = map.Map(50, 100)
m.pick_start_and_stop()
# for node in m.nodes:
#     print(node.connections)
print(m)
m.plot()

nodes, connections = len(m.nodes), len(m.connections)
while True:
    m.remove_unconnected_nodes()
    m.remove_dead_ends()
    print(m)
    m.plot()
    if nodes == len(m.nodes) and connections == len(m.connections):
        break
    else:
        nodes, connections = len(m.nodes), len(m.connections)
