adjacents = (
    ( 1, 0, 0),
    (-1, 0, 0),
    ( 0, 1, 0),
    ( 0,-1, 0),
    ( 0, 0, 1),
    ( 0, 0,-1))


def new_coord(coord, adj):
    return (
        coord[0] + adj[0],
        coord[1] + adj[1],
        coord[2] + adj[2])


def adjacent_coords(coord):
    for adjacent in adjacents:
        yield new_coord(coord, adjacent)


def load_cubes(data):
    all_cubes = []
    for line in data:
        cube = tuple(map(int, line.split(',')))
        all_cubes.append(cube)
    
    return all_cubes


def group_cubes(all_cubes):
    cube_groups = []
    while len(all_cubes) > 0:
        cube_stack = [all_cubes.pop(0)]
        cube_group = []
        while len(cube_stack) > 0:
            cube = cube_stack.pop(0)
            cube_group.append(cube)

            for adj_cube in adjacent_coords(cube):
                if adj_cube in all_cubes:
                    all_cubes.remove(adj_cube)
                    cube_stack.append(adj_cube)
        
        cube_groups.append(cube_group)

    return cube_groups


def count_sides_a(cubes):
    sides = 0
    for cube in cubes:
        for adj_cube in adjacent_coords(cube):
            if adj_cube not in cubes:
                sides += 1

    return sides


def count_sides_b(cubes, air_cubes):
    sides = 0
    for cube in cubes:
        for adj_cube in adjacent_coords(cube):
            if adj_cube in cubes:
                continue

            if adj_cube not in air_cubes:
                continue

            sides += 1

    return sides


def simulate(data):
    all_cubes = load_cubes(data)
    
    max_x = max((cube[0] for cube in all_cubes)) + 1
    max_y = max((cube[1] for cube in all_cubes)) + 1
    max_z = max((cube[2] for cube in all_cubes)) + 1
    print(max_x, max_y, max_z)

    air_cubes = set()
    air_stack = [(-1, -1, -1)]
    seen_cubes = set(air_stack[0])

    while len(air_stack) > 0:
        cube = air_stack.pop(0)
        air_cubes.add(cube)
        seen_cubes.add(cube)

        for adj_cube in adjacent_coords(cube):
            if adj_cube in all_cubes:
                continue

            if adj_cube in seen_cubes:
                continue

            if not (-1 <= adj_cube[0] <= max_x):
                continue

            if not (-1 <= adj_cube[1] <= max_y):
                continue

            if not (-1 <= adj_cube[2] <= max_z):
                continue

            seen_cubes.add(adj_cube)
            air_stack.append(adj_cube)
    
    print(len(air_cubes))

    cube_groups = group_cubes(all_cubes)

    print(len(cube_groups))

    total_sides_a = 0
    total_sides_b = 0
    for cube_group in cube_groups:
        sides_a = count_sides_a(cube_group)
        sides_b = count_sides_b(cube_group, air_cubes)

        print(len(cube_group), sides_a, sides_b)
        total_sides_a += sides_a
        total_sides_b += sides_b

    # code here
    return total_sides_a, total_sides_b


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_018.txt')
    results = simulate(data)
    print(results[0], '==' , 3396)
    print(results[1], '==' , 2044)


if __name__ == '__main__':
    main()

