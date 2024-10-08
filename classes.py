import secrets
import random
import string
import pathlib
import json
from typing import Dict, List, Optional
from rapidfuzz import process


class TypedCipher:
    def __init__(self, encoding: str = "utf-8") -> None:
        self._encoding = encoding
        self._cipher = self.create_cipher(encoding)

    def create_cipher(self, encoding: str = "utf-8") -> Dict[str, str]:
        categories = {
            "uppercase": string.ascii_uppercase,
            "lowercase": string.ascii_lowercase,
            "digits": string.digits,
            "punctuation": string.punctuation,
            "others": [],
        }

        cipher_dict = {}

        for chars in categories.values():
            if chars:
                shuffled_chars = list(chars)
                random.shuffle(shuffled_chars)
                cipher_dict.update(dict(zip(chars, shuffled_chars)))

        for code_point in range(0x80, 0x110000):
            char = chr(code_point)
            try:
                if char.encode(encoding):
                    categories["others"].append(char)
            except UnicodeEncodeError:
                continue

        if categories["others"]:
            shuffled_others = list(categories["others"])
            random.shuffle(shuffled_others)
            cipher_dict.update(dict(zip(categories["others"], shuffled_others)))

        return cipher_dict

    def encode(self, string: str) -> str:
        return "".join(self._cipher.get(char, char) for char in string)


class NameCipher:
    root_path = pathlib.Path(__file__).resolve().parent
    first_name_dictionary_path = "dictionaries/first-names.json"
    last_name_dictionary_path = "dictionaries/last-names.json"

    def __init__(
        self, name_list: List[str], name_match_confidence: float = 85.0
    ) -> None:
        self._match_confidence = name_match_confidence
        self._first_names = self.read_json(NameCipher.first_name_dictionary_path)
        self._last_names = self.read_json(NameCipher.last_name_dictionary_path)
        self._cipher = self.create_cipher(name_list)

    def read_json(self, path: str) -> List[str]:
        with open(path, mode="r") as file:
            return json.load(file)

    def write_json(
        self,
        path: str,
        data: List[str],
        indent: Optional[int] = None,
        sort_keys: bool = True,
    ) -> None:
        with open(path, "w") as file:
            json.dump(data, file, indent=indent, sort_keys=sort_keys)

    def create_cipher(self, name_list: List[str]) -> Dict[str, Optional[str]]:
        name_cipher = {}
        added_names = []
        for name in name_list:
            best_match = process.extractOne(name.lower(), added_names)
            if best_match is None:
                best_match = (name, 0.0, 0)

            if best_match[1] == 100.0:
                continue
            elif best_match[1] >= self._match_confidence and best_match[1] < 100.0:
                name_cipher[name.lower()] = name_cipher.get(best_match[0], None)
            else:
                name_cipher[name.lower()] = self.random_name
                added_names.append(name.lower())

        return name_cipher

    def encode(self, name: str) -> str:
        encoded_name = self._cipher.get(name.lower(), None)
        if encoded_name is None:
            encoded_name = self.append(name)

        return encoded_name

    def append(self, new_name: str) -> str:
        if self._cipher.get(new_name, None) is not None:
            print(f"{new_name} already exists.")
            return new_name

        encoded_name = self.random_name
        self._cipher[new_name] = encoded_name
        return encoded_name

    @property
    def random_name(self) -> str:
        return f"{secrets.choice(self._first_names)} {secrets.choice(self._last_names)}"


class RedactCipher:
    def __init__(self, redaction_reason: str = "Sensitive Info") -> None:
        self._reason = redaction_reason

    def encode(self, current_value: Optional[str] = None) -> str:
        return self._reason
