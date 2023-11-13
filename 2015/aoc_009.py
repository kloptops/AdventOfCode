def next_best(location_a, locations, plan):
    shortest = None
    longest = None
    if len(locations) == 1:
        temp = plan[location_a][locations[0]]
        return temp, temp

    for location in locations:
        next_locations = locations[::]
        next_locations.remove(location)
        distance = plan[location_a][location]
        distance_s, distance_l = next_best(location, next_locations, plan)
        
        if shortest is None or shortest > (distance + distance_s):
            shortest = distance + distance_s

        if longest is None or longest < (distance + distance_l):
            longest = distance + distance_l

    return shortest, longest

def simulate(data):
    plan = {}
    locations = []

    for line in data:
        location_a, _, location_b, _, dist = line.split(' ')
        
        plan.setdefault(location_a, {})[location_b] = int(dist)
        plan.setdefault(location_b, {})[location_a] = int(dist)
        if location_a not in locations:
            locations.append(location_a)
        if location_b not in locations:
            locations.append(location_b)

    shortest = None
    longest = None
    for location in locations:
        new_locations = locations[::]
        new_locations.remove(location)
        distance_s, distance_l = next_best(location, new_locations, plan)

        if shortest is None or shortest > distance_s:
            shortest = distance_s

        if longest is None or longest < distance_l:
            longest = distance_l

    return shortest, longest


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_009.txt')
    results = simulate(data)
    print(results[0], 207)
    print(results[1], 804)

if __name__ == '__main__':
    main()
