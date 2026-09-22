import json
from pathlib import Path


def format_record(record):
    text = (
        "### Instruction\n"
        f"{record['instruction']}\n\n"
        "### Input\n"
        f"{record['input']}\n\n"
        "### Response\n"
        f"{record['output']}"
    )
    return text


def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    root = Path(__file__).resolve().parents[1]
    for split in ['train', 'validation', 'test']:
        in_path = root / 'data' / f'{split}.jsonl'
        out_path = root / 'data' / f'{split}_formatted.txt'
        records = load_jsonl(in_path)
        with open(out_path, 'w', encoding='utf-8') as f:
            for rec in records:
                f.write(format_record(rec) + '\n\n')
        print(f"Formatted {split}: {len(records)} records -> {out_path.name}")

    sample = load_jsonl(root / 'data' / 'train.jsonl')[0]
    print('\nSample formatted prompt:')
    print(format_record(sample))


if __name__ == '__main__':
    main()
