from utilities import read_delim_file, write_delim_file, clean_data, get_column, validate_paths
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

CONFIDENTIAL_PATH = "confidential"
ANONYMIZED_PATH = "anonymized"

PROCESS_FILE = "purchasing_records.csv"
ANONYMIZE_CONFIGS = [
    {"index": 0, "type": "TypedCipher"},
    {
        "index": 5,
        "type": "Redact",
        "options": {
            "reason": "This information was redacted because the information was not easily anonymizable"
        },
    },
    {"index": 6, "type": "NameCipher", "options": {"name_match_confidence": 85.0}},
    {"index": 7, "type": "NameCipher", "options": {"name_match_confidence": 85.0}},
    {"index": 8, "type": "TypedCipher"},
    {"index": 9, "type": "TypedCipher"},
]

validate_paths([CONFIDENTIAL_PATH, ANONYMIZED_PATH])

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
    confidential_path = pathlib.Path(CONFIDENTIAL_PATH)
    anonymous_path = pathlib.Path(ANONYMIZED_PATH)
    
    data, dialect = read_delim_file(confidential_path / PROCESS_FILE)
    data = clean_data(data)
    headers = data.pop(0)
    
    data_anonymized = anonymize_data(data, ANONYMIZE_CONFIGS)
                    
    data.insert(0, headers)
    write_delim_file(anonymous_path / PROCESS_FILE, data_anonymized, dialect.delimiter)
