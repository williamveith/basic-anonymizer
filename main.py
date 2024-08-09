from configs import PATHS, ANONYMIZE_CONFIGS
from utilities import read_delim_file, write_delim_file, clean_data, get_column, validate_paths, find_delimited_files
from classes import TypedCipher, NameCipher
import pathlib

"""
This module handles the anonymization of sensitive data by applying various cipher methods
to specified columns of a CSV file. The file paths are validated, and the anonymized data is
saved to a specified output directory.

Uses:
- `TypedCipher` for general purpose data encryption.
- `NameCipher` specifically for encrypting names with a confidence threshold.
- Redaction for columns where data cannot be anonymized.

The configurations for anonymization are specified in `ANONYMIZE_CONFIGS`.
"""

validate_paths(list(PATHS.values()))

def anonymize_data(data, anon_configs):
    """
    Anonymizes specific columns of data based on the provided configurations.

    Args:
        data (list of list of str): The 2D list of data (table) to be anonymized.
        anon_configs (list of dicts): Configuration list where each dictionary specifies
                                        the column index and the type of anonymization or redaction.

    Returns:
        list of list of str: The anonymized data as a 2D list.

    Processes each column specified in `anon_configs` using the specified anonymization
    type, which could be `TypedCipher`, `NameCipher`, or redaction.
    """
    for column in anon_configs:
        match column["type"]:
            case "TypedCipher":
                cipher = TypedCipher()
                for row_number, row in enumerate(data):
                    encoded_value = cipher.encode(row[column["index"]])
                    data[row_number][column["index"]] = encoded_value
            case "NameCipher":
                names = get_column(data, column["index"])
                cipher = NameCipher(
                    names,
                    name_match_confidence=column["options"]["name_match_confidence"],
                )
                for row_number, row in enumerate(data):
                    encoded_value = cipher.encode(row[column["index"]])
                    data[row_number][column["index"]] = encoded_value
            case _:
                encoded_value = column["options"]["reason"]
                for row_number, row in enumerate(data):
                    data[row_number][column["index"]] = encoded_value
                    
    return data
    
if __name__ == "__main__":
    """
    Main execution path for the script:
    - Validates paths for input and output.
    - Reads a delimited file containing purchasing records.
    - Cleans the data by stripping and replacing excessive whitespace.
    - Anonymizes the data based on predefined configurations.
    - Writes the anonymized data back to a file in the specified output directory.
    """
    confidential_path = pathlib.Path(PATHS.get("confidential", None))
    anonymous_path = pathlib.Path(PATHS.get("anonymized", None))
    
    for file_path in find_delimited_files(confidential_path):
        data, dialect = read_delim_file(file_path)
        data = clean_data(data)
        headers = data.pop(0)
        
        data_anonymized = anonymize_data(data, ANONYMIZE_CONFIGS)
        data_anonymized.insert(0, headers)
        
        anonymized_record_path =  anonymous_path / file_path.name
        write_delim_file(anonymized_record_path, data_anonymized, dialect.delimiter)
