"""Download a small, local-only Topical-Chat conversation sample for annotation.

The script downloads the official test_freq split in memory and writes only the
requested number of complete conversations under evaluation/local_data/. That
directory is ignored by Git; raw conversation text should not be committed.
"""

from __future__ import annotations

import argparse
import json
import random
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "local_data"
SOURCE_URL = (
    "https://raw.githubusercontent.com/alexa/Topical-Chat/master/"
    "conversations/test_freq.json"
)
SOURCE_REPO = "https://github.com/alexa/Topical-Chat"
LICENSE_URL = "https://github.com/alexa/Topical-Chat/blob/master/DATALICENSE"


def fetch_conversations() -> dict[str, Any]:
    request = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "MUJ-NLP-annotation-sample/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise ValueError("Expected Topical-Chat split JSON to contain an object.")
    return payload


def make_preview(limit: int, seed: int) -> dict[str, Any]:
    source = fetch_conversations()
    ids = sorted(source)
    random.Random(seed).shuffle(ids)
    chosen_ids = ids[: min(limit, len(ids))]

    records = []
    for conversation_id in chosen_ids:
        raw = source[conversation_id]
        content = raw.get("content", [])
        turns = [
            {
                "turn_index": index,
                "speaker": turn.get("agent", ""),
                "text": turn.get("message", ""),
                # These are source annotations, not our expansion/topic labels.
                "source_sentiment": turn.get("sentiment"),
                "source_turn_rating": turn.get("turn_rating"),
            }
            for index, turn in enumerate(content)
            if isinstance(turn, dict) and isinstance(turn.get("message"), str)
        ]
        records.append(
            {
                "conversation_id": conversation_id,
                "source_split": "test_freq",
                "turns": turns,
                "annotation_tasks": [
                    {
                        "target_turn_index": turn["turn_index"],
                        "standalone_rewrite": None,
                        "preserves_user_intent": None,
                        "adds_unsupported_details": None,
                        "ambiguous_or_unresolvable": None,
                        "topic_l1": None,
                        "topic_l2": None,
                        "annotator_notes": None,
                    }
                    for turn in turns[1:]
                ],
            }
        )

    return {
        "dataset": "Topical-Chat",
        "source_repository": SOURCE_REPO,
        "source_file": SOURCE_URL,
        "source_license": "Community Data License Agreement - Sharing, Version 1.0",
        "source_license_url": LICENSE_URL,
        "source_split": "test_freq",
        "sample_seed": seed,
        "sampled_conversation_count": len(records),
        "prepared_at_utc": datetime.now(timezone.utc).isoformat(),
        "annotation_note": (
            "Blank fields are for manual annotation. Source sentiment and turn "
            "ratings are retained separately and are not project gold labels."
        ),
        "conversations": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=8, help="Complete conversations to sample")
    parser.add_argument("--seed", type=int, default=230348, help="Deterministic sample seed")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUT_DIR / "topicalchat_preview.json"
    output.write_text(
        json.dumps(make_preview(args.limit, args.seed), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {output}; this file is ignored by Git and stays local.")


if __name__ == "__main__":
    main()
