DIRS = ('>', 'v', '<', '^')
DIR_REF = {
    '>': '<',
    '<': '>',
    '^': 'v',
    'v': '^',
    }

DIR_STEP = {
    '>': ( 1, 0),
    '<': (-1, 0),
    '^': ( 0,-1),
    'v': ( 0, 1),
    }

DIR_TURN = {
    ('>', 'L'): '^',
    ('>', 'R'): 'v',
    ('^', 'L'): '<',
    ('^', 'R'): '>',
    ('<', 'L'): 'v',
    ('<', 'R'): '^',
    ('v', 'L'): '>',
    ('v', 'R'): '<',
    }

DIR_ANGLE = {
    ('>', '^'): 270,
    ('>', '<'): 180,
    ('>', 'v'): 90,
    ('>', '>'): 0,

    ('^', '<'): 270,
    ('^', 'v'): 180,
    ('^', '>'): 90,
    ('^', '^'): 0,

    ('<', '<'): 0,
    ('<', '^'): 90,
    ('<', '>'): 180,
    ('<', 'v'): 270,

    ('v', 'v'): 0,
    ('v', '<'): 90,
    ('v', '^'): 180,
    ('v', '>'): 270,
    }

DIR_TO_DIR = {
    '>^': ('<', '^'),
    '>v': ('<', 'v'),
    'v<': ('^', '<'),
    'v>': ('^', '>'),
    '<^': ('>', '^'),
    '<v': ('>', 'v'),
    '^<': ('v', '<'),
    '^>': ('v', '>'),
    '>>^': ('^', '^'),
    '>>>': ('>', '<'),
    '>>v': ('v', 'v'),
    'vv<': ('<', '<'),
    'vvv': ('v', '^'),
    'vv>': ('>', '>'),
    '<<^': ('^', '^'),
    '<<<': ('<', '>'),
    '<<v': ('v', 'v'),
    '^^<': ('<', '<'),
    '^^^': ('^', 'v'),
    '^^>': ('>', '>'),
    }


