import unittest
from utils.match import match, preprocess_ref, MatchResult
from utils.processfile import FollowerOutputLine, RefFileLine
from typing import List, Tuple, Dict, TypedDict


class MatchTestCase(TypedDict):
    name: str
    scofo_output: List[FollowerOutputLine]
    ref: List[RefFileLine]
    want: MatchResult


class TestMatch(unittest.TestCase):
    def test_match(self):
        self.maxDiff = None
        cases: List[MatchTestCase] = [
            {
                "name": "empty inputs",
                "scofo_output": [],
                "ref": [],
                "want": {
                    "miss_rate": 0.0,
                    "misalign_rate": 0.0,
                    "piece_completion": 0.0,
                    "std_of_error": 0.0,
                    "mean_absolute_error": 0.0,
                    "std_of_latency": 0.0,
                    "mean_latency": 0.0,
                    "std_of_offset": 0.0,
                    "mean_absolute_offset": 0.0,
                },
            },
            {
                "name": "empty scofo_output",
                "scofo_output": [],
                "ref": [
                    {
                        "tru_time": 1,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "tru_time": 3,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                ],
                "want": {
                    "miss_rate": 1.0,
                    "misalign_rate": 0.0,
                    "piece_completion": 0.0,
                    "std_of_error": 0.0,
                    "mean_absolute_error": 0.0,
                    "std_of_latency": 0.0,
                    "mean_latency": 0.0,
                    "std_of_offset": 0.0,
                    "mean_absolute_offset": 0.0,
                },
            },
            {
                "name": "empty ref",
                "scofo_output": [
                    {
                        "est_time": 12,
                        "det_time": 13,
                        "note_start": 14,
                        "midi_note_num": 42,
                    },
                    {
                        "est_time": 13,
                        "det_time": 14,
                        "note_start": 15,
                        "midi_note_num": 43,
                    },
                ],
                "ref": [],
                "want": {
                    "miss_rate": 0.0,
                    "misalign_rate": 0.0,
                    "piece_completion": 0.0,
                    "std_of_error": 0.0,
                    "mean_absolute_error": 0.0,
                    "std_of_latency": 0.0,
                    "mean_latency": 0.0,
                    "std_of_offset": 0.0,
                    "mean_absolute_offset": 0.0,
                },
            },
            {
                "name": "missed all",
                "scofo_output": [
                    {
                        "est_time": 12,
                        "det_time": 13,
                        "note_start": 14,
                        "midi_note_num": 42,
                    },
                    {
                        "est_time": 13,
                        "det_time": 14,
                        "note_start": 15,
                        "midi_note_num": 43,
                    },
                ],
                "ref": [
                    {
                        "tru_time": 1,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "tru_time": 3,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                ],
                "want": {
                    "miss_rate": 1.0,
                    "misalign_rate": 0.0,
                    "piece_completion": 0.0,
                    "std_of_error": 0.0,
                    "mean_absolute_error": 0.0,
                    "std_of_latency": 0.0,
                    "mean_latency": 0.0,
                    "std_of_offset": 0.0,
                    "mean_absolute_offset": 0.0,
                },
            },
            {
                "name": "misaligned all",
                "scofo_output": [
                    {
                        "est_time": 1000,
                        "det_time": 1000,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "est_time": 1000,
                        "det_time": 1000,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                ],
                "ref": [
                    {
                        "tru_time": 1,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "tru_time": 3,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                ],
                "want": {
                    "miss_rate": 0.0,
                    "misalign_rate": 1.0,
                    "piece_completion": 0.0,
                    "std_of_error": 0.0,
                    "mean_absolute_error": 0.0,
                    "std_of_latency": 0.0,
                    "mean_latency": 0.0,
                    "std_of_offset": 0.0,
                    "mean_absolute_offset": 0.0,
                },
            },
            {
                "name": "aligned all",
                "scofo_output": [
                    {
                        "est_time": 1.1,
                        "det_time": 1.2,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "est_time": 3.1,
                        "det_time": 3.2,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                ],
                "ref": [
                    {
                        "tru_time": 1,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "tru_time": 3,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                ],
                "want": {
                    "miss_rate": 0.0,
                    "misalign_rate": 0.0,
                    "piece_completion": 1.0,
                    "std_of_error": 0.0,
                    "mean_absolute_error": 0.1,
                    "std_of_latency": 0.0,
                    "mean_latency": 0.1,
                    "std_of_offset": 0.0,
                    "mean_absolute_offset": 0.2,
                },
            },
            {
                "name": "aligned some",
                "scofo_output": [
                    {
                        "est_time": 1.1,
                        "det_time": 1.2,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "est_time": 3.1,
                        "det_time": 3.2,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                    {
                        "est_time": 1000,
                        "det_time": 1000,
                        "note_start": 6,
                        "midi_note_num": 42,
                    },
                ],
                "ref": [
                    {
                        "tru_time": 1,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "tru_time": 3,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                    {
                        "tru_time": 5,
                        "note_start": 6,
                        "midi_note_num": 42,
                    },
                ],
                "want": {
                    "miss_rate": 0.0,
                    "misalign_rate": 0.3333333333333333,
                    "piece_completion": 0.6666666666666666,
                    "std_of_error": 0.0,
                    "mean_absolute_error": 0.1,
                    "std_of_latency": 0.0,
                    "mean_latency": 0.1,
                    "std_of_offset": 0.0,
                    "mean_absolute_offset": 0.2,
                },
            },
            {
                "name": "missed some",
                "scofo_output": [
                    {
                        "est_time": 1.1,
                        "det_time": 1.2,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "est_time": 3.1,
                        "det_time": 3.2,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                ],
                "ref": [
                    {
                        "tru_time": 1,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "tru_time": 3,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                    {
                        "tru_time": 5,
                        "note_start": 6,
                        "midi_note_num": 42,
                    },
                ],
                "want": {
                    "miss_rate": 0.3333333333333333,
                    "misalign_rate": 0.0,
                    "piece_completion": 0.6666666666666666,
                    "std_of_error": 0.0,
                    "mean_absolute_error": 0.1,
                    "std_of_latency": 0.0,
                    "mean_latency": 0.1,
                    "std_of_offset": 0.0,
                    "mean_absolute_offset": 0.2,
                },
            },
            {
                "name": "aligned ahead of time",
                "scofo_output": [
                    {
                        "est_time": 0.9,
                        "det_time": 0.95,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "est_time": 2.9,
                        "det_time": 2.95,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                ],
                "ref": [
                    {
                        "tru_time": 1,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "tru_time": 3,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                ],
                "want": {
                    "miss_rate": 0.0,
                    "misalign_rate": 0.0,
                    "piece_completion": 1.0,
                    "std_of_error": 0.0,
                    "mean_absolute_error": 0.1,
                    "std_of_latency": 0.0,
                    "mean_latency": 0.05,
                    "std_of_offset": 0.0,
                    "mean_absolute_offset": 0.05,
                },
            },
            {
                "name": "test errors",
                "scofo_output": [
                    {
                        "est_time": 1.5,
                        "det_time": 1.7,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "est_time": 3.1,
                        "det_time": 3.2,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                ],
                "ref": [
                    {
                        "tru_time": 1,
                        "note_start": 2,
                        "midi_note_num": 42,
                    },
                    {
                        "tru_time": 3,
                        "note_start": 4,
                        "midi_note_num": 42,
                    },
                ],
                "want": {
                    "miss_rate": 0.0,
                    "misalign_rate": 0.0,
                    "piece_completion": 1.0,
                    "std_of_error": 0.2,
                    "mean_absolute_error": 0.3,
                    "std_of_latency": 0.05,
                    "mean_latency": 0.15,
                    "std_of_offset": 0.25,
                    "mean_absolute_offset": 0.45,
                },
            },
        ]

        for tc in cases:
            got = match(tc["scofo_output"], tc["ref"])
            want = tc["want"]
            for key, val in got.items():
                self.assertAlmostEqual(want[key], val, 5, f'{tc["name"]}: {key}')  # type: ignore


class TestPreprocessRef(unittest.TestCase):
    def test_preprocess_ref(self):
        inp: List[RefFileLine] = [
            {
                "tru_time": 1,
                "note_start": 2,
                "midi_note_num": 3,
            },
            {
                "tru_time": 4,
                "note_start": 5,
                "midi_note_num": 6,
            },
        ]
        want: Dict[Tuple[float, int], Tuple[float, int]] = {
            (2, 3): (1, 0),
            (5, 6): (4, 1),
        }
        got = preprocess_ref(inp)
        self.assertEqual(want, got)
