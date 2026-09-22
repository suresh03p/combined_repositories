import json
from collections import Counter
from pathlib import Path


def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    root = Path(__file__).resolve().parents[1]
    train_path = root / 'data' / 'train.jsonl'
    records = load_jsonl(train_path)

    labels = [record['output'] for record in records]
    counts = Counter(labels)

    print('Category counts:')
    for category, count in sorted(counts.items()):
        print(f'  {category}: {count}')

    max_count = max(counts.values())
    min_count = min(counts.values())
    print(f'\nMax count: {max_count}')
    print(f'Min count: {min_count}')

    if max_count / min_count > 2:
        print('\nWarning: severe class imbalance detected. The highest-frequency class is more than 2x the lowest-frequency class.')
    else:
        print('\nClass distribution is relatively balanced for this small task.')

    underrepresented = [cat for cat, count in counts.items() if count < 0.8 * max_count]
    if underrepresented:
        print('Underrepresented categories: ' + ', '.join(sorted(underrepresented)))


if __name__ == '__main__':
    main()
