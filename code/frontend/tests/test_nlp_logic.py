import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nlp_logic import is_interruption, parse_expansion_decision, select_consistent_l2


class InterruptionTests(unittest.TestCase):
    def test_known_fillers_are_interruptions(self):
        for message in ("brb", "wait a sec", "Okay!", "thank you"):
            with self.subTest(message=message):
                self.assertTrue(is_interruption(message))

    def test_short_queries_are_not_interruptions(self):
        for message in ("Explain quantum physics", "New topic", "Compare both", "Who won?", "AI safety"):
            with self.subTest(message=message):
                self.assertFalse(is_interruption(message))


class ExpansionDecisionTests(unittest.TestCase):
    def test_ready_expansion_is_parsed(self):
        decision = parse_expansion_decision(
            '{"status":"ready","expanded_query":"What are the duties of India’s prime minister?",'
            '"intent_preserved":true,"unsupported_details":false}',
            "What are his duties?",
        )
        self.assertEqual(decision.expanded_query, "What are the duties of India’s prime minister?")
        self.assertFalse(decision.needs_clarification)

    def test_ambiguous_message_requests_clarification(self):
        decision = parse_expansion_decision(
            '{"status":"needs_clarification","clarification_question":"Which person do you mean?"}',
            "What did he do?",
        )
        self.assertTrue(decision.needs_clarification)
        self.assertEqual(decision.expanded_query, "What did he do?")
        self.assertEqual(decision.clarification_question, "Which person do you mean?")

    def test_malformed_model_output_fails_safe(self):
        decision = parse_expansion_decision("not json", "What about it?")
        self.assertTrue(decision.needs_clarification)
        self.assertEqual(decision.expanded_query, "What about it?")

    def test_failed_faithfulness_check_requests_clarification(self):
        decision = parse_expansion_decision(
            '{"status":"ready","expanded_query":"He became prime minister in 2014",'
            '"intent_preserved":false,"unsupported_details":true}',
            "What are his duties?",
        )
        self.assertTrue(decision.needs_clarification)
        self.assertEqual(decision.expanded_query, "What are his duties?")


class TopicHierarchyTests(unittest.TestCase):
    def test_selects_best_l2_valid_for_predicted_l1(self):
        label, score = select_consistent_l2(
            "Sports",
            [
                {"label": "India", "score": 0.98},
                {"label": "Cricket", "score": 0.75},
                {"label": "Football", "score": 0.89},
            ],
        )
        self.assertEqual(label, "Football")
        self.assertEqual(score, 0.89)

    def test_unexpected_l2_output_uses_valid_zero_score_fallback(self):
        label, score = select_consistent_l2("Politics", [{"label": "Cricket", "score": 0.99}])
        self.assertEqual(label, "India")
        self.assertEqual(score, 0.0)


if __name__ == "__main__":
    unittest.main()
