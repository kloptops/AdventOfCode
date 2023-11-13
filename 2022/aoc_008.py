def before(data, x, y):
    return data[y][:x][::-1]


def after(data, x, y):
    return data[y][x+1:]


def above(data, x, y):
    return [
        line[x]
        for line in data[:y]][::-1]


def below(data, x, y):
    return [
        line[x]
        for line in data[y+1:]]


def is_tallest(cell, data):
    for x in data:
        if x >= cell:
            return False
    return True


def longest_view(cell, data):
    for i, x in enumerate(data, 1):
        if x >= cell:
            return i
    return len(data)


def simulate(data):
    grid = []
    
    for line in data:
        line = line.strip()
        grid.append(list(map(int, line)))

    height = len(grid)
    width = len(grid[0])
    
    total_trees = width + width
    best_view = 0

    for y in range(1, height-1):
        total_trees += 2
        for x in range(1, width - 1):
            cell = grid[y][x]
            if cell == 0:
                continue
            
            # calculate view score for part 2
            view_score = (
                longest_view(cell, above(grid, x, y)) *
                longest_view(cell, below(grid, x, y)) *
                longest_view(cell, before(grid, x, y)) *
                longest_view(cell, after(grid, x, y)))
    
            if view_score > best_view:
                best_view = view_score
            
            # calculate if tallest for part 1
            if is_tallest(cell, above(grid, x, y)):
                total_trees += 1
                continue
    
            if is_tallest(cell, below(grid, x, y)):
                total_trees += 1
                continue
    
            if is_tallest(cell, before(grid, x, y)):
                total_trees += 1
                continue
    
            if is_tallest(cell, after(grid, x, y)):
                total_trees += 1
                continue
    
    return total_trees, best_view


def get_data(file_name):
    data = []
    with open(file_name, 'rt') as fh:
        for line in fh:
            data.append(line.strip())
    
    return data


def main():
    data = get_data('data/input_008.txt')
    result = simulate(data)
    print(result[0], 1733)
    print(result[1], 284648)

if __name__ == '__main__':
    main()


