import hashlib

def hash(text):
    return hashlib.md5(
        text.encode('utf8')).hexdigest()

def simulate(data):
    # code here
    i = 0
    fives = None
    sixes = None
    while fives is None or sixes is None:
        i += 1
        test = hash(data + str(i))
        if fives is None and test.startswith('00000'):
            fives = i
        if sixes is None and test.startswith('000000'):
            sixes = i

    return fives, sixes


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = 'iwrupvqb'
    results = simulate(data)
    print(results[0], 346386)
    print(results[1], 9958218)

if __name__ == '__main__':
    main()
