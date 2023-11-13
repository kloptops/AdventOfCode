def new_coord(coord, adj):
    return (coord[0] + adj[0], coord[1] + adj[1])


def map_display(coords, size):
    from PIL import Image
    
    size = size[:]

    size[1] *= 4
    size[0] *= 4

    im = Image.new('RGB', size, (64, 128, 255))
    
    pix = im.load()

    for y in range(size[1]):
        for x in range(size[0]):
            coord = (x, size[1] - y - 1)
            val = coords.get((x // 4, y // 4), ' ')
            if val == '|':
                pix[coord] = 0,0,0
            
            if val == '#':
                pix[coord] = 153, 94, 15

    im.show()


shapes = (
    # ####
    ((0, 0), (1, 0), (2, 0), (3, 0)),

    # .#.
    # ###
    # .#.
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),

    # ..#
    # ..#
    # ###
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),

    # #
    # #
    # #
    # #
    ((0, 0), (0, 1), (0, 2), (0, 3)),

    # ##
    # ##
    ((0, 0), (1, 0), (0, 1), (1, 1)),
    )


def check_collide(stage, location, shape):
    for cell in shape:
        hit = stage.get(new_coord(location, cell), ' ')
        if hit != ' ':
            return hit
    
    return ' '


def settle(stage, location, shape):
    for cell in shape:
        stage[new_coord(location, cell)] = '#'


def max_height(stage, width):
    if 'height' in stage:
        y = stage['height']

    y = 0
    while True:
        for x in range(1, width+1):
            if stage.get((x, y), ' ') != ' ':
                break
        else:
            stage['height'] = y
            return y

        y += 1


def build_walls(stage, width, height):
    for y in range(height):
        stage[(0, y)] = '|'
        stage[(width+1, y)] = '|'


def build_floor(stage, width):
    for x in range(width):
        stage[(x+1, 0)] = '#'


def line_code(stage, width, y):
    output = 0
    for x in range(width):
        if stage.get((x, y), ' ') != ' ':
            output |= 1<<x
    return output


def signatures(codes, min_length):
    if len(codes) < min_length:
        return

    for i in range(len(codes)-1, min_length-1, -1):
        yield tuple(codes[-i:])


def simulate(wind, width, rounds):
    wind_move = {
        '>': ( 1, 0),
        '<': (-1, 0),
        }

    stage = {}
    build_floor(stage, width)
    build_walls(stage, width, 10)

    base_height = 0

    patterns = {}
    pattern = []
    pattern_length = 200

    optimal_height = None
    optimal_move = None
    optimal_wind = None

    i = 0
    w = 0
    while i < rounds:
        if optimal_height is not None:
            if (i + optimal_move) < rounds:
                print(rounds - i, optimal_move)
                shift_amount = (rounds - i) // optimal_move
                print(shift_amount)

                i += optimal_move * shift_amount
                base_height += optimal_height * shift_amount
                w += optimal_wind * shift_amount
                #base_height -= 1

                continue

        shape = shapes[i % len(shapes)]
        height = max_height(stage, width)

        location = (3, height+3)
        build_walls(stage, width, height+10)

        while True:
            new_location = new_coord(location, wind_move[wind[w % len(wind)]])
            w += 1
            hit = check_collide(stage, new_location, shape)
            if hit == ' ':
                location = new_location

            new_location = new_coord(location, (0, -1))
            hit = check_collide(stage, new_location, shape)
            if hit != ' ':
                settle(stage, location, shape)
                break

            location = new_location


        if optimal_height is None:
            new_height = max_height(stage, width)
            output = 0
            for x in range(height, new_height+1):
                output <<= 8
                output |= line_code(stage, width, x)
    
            pattern.append(output)
            while len(pattern) > pattern_length:
                pattern.pop(0)

            for signature in signatures(pattern, 11):
                if signature not in patterns:
                    patterns[signature] = [1, new_height, i, w]
                else:
                    sig = patterns[signature]
                    sig[0] += 1
                    
                    if sig[0] > 3:
                        print(f'{i}, {len(signature)}, {i - sig[2]}, {new_height - sig[1]}, {w - sig[3]}')
                        
                        optimal_height = new_height - sig[1]
                        optimal_move = i - sig[2]
                        optimal_wind = w - sig[3]
                        break

                    sig[1] = new_height
                    sig[2] = i
                    sig[3] = w

        i += 1


        #print(height, output, i % len(shapes))
        #if height > 295 and height < 300:
        #    map_display(stage, [9, height+20])

    result_a = max_height(stage, width) + base_height

    # code here
    return result_a-1


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_017.txt')

    sample_a = simulate('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 7, 2022)
    print(sample_a, 3068)
    sample_b = simulate('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>', 7, 1_000_000_000_000)
    print(sample_b, 1514285714288)

    result_a = simulate(data[0], 7, 2022)
    print(result_a, 3157)
    result_b = simulate(data[0], 7, 1_000_000_000_000)
    print(result_b, 1564285714319)


if __name__ == '__main__':
    main()


