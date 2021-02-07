import os
from midi import process_midi
import time
from utils.repr import noteinfos_repr, alignment_repr
from utils.processfile import process_score_file
from align import ASMAligner
from utils.eprint import eprint

REPO_ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(REPO_ROOT, "data")
BWV846_PATH = os.path.join(DATA_PATH, "bwv846")

# piece name to postalignthres
PIECES = {
    'prelude': 0,
    'fugue': 500,
}

if __name__ == "__main__":
    for piece, postalignthres in PIECES.items():
        eprint(f"=== Processing: {piece} ===")
        eprint(f"Post align thres: {postalignthres}")

        piece_path = os.path.join(BWV846_PATH, piece)
        piece_output_path = os.path.join(piece_path, "output", str(int(time.time())))
        os.makedirs(piece_output_path, exist_ok=True)

        # convert midi to score format
        for midi_type in ["r", "p"]:
            # r: reference (score)
            # p: performance

            mid_path = os.path.join(piece_path, f"{piece}.{midi_type}.mid")
            mid_notes = process_midi(mid_path)
            output_path = os.path.join(piece_output_path, f"{piece}.{midi_type}score.txt")
            mid_str = noteinfos_repr(mid_notes)

            of = open(output_path, "w")
            of.write(mid_str)
            of.close()

        pscore_path = os.path.join(piece_output_path, f"{piece}.pscore.txt")
        rscore_path = os.path.join(piece_output_path, f"{piece}.rscore.txt")

        P = process_score_file(pscore_path)
        S = process_score_file(rscore_path)

        aligner = ASMAligner(P, S, postalignthres)
        alignment = aligner.get_alignment()

        stdout, stderr = alignment_repr(alignment)

        align_out_path = os.path.join(piece_output_path, f"{piece}.align.txt")
        stat_file_path = os.path.join(piece_output_path, f"{piece}.align.stat.txt")

        of = open(align_out_path, "w")
        of.write(stdout)
        of.close()

        sf = open(stat_file_path, "w")
        sf.write(stderr)
        sf.close()
        
        eprint(f"Finished processing {piece}")
        eprint(f"View output in {piece_output_path}")
        eprint()
