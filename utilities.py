import json
import csv
import pathlib

"""
This utilities module provides a set of functions to handle common file operations and data manipulation tasks including:
- Path validation and directory creation
- JSON file reading and writing
- CSV file reading and writing with automatic delimiter sniffing
- Data cleaning for CSV contents
- Extracting a specific column from 2D data lists
"""


def validate_paths(list_of_paths):
    """
    Validates and ensures the existence of directories or files specified in the paths list.

    Args:
        list_of_paths (list or str): A list of path strings or a single path string.

    Ensures that each directory or the parent directory of each file in the list exists,
    creating them if necessary. Directories are directly checked, while files are checked
    based on their parent directories.
    """
    if not isinstance(list_of_paths, list):
        list_of_paths = [list_of_paths]

    for path_string in list_of_paths:
        path = pathlib.Path(path_string)
        if path.suffix == "":
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path, data, indent=4, sort_keys=True):
    """
    Writes a Python data structure to a JSON file.

    Args:
        path (str): The file path where the JSON data will be written.
        data (dict or list): The data to write to the JSON file.
        indent (int): The indentation level for pretty-printing the JSON file.
        sort_keys (bool): Whether to sort the dictionary keys.

    Writes the data to a JSON file at the specified path with optional sorting of keys
    and indentation for better readability.
    """
    with open(path, "w") as file:
        json.dump(data, file, indent=indent, sort_keys=sort_keys)


def read_json(path):
    """
    Reads a JSON file and returns the data.

    Args:
        path (str): The file path from which to read the JSON data.

    Returns:
        dict or list: The data loaded from the JSON file.
    """
    with open(path, mode="r") as file:
        return json.load(file)


def find_delimited_files(directory):
    """
    Retrieves all files from the specified directory that are likely to be readable
    by the read_delim_file function, which includes typical delimiter-separated values files.

    Args:
        directory (str): The path to the directory from which to retrieve the files.

    Returns:
        list of pathlib.Path: A list of paths to the files that match common delimited file extensions.
    """
    target_directory = pathlib.Path(directory)

    file_extensions = [".csv", ".tsv", ".txt"]

    compatible_files = [
        file for ext in file_extensions for file in target_directory.glob(f"*{ext}")
    ]

    return compatible_files


def read_delim_file(path):
    """
    Reads a delimited file and detects its dialect.

    Args:
        path (str): The path to the delimited file.

    Returns:
        tuple: A tuple containing a list of rows from the file and the detected CSV dialect.

    Automatically detects the delimiter of the file using csv.Sniffer and reads the file accordingly.
    """
    with open(path, newline="") as delim_file:
        dialect = csv.Sniffer().sniff(delim_file.read(2048))
        delim_file.seek(0)
        return list(csv.reader(delim_file, dialect)), dialect


def write_delim_file(path, data, delim):
    """
    Writes a list of lists (data) to a file using a specified delimiter.

    Args:
        path (str): The path where the file will be written.
        data (list of lists): The data to be written to the file.
        delim (str): The delimiter to use for separating entries in the file.

    Writes the data to the specified path using the provided delimiter, typically creating a CSV file.
    """
    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=delim)
        writer.writerows(data)


def clean_data(data):
    """
    Cleans a 2D list by removing extra spaces and stripping whitespace from each string.

    Args:
        data (list of lists): The data to clean.

    Returns:
        list of lists: The cleaned data.

    This function iterates through a 2D list and cleans each string by replacing double
    spaces with single spaces and stripping leading and trailing whitespace.
    """
    return [[item.replace("  ", " ").strip() for item in row] for row in data]


def get_column(two_dimensional_list, column_index):
    """
    Extracts a column from a 2D list.

    Args:
        two_dimensional_list (list of lists): The 2D list from which to extract the column.
        column_index (int): The index of the column to extract.

    Returns:
        list: A list containing the elements of the specified column.

    This function goes through each row of the 2D list and collects the elements
    at the specified column index into a new list.
    """
    return [row[column_index] for row in two_dimensional_list]
