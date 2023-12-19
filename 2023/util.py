import json

from pathlib import Path


DATA_PATH = Path('data/')




NORTH = ( 0, -1)
EAST  = (+1,  0)
SOUTH = ( 0, +1)
WEST  = (-1,  0)

DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
REV_DIRECTIONS = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
    }


def adj_coord(coord, adj):
    return (coord[0] + adj[0], coord[1] + adj[1])


class SpatialMap():
    def __init__(self):
        self.cells = {}
        self.visited_cells = set()
        self.max_x = 0
        self.max_y = 0

    def valid_coord(self, coord):
        if not (0 <= coord[0] < self.max_x):
            return False

        if not (0 <= coord[1] < self.max_y):
            return False

        return True

    def set_cell(self, coord, value):
        if coord[0] >= self.max_x:
            self.max_x = coord[0] + 1

        if coord[1] >= self.max_y:
            self.max_y = coord[1] + 1

        self.cells[coord] = value

    def get_cell(self, coord, default=None):
        return self.cells.get(coord, default)

    def clear_cell(self, coord):
        if coord in cells:
            del self.cells[coord]

    def visit_cell(self, coord):
        self.visited_cells.add(coord)

    def clear_visited(self):
        self.visited_cells.clear()

    def iter_direction(self, coord, direction):
        while True:
            coord = adj_coord(coord, direction)

            if not self.valid_coord(coord):
                return

            yield coord


def save_cache(file_name, results):
    name = DATA_PATH / file_name

    with open(name, 'w') as fh:
        json.dump(results, fh, indent=4, sort_keys=True)


def load_cache(file_name):
    name = DATA_PATH / file_name
    if not name.is_file():
        return {}

    with open(name, 'r') as fh:
        return json.load(fh)


def load_data(file_name):
    with open(DATA_PATH / file_name, 'r') as fh:
        yield from fh


__all__ = (
    'DATA_PATH',
    'DIRECTIONS',
    'REV_DIRECTIONS',
    'NORTH',
    'EAST',
    'SOUTH',
    'WEST',
    'adj_coord',
    'load_cache',
    'load_data',
    'save_cache',
    'SpatialMap'
    )
