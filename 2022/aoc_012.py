def new_coord(coord, adj):
    return (coord[0] + adj[0], coord[1] + adj[1])

def topo_connections(topo, coord, fwd=True):
    global debug_count
    results = []
    coord_value = topo[coord]

    for adj in (
            (-1, 0),
            ( 1, 0),
            ( 0,-1),
            ( 0, 1)):

        adj_coord = new_coord(coord, adj)
        adj_value = topo.get(adj_coord, None)

        if adj_value is None:
            continue
        
        if fwd:
            if coord_value+1 < adj_value:
                continue
        else:
            if coord_value-1 > adj_value:
                continue

        results.append(adj_coord)

    return results


def topo_djisktra(topo, start, fwd=True):
    unvisited_coords = list(topo.keys())

    shortest_distance = {}
    for un_coord in unvisited_coords:
        shortest_distance[un_coord] = 1<<32

    shortest_distance[start] = 0
    path_coords = {}

    while len(unvisited_coords) > 0:
        min_coord = None
        for current_coord in unvisited_coords:
            if min_coord is None:
                min_coord = current_coord

            elif shortest_distance[min_coord] > shortest_distance[current_coord]:
                min_coord = current_coord

        for adj_coord in topo_connections(topo, min_coord, fwd):
            if 1 + shortest_distance[min_coord] < shortest_distance[adj_coord]:
                shortest_distance[adj_coord] = 1 + shortest_distance[min_coord]

                path_coords[adj_coord] = min_coord

        unvisited_coords.remove(min_coord)
    
    return shortest_distance, path_coords

def topo_find(topo, start, end):
    shortest_distance, path_coords = topo_djisktra(topo, start)
    coord = end
    route = []

    while coord != start:
        try:
            route.insert(0, coord)
            coord = path_coords[coord]
        except Exception:
            print('Path not reachable')
            return 1<<32
            break
    #route.insert(0, start)
    
    return len(route)

def load_topography(data):
    topo = {}
    start = None
    end = None

    for y, line in enumerate(data):

        for x, c in enumerate(line):
            coord = (x, y)

            if c == 'S':
                #topo['start'] = coord
                start = coord
                value = 0

            elif c == 'E':
                #topo['end'] = coord
                end = coord
                value = -1

            else:
                value = ord(c) - 97

            topo[coord] = value
    
    #print(topo)

    return topo, start, end


def simulate(data):
    # code here
    topo, start, end = load_topography(data)
    
    print(start, ' -> ', end)

    result_a = topo_find(topo, start, end)
    
    print(result_a)

    shortest_b = result_a

    shortest_distance, _ = topo_djisktra(topo, end, fwd=False)
    print(shortest_distance)
    for i, (coord, distance) in enumerate(shortest_distance.items()):
        if distance > result_a:
            continue

        if topo[coord] != 0:
            continue

        #distance = topo_find(topo, coord, end)
        #print(coord, dj_distance, distance)

        if distance < shortest_b:
            shortest_b = distance

    return result_a, shortest_b


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_012.txt')
    results = simulate(data)
    print(results[0], 420)
    print(results[1], 420)


if __name__ == '__main__':
    main()
