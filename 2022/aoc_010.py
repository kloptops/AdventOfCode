def cpu(code):
    x = 1

    for line in code:
        inst = line.split(' ')
        if inst[0] == 'noop':
            yield x
        elif inst[0] == 'addx':
            yield x
            yield x
            x += int(inst[1])


def simulate_a(data, cycles):
    # code here
    total = 0
    for cycle, x in enumerate(cpu(data), 1):
        if cycle in cycles:
            print(f'{cycle}, {x}: {x * cycle}')
            total += x * cycle
    
    return total


def simulate_b(data):
    # code here
    output = []
    for cycle, reg in enumerate(cpu(data)):
        if cycle > 0 and (cycle % 40) == 0:
            print(''.join(output))
            output = []

        offset = (cycle % 40)
        if abs((offset) - reg) < 2:
            output.append('#')
        else:
            output.append('.')

    print(''.join(output))

    return ''


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_010.txt')
    print(simulate_a(data, (20, 60, 100, 140, 180, 220)), 12460)
    simulate_b(data)
    print('EZFPRAKL')


if __name__ == '__main__':
    main()

