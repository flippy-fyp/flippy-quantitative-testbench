# import argparse

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Reference Score to MIDI Creation Tool.")

#     parser.add_argument("--input", type=str, help="Input Score file path", required=True)

#     args = parser.parse_args()
#     midi_path = args.midi

#     res = process_midi(midi_path)

#     for r in res:
#         print(f'{r["note_start"]:.3f} {r["midi_note_num"]}')
