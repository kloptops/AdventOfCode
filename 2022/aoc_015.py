class SensorPair():
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.bx = coords[2]
        self.by = coords[3]

        self.r = (
            abs(self.x - self.bx) +
            abs(self.y - self.by))

    def in_range(self, coord):
        return (abs(self.x - coord[0]) + abs(self.y - coord[1])) <= self.r

    def min_x(self, y):
        if not (self.minimum_y <= y <= self.maximum_y):
            return None

        return self.x - (self.r - abs(y - self.y))

    def max_x(self, y):
        if not (self.minimum_y <= y <= self.maximum_y):
            return None

        return self.x + (self.r - abs(y - self.y))

    def min_y(self, x):
        if not (self.minimum_x <= x <= self.maximum_x):
            return None

        return self.y - (self.r - abs(x - self.x))

    def max_y(self, coord):
        if not (self.minimum_x <= x <= self.maximum_x):
            return None

        return self.y + (self.r - abs(x - self.x))

    @property
    def beacon(self):
        return (self.bx, self.by)

    @property
    def coord(self):
        return (self.x, self.y)

    @property
    def maximum_x(self):
        return self.x + self.r
    @property
    def maximum_y(self):
        return self.y + self.r

    @property
    def minimum_x(self):
        return self.x - self.r
    @property
    def minimum_y(self):
        return self.y - self.r

    def __repr__(self):
        return f'<SensorPair x={self.x}, y={self.y}, r={self.r}>'


def load_sensors(data):
    sensors = []
    for text in data:
        _, _, s_coord_x, s_coord_y, _, _, _, _, b_coord_x, b_coord_y = text.split(' ')
        
        sensor = SensorPair(tuple(map(int, (s_coord_x.split('=',1)[1][:-1], s_coord_y.split('=',1)[1][:-1], b_coord_x.split('=',1)[1][:-1], b_coord_y.split('=',1)[1]))))
        sensors.append(sensor)
    
    return sensors



def simulate(data):
    sensors = load_sensors(data)
    no_beacons = 0

    y = 2_000_000
    x = None
    max_x = None

    for sensor in sensors[1:]:
        temp = sensor.min_x(y)
        if temp is not None:
            if x is None:
                x = temp
            else:
                x = min(temp, x-1)

        temp = sensor.max_x(y)
        if temp is not None:
            if max_x is None:
                max_x = temp
            else:
                max_x = max(temp, max_x+1)

    count = 0
    while x <= max_x:
        coord = (x, y)

        for i, sensor in enumerate(sensors):
            if sensor.in_range(coord):
                new_x = sensor.max_x(coord[1])
                if coord[1] == sensor.by:
                    no_beacons -= 1
                
                no_beacons += new_x - x + 1
                
                x = new_x

                break

        #print(done)
        if count % 10000 == 0:
            print(count, x, max_x, no_beacons)

        x += 1
        count += 1
    
    print(count)
    
    count = 0
    done = None
    for y in range(4_000_000):
        if done is not None:
            break

        x = 0

        while x < 4_000_000:
            coord = (x, y)

            if count % 100_000 == 0:
                print(count, coord)
            
            count += 1

            for i, sensor in enumerate(sensors):
                if sensor.in_range(coord):
                    x = sensor.max_x(coord[1]) + 1
                    break
            else:
                done = coord
                break

    print(count)
    # code here
    return no_beacons, (done[0] * 4_000_000) + done[1]


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_015.txt')
    results = simulate(data)
    print(results[0], 5_688_618)
    print(results[1], 12_625_383_204_261)


if __name__ == '__main__':
    main()