def dir_nomalise(dir, angle):
    temp = DIRS[(
        DIRS.index(dir) - (angle // 90)) % len(DIRS)]
    
    #print(dir, angle, temp)
    return temp


def step_directions(cubes, from_coord, directions):
    start_coord = from_coord
    angle = 0
    cur_coord = from_coord
    for next_dir in directions:
        cur_cube = cubes[cur_coord]

        if angle > 0:
            next_dir = dir_nomalise(next_dir, angle)

        if next_dir not in cur_cube[3]:
            return None, 0

        angle, next_coord = cur_cube[3][next_dir]
        cur_coord = next_coord

    return cur_coord, angle


def adj_coord(coord, adj):
    return (coord[0] + adj[0], coord[1] + adj[1])

def neg_coord(coord, adj):
    return (coord[0] - adj[0], coord[1] - adj[1])

def do_turn(direction, adj):
    return DIR_TURN[(direction, adj)]


def do_wrap_2d(topo, wrap, coord, direction):
    x, y = coord
    if direction == '>':
        return (wrap[('min_x', y)], y), direction

    elif direction == '<':
        return (wrap[('max_x', y)], y), direction

    elif direction == 'v':
        return (x, wrap[('min_y', x)]), direction

    elif direction == '^':
        return (x, wrap[('max_y', x)]), direction


def do_wrap_3d(topo, cubes, coord, direction):
    cur_loc = (coord[0] // cubes['size'], coord[1] // cubes['size'])

    half_size = cubes['size'] // 2

    cur_cube = cubes[cur_loc]

    new_angle, new_loc = cur_cube[3][direction]
    new_cube = cubes[new_loc]

    base_coord = neg_coord(coord, cur_cube[1])

    if new_angle > 0:
        base_coord = neg_coord(base_coord, (half_size, half_size))

        for i in range(new_angle // 90):
            base_coord = (base_coord[1], base_coord[0] * -1)

        base_coord = adj_coord(base_coord, (half_size, half_size))
    
        direction = dir_nomalise(direction, new_angle)
    
    return adj_coord(base_coord, new_cube[1]), direction


def do_walk(topo, coord, direction, wrap, wrap_func):
    new_coord = adj_coord(coord, DIR_STEP[direction])
    new_direction = direction
    if new_coord not in topo:
        new_coord, new_direction = wrap_func(topo, wrap, coord, direction)
        
        print(coord, new_coord)

    if topo[new_coord] == '#':
        return coord, direction

    return new_coord, new_direction


def load_topo(data, cubed):
    start = None
    topo = {}
    wraps = {}
    sides = 0
    cubes = {}

    for y, line in enumerate(data[:-2]):
        for x, c in enumerate(line):
            if c == ' ':
                continue

            if start is None:
                start = (x, y)
            
            cube = (x // cubed, y // cubed)
            if cube not in cubes:
                cubes[cube] = [sides, (x, y), (x, y), {}]
                sides += 1
            else:
                cubes[cube][2] = (x, y)

            topo[(x, y)] = c

            wraps[('min_x', y)] = min(wraps.get(('min_x', y), x), x)
            wraps[('max_x', y)] = max(wraps.get(('max_x', y), x), x)

            wraps[('min_y', x)] = min(wraps.get(('min_y', x), y), y)
            wraps[('max_y', x)] = max(wraps.get(('max_y', x), y), y)

    instructions = ['']
    for c in data[-1]:
        if c.isdigit():
            instructions[-1] += c
        else:
            instructions[-1] = int(instructions[-1])
            instructions.append(c)
            instructions.append('')

    if instructions[-1] != '':
        instructions[-1] = int(instructions[-1])
    else:
        del instructions[-1]

    # calculate the adjacent faces of a cube. and the rotation between them
    unfinished = list(cubes.keys())
    # stage 1
    for cube_loc in unfinished:
        for direction, adj in DIR_STEP.items():
            adj_loc = adj_coord(cube_loc, adj)
        
            if adj_loc not in cubes:
                continue

            cubes[cube_loc][3][direction] = (0, adj_loc)

    rounds = 0
    # calculate steps
    while len(unfinished) > 0:
        from_loc = unfinished.pop(0)
        from_cube = cubes[from_loc]
        rounds += 1

        if len(from_cube[3]) == 4:
            # this cube is done
            continue

        if rounds > 12:
            break

        print(f'{from_loc}:')
        for to_dirs, (to_dir, from_dir) in DIR_TO_DIR.items():
            to_loc, to_angle = step_directions(cubes, from_loc, to_dirs)
            if to_loc is None:
                continue

            to_angle = (to_angle + DIR_ANGLE[to_dir, from_dir]) % 360
            from_angle = (to_angle + 180) % 360
            #to_dir = dir_nomalise(to_dir, to_angle)

            print(f'    {to_dirs}: {to_loc}, {to_angle}')

            to_cube = cubes[to_loc]
            if to_dir in to_cube[3]:
                continue

            if from_dir in from_cube[3]:
                continue

            if from_dir in from_cube[3]:
                assert from_cube[3][from_dir][1] == to_loc, f'{from_cube[3][from_dir][1]} == {to_loc}'
                print('fuck')
                for t_loc, t_cube in cubes.items():
                    print(t_loc)
                    for direction, (n_angle, n_loc) in t_cube[3].items():
                        print(f'  {direction}: {n_loc}, {n_angle}' )
                break

            to_cube[3][to_dir] = (to_angle, from_loc)
            from_cube[3][from_dir] = (from_angle, to_loc)

        unfinished.append(from_loc)
    
    for t_loc, t_cube in cubes.items():
        print(t_loc, t_cube[0:3])
        for direction, (n_angle, n_loc) in t_cube[3].items():
            print(f'  {direction}: {n_loc}, {n_angle}' )

    cubes['size'] = cubed
    return topo, wraps, cubes, start, instructions


def simulate(data, cubed):
    topo, wraps, cubes, start, instructions = load_topo(data, cubed)

    #print(instructions)
    #print(warps)
    coord_a = start
    direction_a = '>'

    for instruct in instructions:
        if isinstance(instruct, int):
            for i in range(instruct):
                coord_a, direction_a = do_walk(topo, coord_a, direction_a, wraps, do_wrap_2d)
        else:
            direction_a = do_turn(direction_a, instruct)


    print(start, coord_a)
    
    coord_b = start
    direction_b = '>'

    for instruct in instructions:
        if isinstance(instruct, int):
            for i in range(instruct):
                coord_b, direction_b = do_walk(topo, coord_b, direction_b, cubes, do_wrap_3d)
        else:
            direction_b = do_turn(direction_b, instruct)

    result_a = (
        ((coord_a[1] + 1) * 1000) +
        ((coord_a[0] + 1) * 4) +
        DIRS.index(direction_a))

    result_b = (
        ((coord[1] + 1) * 1000) +
        ((coord[0] + 1) * 4) +
        DIRS.index(direction_b))

    return result_a, 0


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.rstrip())
    
    return data


def main():
    data = get_data('data/input_022t.txt')
    results = simulate(data, 4)
    print(results[0], 196134)
    print(results[1], )


if __name__ == '__main__':
    main()
