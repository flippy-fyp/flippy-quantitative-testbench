from music21 import converter
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MusicXML to MIDI Converter.")

    parser.add_argument("--input", type=str, help="Input MusicXML file path", required=True)
    parser.add_argument("--output", type=str, help="Output MIDI file path", required=True)

    args = parser.parse_args()

    inp = args.input
    oup = args.output

    s = converter.parse(inp)
    print(s)