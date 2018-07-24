from map import map


m = map.Map(100, 200)
m.pick_start_and_stop()
# for node in m.nodes:
#     print(node.connections)
print(m)
m.plot()

m.trim(verbose = True)
m.plot()
