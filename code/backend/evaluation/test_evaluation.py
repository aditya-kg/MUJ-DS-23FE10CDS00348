import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_holdout import score
from split_conversations import split_conversations


class HumanEvaluationTests(unittest.TestCase):
    def test_split_keeps_whole_conversations_together(self):
        records = [
            {"conversation_id": f"c{i}", "messages": [{"message_id": "u1"}, {"message_id": "u2"}]}
            for i in range(10)
        ]
        development, held_out = split_conversations(records, test_fraction=0.2, seed=5)
        dev_ids = {record["conversation_id"] for record in development}
        test_ids = {record["conversation_id"] for record in held_out}
        self.assertEqual(len(test_ids), 2)
        self.assertFalse(dev_ids & test_ids)
        self.assertEqual(dev_ids | test_ids, {record["conversation_id"] for record in records})

    def test_scores_labels_and_human_review(self):
        gold = [{
            "conversation_id": "c1",
            "messages": [{
                "message_id": "u1", "role": "user",
                "gold": {"topic_l1": "Sports", "topic_l2": "Cricket", "needs_clarification": False},
            }],
        }]
        predictions = [{
            "conversation_id": "c1",
            "messages": [{
                "message_id": "u1", "role": "user",
                "prediction": {
                    "topic_l1": "Sports", "topic_l2": "Cricket", "needs_clarification": False,
                    "intent_preserved": True, "unsupported_details": False,
                },
            }],
        }]
        result = score(gold, predictions)
        self.assertEqual(result["l1_accuracy"], 1.0)
        self.assertEqual(result["l2_accuracy"], 1.0)
        self.assertEqual(result["clarification"]["f1"], 0.0)
        self.assertEqual(result["intent_preserved_rate"], 1.0)
        self.assertEqual(result["unsupported_detail_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
