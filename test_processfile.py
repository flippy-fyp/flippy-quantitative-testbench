import unittest
from processfile import process_text


class TestProcessText(unittest.TestCase):
    def test_process_text_ok(self):
        inp = "123 456 789\n123 456   789 \n 1\t\t2\t\t3\t\t54\n"
        want = [
            {
                "est_time": 123,
                "det_time": 456,
                "note_start": 789,
            },
            {
                "est_time": 123,
                "det_time": 456,
                "note_start": 789,
            },
            {
                "est_time": 1,
                "det_time": 2,
                "note_start": 3,
            },
        ]   
        got = process_text(inp)
        self.assertEqual(want, got)

    def test_process_text_exception(self):
        cases = [
            "123",
            "abc def ghi",
            "123 456",
        ]

        for c in cases:
            with self.assertRaises(ValueError):
                process_text(c)
