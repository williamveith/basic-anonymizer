import pathlib
from typing import List, Tuple, Union

from utilities import (
    read_delim_file,
    write_delim_file,
    clean_data,
    get_column,
    find_delimited_files,
)
from classes import TypedCipher, NameCipher, RedactCipher
from configs import (
    AnonymizationConfig,
    AnonymizerSettings,
    AnonymizationOption,
    PathSettings,
    PathConfig,
)

path_settings = PathSettings(
    path_configs=[
        PathConfig(name="confidential", path=pathlib.Path("confidential")),
        PathConfig(name="anonymized", path=pathlib.Path("anonymized")),
    ]
)

anonymizer_settings = AnonymizerSettings(
    configs=[
        AnonymizationConfig(index=0, type="TypedCipher"),
        AnonymizationConfig(
            index=5,
            type="RedactCipher",
            options=AnonymizationOption(reason="Sensitive Info"),
        ),
        AnonymizationConfig(
            index=6,
            type="NameCipher",
            options=AnonymizationOption(name_match_confidence=85.0),
        ),
        AnonymizationConfig(
            index=7,
            type="NameCipher",
            options=AnonymizationOption(name_match_confidence=85.0),
        ),
        AnonymizationConfig(index=8, type="TypedCipher"),
        AnonymizationConfig(index=9, type="TypedCipher"),
    ]
)


def anonymize_data(
    data: List[List[Union[str, int, float]]],
    anon_configs: List[AnonymizationConfig]
) -> List[List[Union[str, int, float]]]:
    for column in anon_configs:
        match column.type:
            case "TypedCipher":
                cipher = TypedCipher()
            case "NameCipher":
                names = get_column(data, column.index)
                cipher = NameCipher(
                    names,
                    name_match_confidence=column.options.name_match_confidence,
                )
            case "RedactCipher":
                cipher = RedactCipher(column.options.reason)

        for row_number, row in enumerate(data):
            encoded_value = cipher.encode(row[column.index])
            data[row_number][column.index] = encoded_value
    return data


def preprocess_file_data(
    file_data: List[List[str]], headers: bool = True
) -> Tuple[List[str], List[List[str]]]:
    data = clean_data(file_data)
    headers = data.pop(0) if headers else []
    return headers, data


if __name__ == "__main__":

    for file_path in find_delimited_files(path_settings.confidential):
        file_data, dialect = read_delim_file(file_path)
        headers, data = preprocess_file_data(file_data)

        data_anonymized = anonymize_data(data, anonymizer_settings.configs)
        data_anonymized.insert(0, headers)

        anonymized_record_path = (
            path_settings.anonymized / f"anonymized - {file_path.name}"
        )
        write_delim_file(anonymized_record_path, data_anonymized, dialect.delimiter)
