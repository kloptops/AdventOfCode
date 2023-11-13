def sorty(items, cmp):
    results = []
    for item in items:
        for i in range(len(results)):
            if cmp(item, results[i]) < 0:
                results.insert(i, item)
                break
        else:
            results.append(item)

    return results


def load_list(text):
    return eval(text)


def compare_a(list_a, list_b):
    is_list_a = isinstance(list_a, list)
    is_list_b = isinstance(list_b, list)
    
    if is_list_a and is_list_b:
        for i in range(max(len(list_a), len(list_b))):
            if i >= len(list_a):
                return -1
            if i >= len(list_b):
                return 1

            cmp = compare_a(list_a[i], list_b[i])
            if cmp != 0:
                return cmp

        return 0

    elif is_list_a and not is_list_b:
        return compare_a(list_a, [list_b])

    elif not is_list_a and is_list_b:
        return compare_a([list_a], list_b)

    return max(-1, min(1, list_a - list_b))


def simulate(data):
    i = 0
    offset = 1
    total_a = 0
    key_a = [[2]]
    key_b = [[6]]

    packets = [
        key_a,
        key_b,
        ]

    while i < len(data):
        list_a = load_list(data[i])
        list_b = load_list(data[i+1])
        
        packets.append(list_a)
        packets.append(list_b)
        
        cmp = compare_a(list_a, list_b)
        if cmp < 0:
            total_a += offset
        
        print(offset, cmp)
        i += 3
        offset += 1

    packets = sorty(packets, compare_a)

    total_b = 1
    for i, packet in enumerate(packets, 1):
        print(i, packet)
        if packet == key_a:
            total_b *= i
        if packet == key_b:
            total_b *= i

    # code here
    return total_a, total_b


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_013.txt')
    results = simulate(data)
    print(results[0], 6076)
    print(results[1], 24805)


if __name__ == '__main__':
    main()
