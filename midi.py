import mido
from itertools import chain
from typing import TypedDict, List, Any


class MIDINoteInfo(TypedDict):
    note_start: float  # note start time (ms)
    midi_note_num: int  # MIDI note number


def process_midi(midi_path: str) -> List[MIDINoteInfo]:
    mid = mido.MidiFile(midi_path)
    ret = process_MidiFile(mid)

    for x in ret:
        print(x)
    return ret

def process_MidiFile(mid: mido.MidiFile) -> List[MIDINoteInfo]:
    tempo = get_tempo(mid.tracks[0])
    track_midi_note_info_ticks: List[List[MIDINoteInfo]] = [
        process_track(mid.tracks[i], mid.ticks_per_beat, tempo)
        for i in range(2, len(mid.tracks))
    ]
    # flatten
    ret: List[MIDINoteInfo] = list(chain.from_iterable(track_midi_note_info_ticks))
    # sort
    ret.sort(key=lambda x: x["note_start"])
    return ret

def get_tempo(meta_track: mido.midifiles.tracks.MidiTrack) -> int:
    for msg in list(meta_track):
        if hasattr(msg, 'tempo'):
            return msg.tempo
    raise ValueError('Cannot get track tempo')

def process_track(
    track: mido.midifiles.tracks.MidiTrack, ticks_per_beat: int, tempo: int
) -> List[MIDINoteInfo]:
    ret: List[MIDINoteInfo] = []
    curr_tick = 0
    for msg in track:
        if hasattr(msg, "velocity"):
            if msg.velocity > 0:
                ret.append(
                    {
                        "note_start": mido.tick2second(curr_tick, ticks_per_beat, tempo)
                        * 1000,
                        "midi_note_num": msg.note,
                    }
                )
        curr_tick += msg.time
    return ret


process_midi(
    r"C:\Users\lhlee\Documents\flippy-fyp\flippy-testbench\midi\wtk1-prelude1.mid"
)
