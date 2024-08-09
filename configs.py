PATHS = {
    "confidential": "confidential",
    "anonymized": "anonymized",
    "purchasing-record": "confidential/purchasing_records.csv"
}

ANONYMIZE_CONFIGS = [
    {
        "index": 0,
        "type": "TypedCipher"
    },
    {
        "index": 5,
        "type": "Redact",
        "options": {
            "reason": "This information was redacted because the information was not easily to anonymize"
        },
    },
    {
        "index": 6,
        "type": "NameCipher",
        "options": {
            "name_match_confidence": 85.0
        }
    },
    {
        "index": 7,
        "type": "NameCipher",
        "options": {
            "name_match_confidence": 85.0
        }
    },
    {
        "index": 8,
        "type": "TypedCipher"
    },
    {
        "index": 9,
        "type": "TypedCipher"
    },
]
