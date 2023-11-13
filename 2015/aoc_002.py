def simulate(data):
    # code here
    total_paper = 0
    total_ribbon = 0

    for line in data:
        w, h, l = sorted(list(map(int, line.split('x'))))
        a, b, c = sorted(((w * h),(h * l),(w * l)))
        paper_area = (a + b + c) * 2
        paper_area += a

        ribbon_length = (w * 2) + (h * 2) + (w * h * l)
        
        print(f'{w}x{h}x{l} = {paper_area},{ribbon_length}')
        total_ribbon += ribbon_length
        total_paper += paper_area
 
    return total_paper, total_ribbon


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_002.txt')
    result = simulate(data)
    print(result[0], 1606483)
    print(result[1], 3842356)


if __name__ == '__main__':
    main()
