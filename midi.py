import argparse
from utils.midi import process_midi
from utils.repr import noteinfos_repr


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MIDI to Score Creation Tool.")

    parser.add_argument("--input", type=str, help="Input MIDI file path", required=True)

    args = parser.parse_args()
    midi_path = args.input

    res = process_midi(midi_path)

    out = noteinfos_repr(res)

    print(out)
