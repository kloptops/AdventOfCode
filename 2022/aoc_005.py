
def simulate(data, mode):
    STACKS, INSTRUCTIONS = 0, 1

    stacks = [None]

    state = STACKS
    for line in data:
        if state == STACKS:
            if line.strip() == '':
                state = INSTRUCTIONS
                continue
            
            if not line.strip().startswith('['):
                continue
            
            for i, c in enumerate(line[1::4], 1):
                while i >= len(stacks):
                    stacks.append([])
                if c != ' ':
                    stacks[i].insert(0, c)
        
        elif state == INSTRUCTIONS:
            _, amount, _, from_stack, _, to_stack = line.strip().split(' ')
            if mode == 1:
                for i in range(int(amount)):
                    tmp = stacks[int(from_stack)].pop()
                    stacks[int(to_stack)].append(tmp)
            else:
                tmp = stacks[int(from_stack)][-int(amount):]
                del stacks[int(from_stack)][-int(amount):]
                stacks[int(to_stack)].extend(tmp)
    
    return ''.join([x[-1] for x in stacks[1:]])


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.rstrip())
    
    return data


def main():
    data = get_data('data/input_005.txt')
    print(simulate(data, 1), 'SHQWSRBDL')
    print(simulate(data, 2), 'CDTQZHBRS')


if __name__ == '__main__':
    main()

