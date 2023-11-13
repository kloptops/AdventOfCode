def cmp(a, b):
    return (a - b)


def move_dir(a):
    return min(1, max(-1, a))


def load_monkeys(data):
    monkeys = {}
    for line in data:
        monkey_name, monkey_data = line.split(': ')
        
        if not monkey_data.isdigit():
            t = monkey_data.split(' ')
            monkey_data = [t[1], t[0], t[2]]
        else:
            monkey_data = [int(monkey_data)]

        monkeys[monkey_name] = monkey_data
        #print(monkey_name, monkey_data)

    return monkeys


def monkey_calculate(monkeys, start):
    ops = {
        '+': (lambda a, b: a + b),
        '-': (lambda a, b: a - b),
        '*': (lambda a, b: a * b),
        '/': (lambda a, b: a / b),
        '=': cmp,
        }
    
    stack = [start]
    output = []

    offset = 0

    round = 0
    while len(stack) > 0:
        #print(round, stack, output)
        round += 1

        value = stack.pop(-1)

        if value in monkeys:
            stack.extend(monkeys[value])
            continue

        if isinstance(value, (int, float)):
            output.append(value)
            continue

        if value in '+-*/=':
            assert len(output) >= 2
            a, b = output.pop(-1), output.pop(-1)

            output.append(ops[value](a, b))

    #print(round, stack, output)
    return output[0]


def simulate(data):
    monkeys = load_monkeys(data)

    result_a = monkey_calculate(monkeys, 'root')

    monkeys['root'][0] = '='
    humn = monkeys['humn'][0]

    tries = 0
    direction = None
    last_diff = None

    while True:
        monkeys['humn'][0] = humn
        current = monkey_calculate(monkeys, 'root')

        diff = (0 - current)
        print(tries, diff, current)
        if current == 0:
            break

        if tries > 1000:
            break

        if direction is None:
            direction = move_dir(diff)

        z_diff = move_dir(diff)
        diff //= 10

        if diff == 0:
            diff = z_diff

        if direction > 0:
            humn += diff
        else:
            humn -= diff

        tries += 1
    
    # code here
    return int(result_a), int(humn)


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())

    return data


def main():
    data = get_data('data/input_021.txt')

    results = simulate(data)
    print(results[0], '==', 72664227897438)
    print(results[1], '==', 3916491093817)


if __name__ == '__main__':
    main()
