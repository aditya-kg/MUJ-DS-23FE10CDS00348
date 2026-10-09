"""Score labels and human-reviewed expansion quality on held-out conversations."""

import argparse
import json
from pathlib import Path


def load_jsonl(path: Path):
    with path.open(encoding="utf-8") as source:
        return [json.loads(line) for line in source if line.strip()]


def macro_f1(gold, predicted):
    labels = set(gold) | set(predicted)
    scores = []
    for label in labels:
        tp = sum(g == label and p == label for g, p in zip(gold, predicted))
        fp = sum(g != label and p == label for g, p in zip(gold, predicted))
        fn = sum(g == label and p != label for g, p in zip(gold, predicted))
        denom = 2 * tp + fp + fn
        scores.append((2 * tp / denom) if denom else 0.0)
    return sum(scores) / len(scores) if scores else 0.0


def binary_metrics(gold, predicted):
    tp = sum(g and p for g, p in zip(gold, predicted))
    fp = sum((not g) and p for g, p in zip(gold, predicted))
    fn = sum(g and (not p) for g, p in zip(gold, predicted))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def score(gold_records, prediction_records):
    gold_by_id = {record["conversation_id"]: record for record in gold_records}
    pred_by_id = {record["conversation_id"]: record for record in prediction_records}
    if len(gold_by_id) != len(gold_records) or len(pred_by_id) != len(prediction_records):
        raise ValueError("conversation_id values must be unique in both files")
    if set(gold_by_id) != set(pred_by_id):
        raise ValueError("Gold and prediction files must contain the same held-out conversation IDs")

    gold_l1, pred_l1, gold_l2, pred_l2 = [], [], [], []
    gold_ambiguous, pred_ambiguous = [], []
    intent_reviews, unsupported_reviews = [], []
    evaluated = 0

    for conversation_id, gold_record in gold_by_id.items():
        pred_record = pred_by_id[conversation_id]
        gold_messages = {m["message_id"]: m for m in gold_record["messages"] if m.get("role") == "user" and m.get("gold")}
        pred_messages = {m["message_id"]: m for m in pred_record["messages"] if m.get("role") == "user" and m.get("prediction")}
        if set(gold_messages) != set(pred_messages):
            raise ValueError(f"User message IDs differ for conversation {conversation_id!r}")
        for message_id, gold_message in gold_messages.items():
            gold = gold_message["gold"]
            pred = pred_messages[message_id]["prediction"]
            gold_l1.append(gold["topic_l1"])
            pred_l1.append(pred["topic_l1"])
            gold_l2.append(gold["topic_l2"])
            pred_l2.append(pred["topic_l2"])
            gold_ambiguous.append(bool(gold["needs_clarification"]))
            pred_ambiguous.append(bool(pred["needs_clarification"]))
            if pred.get("intent_preserved") is not None:
                intent_reviews.append(bool(pred["intent_preserved"]))
            if pred.get("unsupported_details") is not None:
                unsupported_reviews.append(bool(pred["unsupported_details"]))
            evaluated += 1

    accuracy = lambda gold, predicted: sum(g == p for g, p in zip(gold, predicted)) / len(gold) if gold else 0.0
    result = {
        "conversations": len(gold_records),
        "user_turns": evaluated,
        "l1_accuracy": accuracy(gold_l1, pred_l1),
        "l1_macro_f1": macro_f1(gold_l1, pred_l1),
        "l2_accuracy": accuracy(gold_l2, pred_l2),
        "l2_macro_f1": macro_f1(gold_l2, pred_l2),
        "clarification": binary_metrics(gold_ambiguous, pred_ambiguous),
        "reviewed_expansions": len(intent_reviews),
        "intent_preserved_rate": sum(intent_reviews) / len(intent_reviews) if intent_reviews else None,
        "unsupported_detail_rate": sum(unsupported_reviews) / len(unsupported_reviews) if unsupported_reviews else None,
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", required=True, type=Path)
    parser.add_argument("--predictions", required=True, type=Path)
    args = parser.parse_args()
    metrics = score(load_jsonl(args.gold), load_jsonl(args.predictions))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
