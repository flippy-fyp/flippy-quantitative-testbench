import unittest
from typing import List, Tuple
from utils.sharedtypes import NoteInfo
from align import sort_parallel_voices, ASMAligner, Alignment


class TestASMAligner(unittest.TestCase):
    def test_sim(self):
        cases: List[Tuple[NoteInfo, NoteInfo, int]] = [
            (
                {"note_start": 0, "midi_note_num": 69},
                {"note_start": 0, "midi_note_num": 69},
                1,
            ),
            (
                {"note_start": 0, "midi_note_num": 69},
                {"note_start": 0, "midi_note_num": 68},
                -1,
            ),
            (
                {"note_start": 0, "midi_note_num": 68},
                {"note_start": 0, "midi_note_num": 69},
                -1,
            ),
            (
                {"note_start": 0, "midi_note_num": 69},
                {"note_start": 0, "midi_note_num": 79},
                -10,
            ),
            (
                {"note_start": 0, "midi_note_num": 10},
                {"note_start": 0, "midi_note_num": 100},
                -12,
            ),
        ]
        for c, s, want in cases:
            aligner = ASMAligner([], [], -1)
            got = aligner._sim(c, s)
            self.assertEqual(want, got)

    def test_align(self):
        cases: List[Tuple[List[NoteInfo], List[NoteInfo], Alignment]] = [
            (
                [
                    {"note_start": 0, "midi_note_num": 69},
                    {"note_start": 10, "midi_note_num": 70},
                    {"note_start": 20, "midi_note_num": 71},
                ],
                [
                    {"note_start": 10, "midi_note_num": 69},
                    {"note_start": 20, "midi_note_num": 70},
                    {"note_start": 30, "midi_note_num": 71},
                ],
                [
                    {
                        "p": {"note_start": 0, "midi_note_num": 69},
                        "s": {"note_start": 10, "midi_note_num": 69},
                    },
                    {
                        "p": {"note_start": 10, "midi_note_num": 70},
                        "s": {"note_start": 20, "midi_note_num": 70},
                    },
                    {
                        "p": {"note_start": 20, "midi_note_num": 71},
                        "s": {"note_start": 30, "midi_note_num": 71},
                    },
                ],
            ),
            (
                [
                    {"note_start": 10, "midi_note_num": 0},
                    {"note_start": 20, "midi_note_num": 1},
                    {"note_start": 30, "midi_note_num": 2},
                    {"note_start": 40, "midi_note_num": 3},
                    {"note_start": 50, "midi_note_num": 0},
                    {"note_start": 60, "midi_note_num": 1},
                    {"note_start": 70, "midi_note_num": 4},
                ],
                [
                    {"note_start": 100, "midi_note_num": 0},
                    {"note_start": 200, "midi_note_num": 2},
                    {"note_start": 300, "midi_note_num": 3},
                    {"note_start": 400, "midi_note_num": 3},
                    {"note_start": 500, "midi_note_num": 2},
                    {"note_start": 600, "midi_note_num": 1},
                    {"note_start": 700, "midi_note_num": 2},
                ],
                [
                    {
                        "p": {"note_start": 10, "midi_note_num": 0},
                        "s": {"note_start": 100, "midi_note_num": 0},
                    },
                    {
                        "p": {"note_start": 20, "midi_note_num": 1},
                        "s": None,
                    },
                    {
                        "p": {"note_start": 30, "midi_note_num": 2},
                        "s": {"note_start": 200, "midi_note_num": 2},
                    },
                    {
                        "p": None,
                        "s": {"note_start": 300, "midi_note_num": 3},
                    },
                    {
                        "p": {"note_start": 40, "midi_note_num": 3},
                        "s": {"note_start": 400, "midi_note_num": 3},
                    },
                    {
                        "p": {"note_start": 50, "midi_note_num": 0},
                        "s": {"note_start": 500, "midi_note_num": 2},
                    },
                    {
                        "p": {"note_start": 60, "midi_note_num": 1},
                        "s": {"note_start": 600, "midi_note_num": 1},
                    },
                    {
                        "p": {"note_start": 70, "midi_note_num": 4},
                        "s": {"note_start": 700, "midi_note_num": 2},
                    },
                ],
            ),
        ]
        for P, S, want in cases:
            aligner = ASMAligner(P, S, -1)
            got = aligner.get_alignment()
            self.assertEqual(want, got)


class TestSortParallelVoices(unittest.TestCase):
    def test_sort_parallel_voices(self):
        cases: List[Tuple[List[NoteInfo], List[NoteInfo]]] = [
            (
                [
                    {
                        "note_start": 0,
                        "midi_note_num": 0,
                    },
                    {
                        "note_start": 1,
                        "midi_note_num": 1,
                    },
                    {
                        "note_start": 2,
                        "midi_note_num": 2,
                    },
                ],
                [
                    {
                        "note_start": 0,
                        "midi_note_num": 0,
                    },
                    {
                        "note_start": 1,
                        "midi_note_num": 1,
                    },
                    {
                        "note_start": 2,
                        "midi_note_num": 2,
                    },
                ],
            ),
            (
                [
                    {
                        "note_start": 0,
                        "midi_note_num": 0,
                    },
                    {
                        "note_start": 0,
                        "midi_note_num": 1,
                    },
                    {
                        "note_start": 0,
                        "midi_note_num": 2,
                    },
                ],
                [
                    {
                        "note_start": 0,
                        "midi_note_num": 0,
                    },
                    {
                        "note_start": 0,
                        "midi_note_num": 1,
                    },
                    {
                        "note_start": 0,
                        "midi_note_num": 2,
                    },
                ],
            ),
            (
                [
                    {
                        "note_start": 0,
                        "midi_note_num": 0,
                    },
                    {
                        "note_start": 1,
                        "midi_note_num": 2,
                    },
                    {
                        "note_start": 1,
                        "midi_note_num": 1,
                    },
                ],
                [
                    {
                        "note_start": 0,
                        "midi_note_num": 0,
                    },
                    {
                        "note_start": 1,
                        "midi_note_num": 1,
                    },
                    {
                        "note_start": 1,
                        "midi_note_num": 2,
                    },
                ],
            ),
            (
                [
                    {
                        "note_start": 0,
                        "midi_note_num": 0,
                    },
                    {
                        "note_start": 1,
                        "midi_note_num": 2,
                    },
                    {
                        "note_start": 1,
                        "midi_note_num": 1,
                    },
                    {
                        "note_start": 3,
                        "midi_note_num": 2,
                    },
                    {
                        "note_start": 3,
                        "midi_note_num": 1,
                    },
                    {
                        "note_start": 3,
                        "midi_note_num": 0,
                    },
                ],
                [
                    {
                        "note_start": 0,
                        "midi_note_num": 0,
                    },
                    {
                        "note_start": 1,
                        "midi_note_num": 1,
                    },
                    {
                        "note_start": 1,
                        "midi_note_num": 2,
                    },
                    {
                        "note_start": 3,
                        "midi_note_num": 0,
                    },
                    {
                        "note_start": 3,
                        "midi_note_num": 1,
                    },
                    {
                        "note_start": 3,
                        "midi_note_num": 2,
                    },
                ],
            ),
        ]

        for inp, want in cases:
            got = sort_parallel_voices(inp)
            self.assertEqual(want, got)
