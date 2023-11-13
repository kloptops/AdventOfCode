import json

def walk_a(data, numbers=None):
    if numbers is None:
        numbers = []
    
    if isinstance(data, list):
        for value in data:
            if isinstance(value, (dict, list)):
                walk_a(value, numbers)
            elif isinstance(value, int):
                numbers.append(value)
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                walk_a(value, numbers)
            elif isinstance(value, int):
                numbers.append(value)
    elif isinstance(data, int):
        numbers.append(data)
    
    return numbers

def walk_b(data, numbers=None):
    if numbers is None:
        numbers = []
    
    if isinstance(data, list):
        for value in data:
            if isinstance(value, (dict, list)):
                walk_b(value, numbers)
            elif isinstance(value, int):
                numbers.append(value)
    elif isinstance(data, dict):
        new_numbers = []
        bad = False
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                walk_b(value, new_numbers)
            elif isinstance(value, int):
                new_numbers.append(value)
            elif value == 'red':
                bad = True
        
        if not bad:
            numbers.extend(new_numbers)

    elif isinstance(data, int):
        numbers.append(data)
    
    return numbers

def simulate(data):
    # code here
    data = json.loads(data[0])
    
    numbers_a = walk_a(data)
    numbers_b = walk_b(data)

    return sum(numbers_a), sum(numbers_b)


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_012.txt')
    results = simulate(data)
    print(results[0], 191164)
    print(results[1], 87842)


if __name__ == '__main__':
    main()
