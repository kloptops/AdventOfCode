def ranger(a):
    b = a.split('-')
    return set(range(int(b[0]), int(b[1]) + 1))


def simulate(data):
    total_a = 0
    total_b = 0

    for line in data:
        a, b = map(ranger, line.split(','))
        
        if len(a.intersection(b)) >= 1:
            total_b += 1
        
        if len(a.intersection(b)) == len(a):
            total_a += 1
        elif len(b.intersection(a)) == len(b):
            total_a += 1
    
    return (total_a, total_b)


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data

def main():
    data = get_data('data/input_004.txt')
    result = simulate(data)
    print(result[0], 487)
    print(result[1], 849)

if __name__ == '__main__':
    main()

