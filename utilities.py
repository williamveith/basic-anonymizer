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


def find_delimited_files(directory):
    file_extensions = [".csv", ".tsv", ".txt"]

    compatible_files = [
        file for ext in file_extensions for file in directory.glob(f"*{ext}")
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
