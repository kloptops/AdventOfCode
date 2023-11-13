
def inode():
    return {'size': 0, 'dirs': {}, 'files': {}}


def simulate(data):
    root = inode()
    stack = [root]
    cwd = root
    dirs = []

    for line in data:
        data = line.split(' ')
        if data[0] == '$':
            # command
            if data[1] == 'cd':
                if data[2] == '..':
                    stack.pop()
                    cwd = stack[-1]
                elif data[2] == '/':
                    stack = [root]
                    cwd = root
                else:
                    tmp = inode()
                    stack.append(tmp)
                    cwd['dirs'][data[2]] = tmp
                    cwd = tmp
                    dirs.append(tmp)
        else:
            if data[0] == 'dir':
                pass
            else:
                size = int(data[0])
                cwd['files'][data[1]] = size
                for item in stack:
                    item['size'] += size

    # part a       
    small_dirs = 0
    for item in dirs:
        if item['size'] <= 100000:
            small_dirs += item['size']
    
    # part b
    total = 70_000_000
    free = total - root['size']
    required = 30_000_000
    
    smallest_dir = total
    for item in dirs:
        if free + item['size'] > required:
            if item['size'] < smallest_dir:
                smallest_dir = item['size']

    return (small_dirs, smallest_dir)


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_007.txt')
    result = simulate(data)
    print(result[0], 1490523)
    print(result[1], 12390492)


if __name__ == '__main__':
    main()

