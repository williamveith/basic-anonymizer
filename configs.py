from dataclasses import dataclass, field
from typing import List
import pathlib


@dataclass
class AnonymizationOption:
    """Represents additional options for anonymization types."""

    reason: str = ""
    name_match_confidence: float = 0.0


@dataclass
class AnonymizationConfig:
    """
    Defines a single column's anonymization strategy.

    Attributes:
        index (int): Column index in the dataset to be anonymized.
        type (str): Type of anonymization ('TypedCipher', 'RedactCipher', 'NameCipher').
        options (AnonymizationOption): Detailed options for the anonymization process.
    """

    index: int
    type: str
    options: AnonymizationOption = field(default_factory=AnonymizationOption)


@dataclass
class AnonymizerSettings:
    """
    Stores all configurations for the anonymization process.

    Attributes:
        configs (List[AnonymizationConfig]): A list of anonymization configurations.
    """

    configs: List[AnonymizationConfig]


@dataclass
class PathConfig:
    """
    Represents the configuration for a single file system path within the project.

    Attributes:
        name (str): A unique identifier for the path configuration.
        path (pathlib.Path): The file system path object, which may represent a directory or a file.

    The `__post_init__` method automatically ensures that the directory exists, or if the path points to a file,
    ensures that the file's parent directory exists. This automatic setup occurs immediately upon object instantiation.
    """

    name: str
    path: pathlib.Path

    def __post_init__(self):
        if not self.path.exists():
            self.path.mkdir(parents=True, exist_ok=True)
        elif self.path.is_file():
            self.path.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class PathSettings:
    """
    Manages a collection of PathConfig objects, providing structured access to multiple file system paths.

    Attributes:
        path_configs (List[PathConfig]): A list of PathConfig objects that represent different paths.

    The `__post_init__` method sets up each path as an attribute of the instance, enabling attribute-style access
    to each path based on its name. This setup occurs immediately upon object instantiation.
    """

    path_configs: List[PathConfig] = field(default_factory=list)

    def __post_init__(self):
        for path_config in self.path_configs:
            setattr(self, path_config.name, path_config.path)
