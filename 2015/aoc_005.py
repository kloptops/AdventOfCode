
def is_nice_a(text):
    vowels = 'aeiou'
    doubles = (
        'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg',
        'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn',
        'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu',
        'vv', 'ww', 'xx', 'yy', 'zz')
    bads = ('ab', 'cd', 'pq', 'xy')

    count = 0
    for v in vowels:
        count += text.count(v)
    if count < 3:
        return False
    
    for db in doubles:
        if db in text:
            break
    else:
        return False
    
    for bd in bads:
        if bd in text:
            return False
    
    return True


def is_nice_b(text):
    for i in range(len(text)):
        if text[i:i+2] in text[i+2:]:
            break
    else:
        # print('fail 1 -', text)
        return False

    for i in range(len(text)-2):
        if text[i] == text[i+2]:
            break
    else:
        # print('fail 2 -', text)
        return False
    
    # print('passed -', text)
    return True


def simulate(data):
    # code here
    nice_a = 0
    nice_b = 0

    for line in data:
        if is_nice_a(line):
            nice_a += 1
        if is_nice_b(line):
            nice_b += 1

    return nice_a, nice_b


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_005.txt')
    results = simulate(data)
    print(results[0], 238)
    print(results[1], 69)

if __name__ == '__main__':
    main()
