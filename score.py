from utils.processfile import process_score_file
from refscore import process_notes
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score to MIDI Creation Tool.")

    parser.add_argument(
        "--input", type=str, help="Input Score file path", required=True
    )
    parser.add_argument("--output", type=str, help="Output file path", required=True)
    parser.add_argument(
        "--offset_ticks",
        type=int,
        help="Number of MIDI ticks to place note offsets after their respective onsets.",
        default=64,
    )

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output

    score = process_score_file(input_path)
    notes = [(x["note_start"], x["midi_note_num"]) for x in score]

    mid = process_notes(notes, args.offset_ticks)
    mid.save(output_path)
