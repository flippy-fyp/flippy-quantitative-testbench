import unittest
from typing import List, Tuple
from sharedtypes import Alignment
from postalign import PostAlign


class TestPostAlign(unittest.TestCase):
    def test_fix_mismatches(self):
        cases: List[Tuple[Alignment, float, Alignment]] = [
            # swapped within threshold
            (
                [
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 10,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 20,
                        },
                    },
                    {
                        "p": {
                            "note_start": 15,
                            "midi_note_num": 20,
                        },
                        "s": {
                            "note_start": 25,
                            "midi_note_num": 10,
                        },
                    },
                ],
                50,
                [
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 10,
                        },
                        "s": {
                            "note_start": 25,
                            "midi_note_num": 10,
                        },
                    },
                    {
                        "p": {
                            "note_start": 15,
                            "midi_note_num": 20,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 20,
                        },
                    },
                ],
            ),
            # swapped within threshold, closest swapped
            (
                [
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 10,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 20,
                        },
                    },
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 10,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 20,
                        },
                    },
                    {
                        "p": {
                            "note_start": 15,
                            "midi_note_num": 20,
                        },
                        "s": {
                            "note_start": 25,
                            "midi_note_num": 10,
                        },
                    },
                ],
                50,
                [
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 10,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 20,
                        },
                    },
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 10,
                        },
                        "s": {
                            "note_start": 25,
                            "midi_note_num": 10,
                        },
                    },
                    {
                        "p": {
                            "note_start": 15,
                            "midi_note_num": 20,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 20,
                        },
                    },
                ],
            ),
            # unswapped outside threshold
            (
                [
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 10,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 20,
                        },
                    },
                    {
                        "p": {
                            "note_start": 15,
                            "midi_note_num": 20,
                        },
                        "s": {
                            "note_start": 125,
                            "midi_note_num": 10,
                        },
                    },
                ],
                50,
                [
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 10,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 20,
                        },
                    },
                    {
                        "p": {
                            "note_start": 15,
                            "midi_note_num": 20,
                        },
                        "s": {
                            "note_start": 125,
                            "midi_note_num": 10,
                        },
                    },
                ],
            ),
            # swapped, note in middle
            (
                [
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 10,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 20,
                        },
                    },
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 69,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 69,
                        },
                    },
                    {
                        "p": {
                            "note_start": 15,
                            "midi_note_num": 20,
                        },
                        "s": {
                            "note_start": 25,
                            "midi_note_num": 10,
                        },
                    },
                ],
                50,
                [
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 10,
                        },
                        "s": {
                            "note_start": 25,
                            "midi_note_num": 10,
                        },
                    },
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 69,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 69,
                        },
                    },
                    {
                        "p": {
                            "note_start": 15,
                            "midi_note_num": 20,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 20,
                        },
                    },
                ],
            ),
        ]
        for alignment, threshold_ms, want in cases:
            pa = PostAlign(alignment, threshold_ms)
            got = pa.postalign()
            self.assertEqual(want, got)

    def test_fix_gaps(self):
        cases: List[Tuple[Alignment, float, Alignment]] = [
            # match and mismatch not cared
            (
                [
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 11,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 11,
                        },
                    },
                    {
                        "p": {
                            "note_start": 50,
                            "midi_note_num": 12,
                        },
                        "s": {
                            "note_start": 60,
                            "midi_note_num": 69,
                        },
                    },
                ],
                50.0,
                [
                    {
                        "p": {
                            "note_start": 10,
                            "midi_note_num": 11,
                        },
                        "s": {
                            "note_start": 20,
                            "midi_note_num": 11,
                        },
                    },
                    {
                        "p": {
                            "note_start": 50,
                            "midi_note_num": 12,
                        },
                        "s": {
                            "note_start": 60,
                            "midi_note_num": 69,
                        },
                    },
                ],
            ),
            # empty
            (
                [],
                50.0,
                [],
            ),
            # matched gap backwards within threshold
            (
                [
                    {
                        "p": None,
                        "s": {
                            "note_start": 6469,
                            "midi_note_num": 64,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7810,
                            "midi_note_num": 64,
                        },
                        "s": None,
                    },
                ],
                50.0,
                [
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7810,
                            "midi_note_num": 64,
                        },
                        "s": {
                            "note_start": 6469,
                            "midi_note_num": 64,
                        },
                    },
                ],
            ),
            # unmatched gap backwards
            (
                [
                    {
                        "p": None,
                        "s": {
                            "note_start": 6469,
                            "midi_note_num": 100,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7810,
                            "midi_note_num": 64,
                        },
                        "s": None,
                    },
                ],
                50.0,
                [
                    {
                        "p": None,
                        "s": {
                            "note_start": 6469,
                            "midi_note_num": 100,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7810,
                            "midi_note_num": 64,
                        },
                        "s": None,
                    },
                ],
            ),
            # unmatched gap backwards over threshold
            (
                [
                    {
                        "p": None,
                        "s": {
                            "note_start": 300,
                            "midi_note_num": 64,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7810,
                            "midi_note_num": 64,
                        },
                        "s": None,
                    },
                ],
                50.0,
                [
                    {
                        "p": None,
                        "s": {
                            "note_start": 300,
                            "midi_note_num": 64,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7810,
                            "midi_note_num": 64,
                        },
                        "s": None,
                    },
                ],
            ),
            # matched gap forwards within threshold
            (
                [
                    {
                        "p": {
                            "note_start": 7750,
                            "midi_note_num": 64,
                        },
                        "s": None,
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": None,
                        "s": {
                            "note_start": 6542,
                            "midi_note_num": 64,
                        },
                    },
                ],
                50.0,
                [
                    {
                        "p": {
                            "note_start": 7750,
                            "midi_note_num": 64,
                        },
                        "s": {
                            "note_start": 6542,
                            "midi_note_num": 64,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                ],
            ),
            # unmatched gap forwards
            (
                [
                    {
                        "p": {
                            "note_start": 7750,
                            "midi_note_num": 64,
                        },
                        "s": None,
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": None,
                        "s": {
                            "note_start": 6542,
                            "midi_note_num": 100,
                        },
                    },
                ],
                50.0,
                [
                    {
                        "p": {
                            "note_start": 7750,
                            "midi_note_num": 64,
                        },
                        "s": None,
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": None,
                        "s": {
                            "note_start": 6542,
                            "midi_note_num": 100,
                        },
                    },
                ],
            ),
            # unmatched gap forwards over threshold
            (
                [
                    {
                        "p": {
                            "note_start": 7750,
                            "midi_note_num": 64,
                        },
                        "s": None,
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": None,
                        "s": {
                            "note_start": 10000,
                            "midi_note_num": 64,
                        },
                    },
                ],
                50.0,
                [
                    {
                        "p": {
                            "note_start": 7750,
                            "midi_note_num": 64,
                        },
                        "s": None,
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 6500,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": None,
                        "s": {
                            "note_start": 10000,
                            "midi_note_num": 64,
                        },
                    },
                ],
            ),
            # match closest first
            (
                [
                    {
                        "p": None,
                        "s": {
                            "note_start": 6469,
                            "midi_note_num": 64,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 7980,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7810,
                            "midi_note_num": 64,
                        },
                        "s": None,
                    },
                    {
                        "p": {
                            "note_start": 8000,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 8000,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": None,
                        "s": {
                            "note_start": 8000,
                            "midi_note_num": 64,
                        },
                    },
                ],
                50.0,
                [
                    {
                        "p": None,
                        "s": {
                            "note_start": 6469,
                            "midi_note_num": 64,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7780,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 7980,
                            "midi_note_num": 67,
                        },
                    },
                    {
                        "p": {
                            "note_start": 7810,
                            "midi_note_num": 64,
                        },
                        "s": {
                            "note_start": 8000,
                            "midi_note_num": 64,
                        },
                    },
                    {
                        "p": {
                            "note_start": 8000,
                            "midi_note_num": 67,
                        },
                        "s": {
                            "note_start": 8000,
                            "midi_note_num": 67,
                        },
                    },
                ],
            ),
        ]

        for alignment, threshold_ms, want in cases:
            pa = PostAlign(alignment, threshold_ms)
            got = pa.postalign()
            self.assertEqual(want, got)

    def test_fix_reverse_mismatch(self):
        # tests for cases that requires reverse processing
        cases: List[Tuple[Alignment, float, Alignment]] = [
            (
                [
                    {
                        "p": {
                            "note_start": 78522.5,
                            "midi_note_num": 46,
                        },
                        "s": {
                            "note_start": 63000,
                            "midi_note_num": 45,
                        },
                    },
                    {
                        "p": {
                            "note_start": 78536,
                            "midi_note_num": 69,
                        },
                        "s": {
                            "note_start": 63001,
                            "midi_note_num": 69,
                        },
                    },
                    {
                        "p": {
                            "note_start": 79161.667,
                            "midi_note_num": 45,
                        },
                        "s": {
                            "note_start": 63002,
                            "midi_note_num": 43,
                        },
                    },
                ],
                50.0,
                [
                    {
                        "p": {
                            "note_start": 78522.5,
                            "midi_note_num": 46,
                        },
                        "s": {
                            "note_start": 63002,
                            "midi_note_num": 43,
                        },
                    },
                    {
                        "p": {
                            "note_start": 78536,
                            "midi_note_num": 69,
                        },
                        "s": {
                            "note_start": 63001,
                            "midi_note_num": 69,
                        },
                    },
                    {
                        "p": {
                            "note_start": 79161.667,
                            "midi_note_num": 45,
                        },
                        "s": {
                            "note_start": 63000,
                            "midi_note_num": 45,
                        },
                    },
                ],
            ),
        ]

        for alignment, threshold_ms, want in cases:
            pa = PostAlign(alignment, threshold_ms)
            got = pa.postalign()
            self.assertEqual(want, got)

    def test_fix_reverse_gap(self):
        # tests for cases that requires reverse processing
        cases: List[Tuple[Alignment, float, Alignment]] = [
            (
                [
                    {
                        "p": None,
                        "s": {
                            "note_start": 37250,
                            "midi_note_num": 60,
                        },
                    },
                    {
                        "p": {
                            "note_start": 45309.167,
                            "midi_note_num": 78,
                        },
                        "s": {
                            "note_start": 37250,
                            "midi_note_num": 78,
                        },
                    },
                    {
                        "p": {
                            "note_start": 45646.667,
                            "midi_note_num": 60,
                        },
                        "s": None,
                    },
                ],
                50.0,
                [
                    {
                        "p": {
                            "note_start": 45309.167,
                            "midi_note_num": 78,
                        },
                        "s": {
                            "note_start": 37250,
                            "midi_note_num": 78,
                        },
                    },
                    {
                        "p": {
                            "note_start": 45646.667,
                            "midi_note_num": 60,
                        },
                        "s": {
                            "note_start": 37250,
                            "midi_note_num": 60,
                        },
                    },
                ],
            ),
        ]
        for alignment, threshold_ms, want in cases:
            pa = PostAlign(alignment, threshold_ms)
            got = pa.postalign()
            print(got)
            self.assertEqual(want, got)
