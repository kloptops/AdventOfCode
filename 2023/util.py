
from pathlib import Path


DATA_PATH = Path('data/')

def load_data(file_name):
    with open(DATA_PATH / file_name, 'r') as fh:
        yield from fh


__all__ = (
    'DATA_PATH',
    'load_data',
    )
