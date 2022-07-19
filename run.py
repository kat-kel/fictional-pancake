import argparse, os

from src.segment import Text
from src.lemmatize import execute_lemmatize


def get_args():
    parser = argparse.ArgumentParser()
    # Required positional argument that points to the directory containing TEI-XML files
    parser.add_argument("data", help="path to data", type=dir_path)
    args = parser.parse_args()
    return args.data

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError

if __name__ == "__main__":
    data = get_args()
    with os.scandir(data) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.xml'):
                segments = Text(entry).segments
                execute_lemmatize(segments)

                