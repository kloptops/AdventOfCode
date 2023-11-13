def ingredient(line):
    name, properties = line.split(':')
    data = {}
    for property in properties.strip().split(', '):
        key, value = property.split(' ')
        data[key] = int(value)
    
    return name, data

def mix_series(amount, total):
    stack = [0] * (total-1)
    
    while True:
        result = []
        for i, x in enumerate(stack):
            result.append()
        stack[0] += 1
    
    print(final)

def simulate(data):
    # code here
    ingredients = {}
    names = []
    for line in data:
        name, info = ingredient(line)
        ingredients[name] = info
        names.append(name)
    
    print(names)

    mix_series(10, 4)
    return 0, 0


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_014.txt')
    results = simulate(data)
    print(results[0], )


if __name__ == '__main__':
    main()
