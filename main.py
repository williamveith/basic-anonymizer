from utilities import read_delim_file, write_delim_file, clean_data, get_column, validate_paths
from classes import TypedCipher, NameCipher
import pathlib

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
    confidential_path = pathlib.Path(CONFIDENTIAL_PATH)
    anonymous_path = pathlib.Path(ANONYMIZED_PATH)
    
    data, dialect = read_delim_file(confidential_path / PROCESS_FILE)
    data = clean_data(data)
    headers = data.pop(0)
    
    data_anonymized = anonymize_data(data, ANONYMIZE_CONFIGS)
                    
    data.insert(0, headers)
    write_delim_file(anonymous_path / PROCESS_FILE, data_anonymized, dialect.delimiter)
