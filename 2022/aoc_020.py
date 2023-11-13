def next_index(seq, items):
    for idx in range(len(items)):
        if items[idx][0] == seq:
            return idx

    raise IndexError(i)

    
def load_items(data, key):
    return [
        (i, int(n) * key)
        for i, n in enumerate(data)]


def decrypt(data, rounds, key):
    items = load_items(data, key)

    for round in range(rounds):
        for seq in range(len(items)):
            offset = next_index(seq, items)
            new_offset = (offset + items[offset][1])
    
            temp = items.pop(offset)
            new_offset %= len(items)
    
            items.insert(new_offset, temp)

    for offset in range(len(data)):
        if items[offset][1] == 0:
            break

    print(offset)
    result = (
        items[(offset + 1000) % len(items)][1],
        items[(offset + 2000) % len(items)][1],
        items[(offset + 3000) % len(items)][1])
    
    print(result)

    return sum(result)

def simulate(data):
    result_a = decrypt(data, 1, 1)
    result_b = decrypt(data, 10, 811589153)

    return result_a, result_b


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_020.txt')
    results = simulate(data)
    print(results[0], 13289)
    print(results[1], )


if __name__ == '__main__':
    main()
