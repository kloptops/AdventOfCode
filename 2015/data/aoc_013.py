def simulate(data):
    # code here
    return 0, 0


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_001.txt')
    results = simulate(data)
    print(results[0], )


if __name__ == '__main__':
    main()
