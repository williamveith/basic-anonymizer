import random
import string
import pathlib
import json
from rapidfuzz import process

"""
This module provides two main classes, TypedCipher and NameCipher, for encrypting text data.
TypedCipher handles general character-based encryption while NameCipher specializes in name encryption
using a fuzzy matching approach to replace names with pseudonyms or other names from predefined lists.
"""

class TypedCipher:
    """
    A cipher for encoding text using a random substitution cipher that maintains character types,
    such as upper/lowercase letters, digits, and punctuation.

    Attributes:
        _encoding (str): The character encoding used to verify if characters can be encoded.
        _cipher (dict): A dictionary mapping original characters to their cipher equivalents.
    """
    
    def __init__(self, encoding='utf-8'):
        """
        Initializes the TypedCipher with a specific encoding.

        Args:
            encoding (str): The text encoding format to use for character validation. Defaults to 'utf-8'.
        """
        self._encoding = encoding
        self._cipher = self.create_cipher(encoding)
        
    def create_cipher(self, encoding='utf-8'):
        """
        Generates a substitution cipher dictionary based on character categories including
        a comprehensive range of Unicode characters.

        Args:
            encoding (str): The text encoding format to use for character validation.

        Returns:
            dict: A dictionary mapping each character to a shuffled equivalent.
        """
        categories = {
            'uppercase': string.ascii_uppercase,
            'lowercase': string.ascii_lowercase,
            'digits': string.digits,
            'punctuation': string.punctuation,
            'others': []
        }

        cipher_dict = {}

        for category, chars in categories.items():
            if chars:
                shuffled_chars = list(chars)
                random.shuffle(shuffled_chars)
                cipher_dict.update(dict(zip(chars, shuffled_chars)))

        for code_point in range(0x80, 0x110000):
            char = chr(code_point)
            try:
                if char.encode(encoding):
                    categories['others'].append(char)
            except UnicodeEncodeError:
                continue

        if categories['others']:
            shuffled_others = list(categories['others'])
            random.shuffle(shuffled_others)
            cipher_dict.update(dict(zip(categories['others'], shuffled_others)))

        return cipher_dict
    
    def encode(self, string):
        """
        Encodes a string using the predefined substitution cipher.

        Args:
            string (str): The string to encode.

        Returns:
            str: The encoded string.
        """
        return ''.join(self._cipher.get(char, char) for char in string)

class NameCipher:
    """
    A cipher for encoding names using best-match replacement from a provided list of names,
    leveraging fuzzy matching to determine the closest matches and employing a predefined confidence
    threshold for match acceptance.

    Attributes:
        _match_confidence (float): The confidence threshold for accepting a name match.
        _first_names (list): A list of possible first names loaded from a JSON file.
        _last_names (list): A list of possible last names loaded from a JSON file.
        _cipher (dict): A dictionary mapping original names to their encoded counterparts.
    """
    root_path = pathlib.Path(__file__).resolve().parent
    first_name_dictionary_path = "dictionaries/first-names.json"
    last_name_dictionary_path = "dictionaries/last-names.json"
    
    def __init__(self, name_list, name_match_confidence=85.0):
        """
        Initializes the NameCipher with a list of names and a match confidence threshold.

        Args:
            name_list (list of str): The list of names to encode.
            name_match_confidence (float): The threshold confidence score for name matching. Defaults to 85.0.
        """
        self._match_confidence = name_match_confidence
        self._first_names = self.read_json(NameCipher.first_name_dictionary_path)
        self._last_names = self.read_json(NameCipher.last_name_dictionary_path)
        self._cipher = self.create_cipher(name_list)
    
    def read_json(self, path):
        """
        Reads a JSON file from the given path and returns its content.

        Args:
            path (str): The file path to read the JSON data from.

        Returns:
            dict: The content of the JSON file.
        """
        with open(path, mode="r") as file:
            return json.load(file)
    
    def create_cipher(self, name_list):
        """
        Creates a name cipher by performing fuzzy matches against a dynamic list of names,
        adding unmatched or insufficiently matched names as new entries.

        Args:
            name_list (list of str): The list of names to process for cipher creation.

        Returns:
            dict: A dictionary mapping original names to their replacements.
        """
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
                
    def encode(self, name):
        """
        Encodes a given name using the cipher, or generates a new pseudonym if no suitable match is found.

        Args:
            name (str): The name to encode.

        Returns:
            str: The encoded or newly generated name.
        """
        encoded_name = self._cipher.get(name.lower(), None)
        if encoded_name is None:
            encoded_name = self.append(self, name)
        
        return encoded_name
    
    def append(self, new_name):
        """
        Appends a new name to the cipher dictionary, ensuring uniqueness.

        Args:
            new_name (str): The name to append.

        Returns:
            str: The encoded or original name, depending on existence in the cipher.
        """
        if self._cipher.get(new_name, None) is not None:
            print(f"{new_name} already exists.")
            return new_name
        
        encoded_name = self.random_name
        self._cipher[new_name] = encoded_name
        return encoded_name
    
    @property 
    def random_name(self):
        """
        Generates a random name by combining a random first name and a last name.

        Returns:
            str: A randomly generated name.
        """
        return f"{random.choice(self._first_names)} {random.choice(self._last_names)}"