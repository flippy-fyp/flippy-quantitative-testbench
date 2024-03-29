import unittest
from os import path
from midi import process_midi
from utils.sharedtypes import NoteInfo
from typing import List


class TestProcessMIDI(unittest.TestCase):
    def test_process_midi(self):
        midi_file_path = path.join(
            path.dirname(path.dirname(__file__)),
            "data",
            "sample_midis",
            "short_demo.mid",
        )
        want: List[NoteInfo] = [
            {"midi_note_num": 60, "note_start": 4.882802734375},
            {"midi_note_num": 62, "note_start": 514.6474082031249},
            {"midi_note_num": 64, "note_start": 1010.2518857421874},
            {"midi_note_num": 64, "note_start": 1505.8563632812497},
            {"midi_note_num": 67, "note_start": 1505.8563632812497},
        ]
        got = process_midi(midi_file_path)
        self.assertEqual(want, got)

    def test_process_midi_tracks(self):
        midi_file_path = path.join(
            path.dirname(path.dirname(__file__)),
            "data",
            "sample_midis",
            "short_demo_chord.mid",
        )
        want: List[NoteInfo] = [
            {"midi_note_num": 60, "note_start": 4.882802734375},
            {"midi_note_num": 64, "note_start": 4.882802734375},
        ]
        got = process_midi(midi_file_path)
        self.assertEqual(want, got)
