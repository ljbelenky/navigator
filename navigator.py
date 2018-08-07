from map import map


m = map.Map(500, 1500)
print(m)

for j in [0,499]:
    for i, k in m.connections.items():
        if j in i:
            print(i,k)
