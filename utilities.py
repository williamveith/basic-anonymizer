import json
import csv
import pathlib

def validate_paths(list_of_paths):
    if not isinstance(list_of_paths, list):
        list_of_paths = [list_of_paths]

    for path_string in list_of_paths:
        path = pathlib.Path(path_string)
        if path.suffix == "":
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            
def write_json(path, data, indent=4, sort_keys=True):
    with open(path, "w") as file:
        json.dump(data, file, indent=indent, sort_keys=sort_keys)


def read_json(path):
    with open(path, mode="r") as file:
        return json.load(file)


def read_delim_file(path):
    with open(path, newline="") as delim_file:
        dialect = csv.Sniffer().sniff(delim_file.read(2048))
        delim_file.seek(0)
        return list(csv.reader(delim_file, dialect)), dialect


def write_delim_file(path, data, delim):
    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=delim)
        writer.writerows(data)


def clean_data(data):
    return [[item.replace("  ", " ").strip() for item in row] for row in data]


def get_column(two_dimensional_list, column_index):
    return [row[column_index] for row in two_dimensional_list]