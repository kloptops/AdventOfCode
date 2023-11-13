
def stepper(x1, y1, x2, y2):
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            yield y * 1000 + x

def turn_on(lights, steps):
    for step in steps:
        lights[step] = 1

def turn_off(lights, steps):
    for step in steps:
        lights[step] = 0

def toggle(lights, steps):
    for step in steps:
        if lights[step]:
            lights[step] = 0
        else:
            lights[step] = 1

def turn_up(lights, steps):
    for step in steps:
        lights[step] += 1

def turn_down(lights, steps):
    for step in steps:
        if lights[step] > 0:
            lights[step] -= 1

def double(lights, steps):
    for step in steps:
        lights[step] += 2

def simulate(data):
    # code here
    lights_a = [
        0
        for i in range(1000 * 1000)]

    lights_b = [
        0
        for i in range(1000 * 1000)]

    cmds_a = {
        'toggle': toggle,
        'turn on': turn_on,
        'turn off': turn_off,
        }
    
    cmds_b = {
        'toggle': double,
        'turn on': turn_up,
        'turn off': turn_down,
        }

    for line in data:
        cmd, start, _, end = line.rsplit(' ', 3)
        x1, y1 = map(int, start.split(','))
        x2, y2 = map(int, end.split(','))
        cmds_a[cmd](lights_a, stepper(x1, y1, x2, y2)) 
        cmds_b[cmd](lights_b, stepper(x1, y1, x2, y2))

    return sum(lights_a), sum(lights_b)


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_006.txt')
    results = simulate(data)

    print(results[0], 400410)
    print(results[1], 15343601)

if __name__ == '__main__':
    main()
