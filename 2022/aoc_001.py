def simulate(data):
    result = [0]
    for line in data:
        if line == '':
            result.append(0)
            continue
        
        result[-1] += int(line)
    
    result.sort()
    return result

def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data

def main():
    data = get_data('data/input_001.txt')
    result = simulate(data)
    print(result[-1], 66306)
    print(sum(result[-3:]), 195292)

if __name__ == '__main__':
    main()

