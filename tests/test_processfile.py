import unittest
from utils.processfile import (
    process_follower_input_text,
    process_ref_text,
    process_score_text,
)


class TestProcessFollowerInputText(unittest.TestCase):
    def test_process_follower_input_text_ok(self):
        inp = "123.01 456 789 69\n123 456   789 69\n 1\t\t2\t\t3\t\t54\n"
        want = [
            {
                "est_time": 123.01,
                "det_time": 456,
                "note_start": 789,
                "midi_note_num": 69,
            },
            {
                "est_time": 123,
                "det_time": 456,
                "note_start": 789,
                "midi_note_num": 69,
            },
            {
                "est_time": 1,
                "det_time": 2,
                "note_start": 3,
                "midi_note_num": 54,
            },
        ]
        got = process_follower_input_text(inp)
        self.assertEqual(want, got)

    def test_process_follower_input_text_exception(self):
        cases = [
            "123",
            "abc def ghi",
            "123 456",
        ]

        for c in cases:
            with self.assertRaises(ValueError):
                process_follower_input_text(c)


class TestProcessRefText(unittest.TestCase):
    def test_process_ref_text_ok(self):
        inp = "123.01 456 69\n123 456   69\n 1\t\t2\t\t3\t\t54\n\t//lol\n// 123 123 123"
        want = [
            {
                "tru_time": 123.01,
                "note_start": float(456),
                "midi_note_num": 69,
            },
            {
                "tru_time": 123,
                "note_start": 456,
                "midi_note_num": 69,
            },
            {
                "tru_time": 1,
                "note_start": 2,
                "midi_note_num": 3,
            },
        ]
        got = process_ref_text(inp)
        self.assertEqual(want, got)

    def test_process_ref_text_exception(self):
        cases = [
            "123",
            "abc def ghi",
            "123 456",
        ]

        for c in cases:
            with self.assertRaises(ValueError):
                process_ref_text(c)


class TestProcessScoreFile(unittest.TestCase):
    def test_process_score_text_ok(self):
        inp = "123.01 456\n123 456   \n 1\t\t2\t\t3\t\t54\n"
        want = [
            {
                "note_start": 123.01,
                "midi_note_num": 456,
            },
            {
                "note_start": 123,
                "midi_note_num": 456,
            },
            {
                "note_start": 1,
                "midi_note_num": 2,
            },
        ]
        got = process_score_text(inp)
        self.assertEqual(want, got)

    def test_process_score_text_exception(self):
        cases = [
            "123",
            "abc def ghi",
            "123 456",
        ]

        for c in cases:
            with self.assertRaises(ValueError):
                process_ref_text(c)
