import unittest
from typing import List, Tuple
from sharedtypes import Alignment
from gapfix import GapFixer

class TestGapFixer(unittest.TestCase):
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
            # match backwards first
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
            ),
        ]
    
        for alignment, threshold_ms, want in cases:
            gf = GapFixer(alignment, threshold_ms)
            got = gf.fix_gaps()
            self.assertEqual(want, got)