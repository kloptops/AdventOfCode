def new_coord(coord, adj):
    return (coord[0] + adj[0], coord[1] + adj[1])


def map_display(coords, size):
    from PIL import Image
    
    size = size[:]

    size[1] += 10

    im = Image.new('RGB', size, (64, 128, 255))
    
    pix = im.load()

    for y in range(size[1]):
        for x in range(size[0]):
            coord = (x, y)
            val = coords.get(coord, ' ')
            if val == '#':
                pix[coord] = 0,0,0
            
            if val == 'o':
                pix[coord] = 153, 94, 15

    im.show()


def draw_line(coords, coord_a, coord_b):
    if coord_a[0] == coord_b[0]:
        if coord_b[1] < coord_a[1]:
            coord_a, coord_b = coord_b, coord_a

        for i in range(coord_a[1], coord_b[1]+1):
            coords[(coord_a[0], i)] = '#'
    else:
        if coord_b[0] < coord_a[0]:
            coord_a, coord_b = coord_b, coord_a

        for i in range(coord_a[0], coord_b[0]+1):
            coords[(i, coord_a[1])] = '#'


def load_map(data):
    coords = {}
    size = [0, 0]
    for line in data:
        segments = [
            tuple(map(int, line.split(',')))
            for line in line.split(' -> ')]
        
        for coord_a, coord_b in zip(segments[:-1], segments[1:]):
            draw_line(coords, coord_a, coord_b)
            
            if coord_a[0] > size[0]:
                size[0] = coord_a[0]

            if coord_a[1] > size[1]:
                size[1] = coord_a[1]

            if coord_b[0] > size[0]:
                size[0] = coord_b[0]

            if coord_b[1] > size[1]:
                size[1] = coord_b[1]

    size[0] += 100
    
    return coords, size


def simulate_sand(coords, size, coord):
    while coord[1] < size[1]:
        new_loc = new_coord(coord, (0, 1))
        if coords.get(new_loc, ' ') == ' ':
            coord = new_loc
            continue

        new_loc = new_coord(coord, (-1, 1))
        if coords.get(new_loc, ' ') == ' ':
            coord = new_loc
            continue

        new_loc = new_coord(coord, (1, 1))
        if coords.get(new_loc, ' ') == ' ':
            coord = new_loc
            continue

        coords[coord] = 'o'
        break

    return coord


def simulate(data):
    coords, size = load_map(data)

    counter_a = 0
    while True:
        location = simulate_sand(coords, size, (500, 0))

        if counter_a % 100 == 0:
            map_display(coords, size)
            print(counter_a, location)

        if location[1] >= size[1]:
            break
        
        counter_a += 1
    
    size[1] += 2

    draw_line(coords, (0, size[1]), (size[0]+500, size[1]))

    counter_b = counter_a
    while True:
        location = simulate_sand(coords, size, (500, 0))

        if counter_b % 1000 == 0:
            map_display(coords, size)
            print(counter_b, location)

        if location[1] == 0:
            break

        counter_b += 1

    map_display(coords, size)
    # code here
    return counter_a, counter_b+1


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())

    return data


def main():
    data = get_data('data/input_014.txt')
    results = simulate(data)
    print(results[0], 1199)
    print(results[1], 23925)


if __name__ == '__main__':
    main()
