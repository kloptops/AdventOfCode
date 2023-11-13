def group(text):
    output = []

    i = 1
    last = text[0]
    amount = 1
    while i < len(text):
        if last == text[i]:
            i += 1
            amount += 1
            continue
        else:
            output.extend((str(amount), last))
            last = text[i]
            amount = 1
            i += 1
    output.extend((str(amount), last))

    return ''.join(output)

def simulate(data):
    for _ in range(40):
        data = group(data)
    
    len_a = len(data)
    for _ in range(10):
        data = group(data)

    return len_a, len(data)


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = '3113322113'
    results = simulate(data)
    print(results[0], 329356)
    print(results[1], )


if __name__ == '__main__':
    main()
