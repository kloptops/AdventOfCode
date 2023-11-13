
def simulate(data):
    # code here

    move = {
        '<': (-1, 0),
        '^': ( 0,-1),
        '>': ( 1, 0),
        'v': ( 0, 1),
        }
    
    santa_a = [0, 0]
    santa_b = [0, 0]
    robot_b = [0, 0]
    
    visit_a = set()
    visit_b = set()
    
    visit_a.add(tuple(santa_a))
    visit_b.add(tuple(santa_b))

    for i, c in enumerate(data[0]):
        
        santa_a[0] += move[c][0]
        santa_a[1] += move[c][1]
        
        if i & 1:
            robot_b[0] += move[c][0]
            robot_b[1] += move[c][1]
        else:
            santa_b[0] += move[c][0]
            santa_b[1] += move[c][1]
        
        visit_a.add(tuple(santa_a))
        visit_b.add(tuple(santa_b))
        visit_b.add(tuple(robot_b))

    return len(visit_a), len(visit_b)


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_003.txt')

    results = simulate(data)
    print(results[0], 2592)
    print(results[1], 2360)

if __name__ == '__main__':
    main()

