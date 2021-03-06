from music21 import converter  # type: ignore
import argparse
import sys
import shutil
import os
import math
from utils.eprint import eprint
from midi import process_midi
from utils.repr import noteinfos_repr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MusicXML to MIDI/Score Converter.")

    parser.add_argument(
        "--input", type=str, help="Input MusicXML file path", required=True
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["midi", "score"],
        help="Output type",
        default="score",
    )
    parser.add_argument("--output", type=str, help="Output file path for MIDI")

    args = parser.parse_args()

    inp = args.input
    oup = args.output
    mode = args.mode

    if mode == "midi" and len(oup) == 0:
        eprint("Output file path required for midi mode.")
        sys.exit(1)

    s = converter.parse(inp)

    # first convert to MIDI
    tmp_path = s.write("midi")

    if mode == "midi":
        shutil.move(tmp_path, oup)
    elif mode == "score":
        res = process_midi(tmp_path)

        out = noteinfos_repr(res)

        print(out)
