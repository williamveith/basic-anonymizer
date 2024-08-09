# Basic Anonymizer

The Basic Anonymizer project provides tools for anonymizing sensitive data in structured formats (CSV and JSON), focusing on names and other personally identifiable information (PII). This utility is ideal for preparing data for public datasets or anonymized analysis.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)

## Features

- **Data Encryption**: Utilize `TypedCipher` for general text encryption and `NameCipher` for specific name anonymization.
- **File Operations**: Easy reading and writing for JSON and CSV files.
- **Data Cleaning**: Automatically clean data from CSV files, including removing excess whitespace and normalizing text format.
- **Directory Validation**: Automatically create and verify required directories and paths.

## Getting Started

### Prerequisites

- Python 3.8 or newer
- `rapidfuzz` library

### Installation

Clone the repository using git:

```bash
git clone https://github.com/williamveith/basic-anonymizer.git
cd basic-anonymizer
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Usage

Here is how you can use the Basic Anonymizer to anonymize a dataset:

1. **Prepare your CSV or JSON data file.**
2. **Define your anonymization rules in the configuration.**
3. **Run the anonymization script.**

Example of running the script:

```python
python anonymize.py
```

### Configuration

Edit the `ANONYMIZE_CONFIGS` in `anonymize.py` to define which columns should be anonymized and specify the type of anonymization:

```python
ANONYMIZE_CONFIGS = [
    {"index": 0, "type": "TypedCipher"},
    {"index": 5, "type": "Redact", "options": {"reason": "Redacted for privacy"}},
    {"index": 6, "type": "NameCipher", "options": {"name_match_confidence": 85.0}},
]
```
