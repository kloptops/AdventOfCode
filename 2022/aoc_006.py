
def simulate(data, length):
    # code here
    for i in range(len(data)):
        a = set(data[i:i+length])
        if len(a) == length:
            # print(data[i:i+length], i, i+length)
            return i + length


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_006.txt')
    print(simulate(data[0],  4), 1198)
    print(simulate(data[0], 14), 3120)


if __name__ == '__main__':
    main()

