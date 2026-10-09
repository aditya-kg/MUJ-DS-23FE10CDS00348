"""Create development and held-out sets without splitting conversations."""

import argparse
import json
import math
import random
from pathlib import Path


def load_conversations(path: Path):
    records = []
    seen = set()
    with path.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            conversation_id = record.get("conversation_id")
            if not conversation_id:
                raise ValueError(f"Line {line_number}: missing conversation_id")
            if conversation_id in seen:
                raise ValueError(f"Line {line_number}: duplicate conversation_id {conversation_id!r}")
            if not isinstance(record.get("messages"), list):
                raise ValueError(f"Line {line_number}: messages must be a list")
            seen.add(conversation_id)
            records.append(record)
    if len(records) < 2:
        raise ValueError("At least two complete conversations are required for a held-out split")
    return records


def split_conversations(records, test_fraction=0.2, seed=42):
    if not 0 < test_fraction < 1:
        raise ValueError("test_fraction must be between 0 and 1")
    shuffled = list(records)
    random.Random(seed).shuffle(shuffled)
    test_count = min(len(shuffled) - 1, max(1, math.ceil(len(shuffled) * test_fraction)))
    held_out = shuffled[:test_count]
    development = shuffled[test_count:]
    return development, held_out


def write_jsonl(path: Path, records):
    with path.open("w", encoding="utf-8", newline="\n") as output:
        for record in records:
            output.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--test-fraction", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    records = load_conversations(args.input)
    development, held_out = split_conversations(records, args.test_fraction, args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "development.jsonl", development)
    write_jsonl(args.output_dir / "held_out_test.jsonl", held_out)
    print(f"Development conversations: {len(development)}")
    print(f"Held-out conversations: {len(held_out)}")


if __name__ == "__main__":
    main()
