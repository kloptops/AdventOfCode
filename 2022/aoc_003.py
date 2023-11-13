def match(a, b):
    return ''.join(list(set(a).intersection(b)))


def value(a):
    result = 0

    for x in a:
        result += 1 + 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(x)
    
    return result    


def simulate(data):
    a_total = 0
    b_total = 0
    group = []

    for line in data:
        a = line[:(len(line)//2)]
        b = line[(len(line)//2):]

        x = match(a, b)
        z = value(x)

        print(f'{a},{b}: {x}, {z}')
        a_total += z
        group.append(line)
        if len(group) == 3:
            x = match(group[0], group[1])
            x = match(x, group[2])
            z = value(x)
            print(f'{x}: {z}')
            b_total += z
            group = []
    
    return a_total, b_total


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_003.txt')
    result = simulate(data)
    print(result[0], 8085)
    print(result[1], 2515)


if __name__ == '__main__':
    main()

