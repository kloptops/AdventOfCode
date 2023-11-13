
def parse_monkeys(data):
    monkeys = [{'inspections': 0}]
    tests = []
    for line in data:
        if line == '':
            monkeys.append({'inspections': 0})
            continue

        if line.startswith('Monkey'):
            continue

        if line.startswith('Starting'):
            monkeys[-1]['items'] = list(map(int, line.split(': ')[1].split(', ')))
            continue

        if line.startswith('Operation'):
            monkeys[-1]['operation'] = eval("lambda old: " + line.split(' = ')[1])
            continue

        if line.startswith('Test'):
            monkeys[-1]['test'] = int(line.split(' by ')[1])
            tests.append(monkeys[-1]['test'])
            continue

        if line.startswith('If true'):
            monkeys[-1]['true'] = int(line.rsplit(' ', 1)[1])
            continue

        if line.startswith('If false'):
            monkeys[-1]['false'] = int(line.rsplit(' ', 1)[1])
            continue
    
    total = tests[0]
    for x in tests[1:]:
        total *= x

    return monkeys, total

def monkey_simulate(monkey, monkeys, mode_a, maximus):
    for item in monkey['items']:
        temp = monkey['operation'](item)
        if mode_a:
            temp //= 3
        
        temp %= maximus

        result = (temp % monkey['test']) == 0 and 'true' or 'false'
        target = monkey[result]
        
        monkeys[target]['items'].append(temp)
        monkey['inspections'] += 1

    monkey['items'] = []

def simulate(data, rounds, mode_a=True):
    monkeys, maximus = parse_monkeys(data)
    
    for i in range(rounds):
        print(f'Round {i}')
        for monkey in monkeys:
            monkey_simulate(monkey, monkeys, mode_a, maximus)

    inspections = []
    for monkey in monkeys:
        inspections.append(monkey['inspections'])
    
    inspections.sort()
    
    # code here
    return inspections[-1] * inspections[-2]


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_011.txt')

    print(simulate(data, 20, True), 58056)
    print(simulate(data, 10000, False), 58056)


if __name__ == '__main__':
    main()
