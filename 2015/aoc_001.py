def simulate(data):
    # code here
    floor = 0
    first = 0
    for i, c in enumerate(data[0], 1):
        if c == '(':
            floor += 1
        elif c == ')':
            floor -= 1
            if first == 0 and floor == -1:
                first = i
    
    return floor, first


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_001.txt')
    result = simulate(data)
    print(result[0], 232)
    print(result[1], 1783)


if __name__ == '__main__':
    main()
