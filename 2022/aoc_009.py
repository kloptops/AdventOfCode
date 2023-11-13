def do_move(head, dir):
    dir_move = {
        'L': (-1, 0),
        'R': ( 1, 0),
        'U': ( 0, 1),
        'D': ( 0,-1),
        }

    head[0] += dir_move[dir][0]
    head[1] += dir_move[dir][1]


def do_update(head, tail):
    x_diff = (head[0] - tail[0])
    y_diff = (head[1] - tail[1])

    if x_diff == 0 and abs(y_diff) > 1:
        tail[1] += min(1, max(-1, y_diff))

    elif y_diff == 0 and abs(x_diff) > 1:
        tail[0] += min(1, max(-1, x_diff))

    elif abs(x_diff) > 1 or abs(y_diff) > 1:
        tail[0] += min(1, max(-1, x_diff))
        tail[1] += min(1, max(-1, y_diff))


def simulate(length, data):
    rope = [
        [0, 0]
        for _ in range(length)]

    seen = {(0, 0)}

    for line in data:
        dir, amount = line.split(' ')

        for _ in range(int(amount)):
            do_move(rope[0], dir)
            
            for head, tail in zip(rope[:-1], rope[1:]):
                do_update(head, tail)
            
            seen.add(tuple(rope[-1]))
    
    return len(seen)


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_009.txt')
    print(simulate(2, data), 6087)
    print(simulate(10, data), 2493)

    
if __name__ == '__main__':
    main()

