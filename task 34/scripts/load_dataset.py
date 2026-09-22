import json
from pathlib import Path


def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def validate_record(record):
    required = {'instruction', 'input', 'output'}
    missing = required - set(record.keys())
    if missing:
        raise ValueError(f"Missing keys: {sorted(missing)} in record: {record}")
    if not isinstance(record['instruction'], str) or not record['instruction'].strip():
        raise ValueError(f"Invalid instruction field: {record}")
    if not isinstance(record['input'], str) or not record['input'].strip():
        raise ValueError(f"Invalid input field: {record}")
    if not isinstance(record['output'], str) or not record['output'].strip():
        raise ValueError(f"Invalid output field: {record}")


def main():
    root = Path(__file__).resolve().parents[1]
    data_dir = root / 'data'

    train_path = data_dir / 'train.jsonl'
    validation_path = data_dir / 'validation.jsonl'

    train_records = load_jsonl(train_path)
    validation_records = load_jsonl(validation_path)

    for record in train_records + validation_records:
        validate_record(record)

    print(f"Training samples: {len(train_records)}")
    print(f"Validation samples: {len(validation_records)}")
    print("Sample training record:")
    print(json.dumps(train_records[0], ensure_ascii=False, indent=2))
    print("Sample validation record:")
    print(json.dumps(validation_records[0], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
