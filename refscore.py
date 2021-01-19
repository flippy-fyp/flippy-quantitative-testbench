import argparse
from mido import Message, MidiFile, MidiTrack, second2tick, MetaMessage, bpm2tempo
from processfile import process_ref_file
from typing import List, Tuple

BPM = 120
TICKS_PER_BEAT = 48

def ms_to_tick_gap_and_note_off(
    notes: List[Tuple[float, int]]
) -> List[Tuple[int, int]]:
    res: List[Tuple[int, int]] = []
    # first convert to absolute ticks
    notes_ticks = [
        (int(second2tick(tru_time / 1000, TICKS_PER_BEAT, bpm2tempo(BPM))), midi_note_num)
        for (tru_time, midi_note_num) in notes
    ]

    # add the negative notes 32 ticks after--these are the 'note_off' messages
    off_notes_ticks = [(t + 64, -midi_note_num) for (t, midi_note_num) in notes_ticks]
    notes_ticks.extend(off_notes_ticks)
    # sort by tick
    all_notes = sorted(notes_ticks, key=lambda x: x[0])

    # now convert to gaps
    last_tick = 0
    for (abs_tick, note) in all_notes:
        tick_gap = abs_tick - last_tick
        last_tick = abs_tick
        res.append((tick_gap, note))

    return res


def process_notes(notes: List[Tuple[float, int]]) -> MidiFile:
    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = MidiTrack()

    tempo = bpm2tempo(BPM)
    track.append(MetaMessage('set_tempo', tempo=tempo))
    track.append(MetaMessage('time_signature'))
    track.append(Message('program_change', program=0))

    # first convert to absolute ticks
    notes_ticks = ms_to_tick_gap_and_note_off(notes)
    for tick, midi_note_num in notes_ticks:
        msg_type = "note_on" if midi_note_num >= 0 else "note_off"
        track.append(
            Message(msg_type, note=abs(midi_note_num), velocity=127, time=tick)
        )

    mid.tracks.append(track)
    return mid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reference Score to MIDI Creation Tool."
    )

    parser.add_argument(
        "--input", type=str, help="Input Score file path", required=True
    )
    parser.add_argument("--output", type=str, help="Output file path", required=True)

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output

    score = process_ref_file(input_path)
    notes = [(x["tru_time"], x["midi_note_num"]) for x in score]

    mid = process_notes(notes)
    mid.save(output_path)
