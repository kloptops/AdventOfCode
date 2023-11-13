def NOT(vm, data):
    value = fetch(vm, data[1])
    return (~(0x10000| value)) & 0xffff

def LSHIFT(vm, data):
    a = fetch(vm, data[1])
    b = fetch(vm, data[2])
    return (a << b) & 0xffff

def RSHIFT(vm, data):
    a = fetch(vm, data[1])
    b = fetch(vm, data[2])
    return (a >> b) & 0xffff

def RSHIFT(vm, data):
    a = fetch(vm, data[1])
    b = fetch(vm, data[2])
    return (a >> b) & 0xffff

def AND(vm, data):
    a = fetch(vm, data[1])
    b = fetch(vm, data[2])
    return (a & b) & 0xffff

def OR(vm, data):
    a = fetch(vm, data[1])
    b = fetch(vm, data[2])
    return (a | b) & 0xffff

insts = {
    'NOT': NOT,
    'LSHIFT': LSHIFT,
    'RSHIFT': RSHIFT,
    'AND': AND,
    'OR': OR,
    }

def fetch(vm, key):
    if isinstance(key, int):
        return key

    value = vm[key]
    
    if isinstance(value, list):
        result = insts[value[0]](vm, value)
        print(key, value, '=', result)
        vm[key] = result
        return result
    elif isinstance(value, str):
        result = fetch(vm, value)
        vm[key] = result
        return result
    else:
        return value

def to_value(data):
    if data.isdigit():
        return int(data)
    else:
        return data

def load_vm(data):
    vm = {}
    # code here
    for line in data:
        tokens = line.split(' ')
        output = tokens[-1]
        if output in vm:
            print('redefined ', output)

        if tokens[0] in ('NOT', ):
            vm[output] = [tokens[0], to_value(tokens[1])]
        elif tokens[1] == '->':
            vm[output] = to_value(tokens[0])
        else:
            vm[output] = [tokens[1], to_value(tokens[0]), to_value(tokens[2])]

    return vm

def simulate(data):
    vm = load_vm(data)
    
    result_a = fetch(vm, 'a')

    vm = load_vm(data)
    vm['b'] = result_a
    
    result_b = fetch(vm, 'a')
    
    return result_a, result_b


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_007.txt')
    results = simulate(data)
    
    print(results[0], 956)
    print(results[1], 40149)

if __name__ == '__main__':
    main()
