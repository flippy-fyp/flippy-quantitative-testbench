import mido
import argparse
import json
from itertools import chain
from typing import TypedDict, List, Any
from sharedtypes import NoteInfo


def process_midi(midi_path: str) -> List[NoteInfo]:
    mid = mido.MidiFile(midi_path)
    ret = process_MidiFile(mid)

    return ret


def process_MidiFile(mid: mido.MidiFile) -> List[NoteInfo]:
    tempo = get_tempo(mid.tracks[0])
    track_midi_note_info_ticks: List[List[NoteInfo]] = [
        process_track(mid.tracks[i], mid.ticks_per_beat, tempo)
        for i in range(1, len(mid.tracks))
    ]
    # flatten
    ret: List[NoteInfo] = list(chain.from_iterable(track_midi_note_info_ticks))
    # sort
    ret.sort(key=lambda x: x["note_start"])
    return ret


def get_tempo(meta_track: mido.midifiles.tracks.MidiTrack) -> int:
    for msg in list(meta_track):
        if hasattr(msg, "tempo"):
            return msg.tempo
    raise ValueError("Cannot get track tempo")


def process_track(
    track: mido.midifiles.tracks.MidiTrack, ticks_per_beat: int, tempo: int
) -> List[NoteInfo]:
    ret: List[NoteInfo] = []
    curr_tick = 0
    for msg in track:
        curr_tick += msg.time
        if hasattr(msg, "velocity"):
            if msg.velocity > 0:
                ret.append(
                    {
                        "note_start": mido.tick2second(curr_tick, ticks_per_beat, tempo)
                        * 1000,
                        "midi_note_num": msg.note,
                    }
                )
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MIDI to Score Creation Tool.")

    parser.add_argument("--midi", type=str, help="Input MIDI file path", required=True)

    args = parser.parse_args()
    midi_path = args.midi

    res = process_midi(midi_path)

    for r in res:
        print(f'{r["note_start"]:.3f} {r["midi_note_num"]}')
