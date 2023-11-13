distance_cache = {}
def distance_to(network, from_valve, to_valve, depth=0, seen=None):
    global distance_cache

    if seen is None:
        seen = [from_valve]

    connections = network[from_valve]

    if to_valve in connections:
        return depth + 1

    key = (from_valve, to_valve)
    if key in distance_cache:
        return depth + distance_cache[key]

    if seen is None:
        seen = []

    seen.append(from_valve)
    min_depth = None
    for to_connection in connections:
        if to_connection in seen:
            continue

        new_depth = distance_to(network, to_connection, to_valve, depth+1, seen[:])
        if new_depth is None:
            continue

        if min_depth is None or new_depth < min_depth:
            min_depth = new_depth
    
    if min_depth is None:
        return None

    distance_cache[key] = (min_depth - depth)

    return min_depth


def best_move_a(network, valves, location, valves_left, time_left):

    best_score = 0
    for next_valve in valves_left:
        time_to = distance_to(network, location, next_valve)
        new_time_left = time_left - time_to - 1
        if new_time_left < 0:
            continue

        new_score = new_time_left * valves[next_valve]

        new_valves_left = valves_left[:]
        new_valves_left.remove(next_valve)
        
        new_score += best_move_a(network, valves, next_valve, new_valves_left, new_time_left)

        if best_score < new_score:
            best_score = new_score

    return best_score

best_move_cache = {}
def best_move_b(network, valves, from_a, from_b, left_a, time_left_a, time_left_b, depth=0):
    best_score = 0

    key = tuple((from_a, from_b, tuple(left_a), time_left_a, time_left_b))

    if key in best_move_cache:
        return best_move_cache[key]
        pass

    if len(left_a) == 1:
        best_a = best_move_a(network, valves, from_a, left_a, time_left_a)

        best_b = best_move_a(network, valves, from_b, left_a, time_left_b)

        if best_a > best_a:
            return best_a
        else:
            return best_b

    if depth < 2:
        print(depth, from_a, from_b)

    for i, to_a in enumerate(left_a):
        left_b = [
            v
            for v in left_a if v != to_a]

        time_to_a = distance_to(network, from_a, to_a)

        new_time_left_a = time_left_a - time_to_a - 1

        for to_b in left_b:
            new_valves_left = [
                v
                for v in left_b if v != to_b]

            time_to_b = distance_to(network, from_b, to_b)

            new_time_left_b = time_left_b - time_to_b - 1

            new_score = 0
            if new_time_left_a > 0:
                new_score += new_time_left_a * valves[to_a]

            if new_time_left_b > 0:
                new_score += new_time_left_b * valves[to_b]

            if new_score == 0:
                continue
            
            if len(new_valves_left) > 0:
                if new_time_left_a > 2 and new_time_left_b > 2:
                    new_score += best_move_b(
                        network, valves,
                        to_a, to_b,
                        new_valves_left,
                        new_time_left_a,
                        new_time_left_b, depth+1)
                elif new_time_left_a > 2:
                    new_score += best_move_a(
                        network, valves,
                        to_a,
                        new_valves_left,
                        new_time_left_a)
                elif new_time_left_b > 2:
                    new_score += best_move_a(
                        network, valves,
                        to_b,
                        new_valves_left,
                        new_time_left_b)

            if best_score < new_score:
                best_score = new_score

        if depth == 0:
            print(best_score, len(best_move_cache))

    if key in best_move_cache and best_move_cache[key] != best_score:
        print(key, best_move_cache[key], best_score)
    best_move_cache[key] = best_score

    return best_score


def load_data(data):
    network = {}
    valves = {}
    for line in data:
        valve_info, network_info = line.split(';')
        _, valve_id, _, _, valve_rate = valve_info.split(' ')
        valve_rate = int(valve_rate.split('=')[1])
        valves[valve_id] = valve_rate
        network[valve_id] = []
        for joined in network_info.split(' valve')[1].strip(' s').split(', '):
            network[valve_id].append(joined)

    return network, valves


def simulate(data):
    network, valves = load_data(data)

    valves_left = [
        key
        for key, value in valves.items() if value > 0]

    print(len(valves_left))
    result_a = best_move_a(network, valves, 'AA', valves_left, 30)
    result_b = best_move_b(network, valves, 'AA', 'AA', valves_left, 26, 26)

    # code here
    return result_a, result_b


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_016.txt')
    results = simulate(data)
    print(results[0], 1724)
    print(results[1], 2283)


if __name__ == '__main__':
    main()
