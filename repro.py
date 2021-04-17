import sys
from utils.eprint import eprint


def bach10():
    import os
    import re
    import time
    import json
    from typing import Tuple, List
    from midi import process_midi
    from align import ASMAligner, alignment_repr
    from utils.sharedtypes import Alignment, NoteInfo, FollowerOutputLine
    from utils.eprint import eprint
    from utils.processfile import process_ref_file
    from utils.match import match

    REPO_ROOT = os.path.dirname(os.path.realpath(__file__))
    DATA_PATH = os.path.join(REPO_ROOT, "data")
    BACH10_PATH = os.path.join(DATA_PATH, "bach10", "Bach10_v1.1")
    OUTPUT_PATH = os.path.join(DATA_PATH, "bach10", f"output-{int(time.time())}")
    BACH10_PIECE_PATHS = [
        f.path
        for f in os.scandir(BACH10_PATH)
        if f.is_dir() and bool(re.search(r"^[0-9]{2}-\w+$", os.path.basename(f.path)))
    ]
    BACH10_PIECE_BASENAMES = [os.path.basename(x) for x in BACH10_PIECE_PATHS]

    class Bach10Piece:
        def __init__(self, name: str, postalignthres: float):
            self.name = name
            self.dirpath = os.path.join(BACH10_PATH, name)
            self.refalignpath = os.path.join(self.dirpath, f"{self.name}.txt")
            self.rscorepath = os.path.join(self.dirpath, f"{self.name}.mid")
            self.pscore: List[NoteInfo] = self._refalign_to_pscore()
            self.rscore: List[NoteInfo] = process_midi(self.rscorepath)
            self.postalignthres = postalignthres

        def align(self) -> Alignment:
            """
            align and return (alignment)
            """
            eprint(f"Aligning {self.name}")
            aligner = ASMAligner(self.pscore, self.rscore, postalignthres)
            alignment = aligner.get_alignment()

            return alignment

        def _refalign_to_pscore(self) -> List[NoteInfo]:
            f = open(self.refalignpath)
            t = f.read().strip()
            f.close()

            def process_line(line: str) -> NoteInfo:
                ls = line.split()
                if len(ls) < 4:
                    raise ValueError(f"Too few entries on line: {line}")
                # (performance time (ms), MIDI note num)
                return {"note_start": float(ls[0]), "midi_note_num": int(ls[2])}

            return list(map(process_line, t.splitlines()))

    def align_piece(name: str, postalignthres: float) -> Alignment:
        p = Bach10Piece(name, postalignthres)
        return p.align()

    def alignment_to_follower_output(alignment: Alignment) -> List[FollowerOutputLine]:
        return [
            {
                "est_time": n["p"]["note_start"],
                "det_time": n["p"]["note_start"],
                "note_start": round(
                    n["s"]["note_start"]
                ),  # round to match the notes produced in bach10
                "midi_note_num": n["p"]["midi_note_num"],
            }
            for n in alignment
            if n["p"] is not None
            and n["s"] is not None
            and n["p"]["midi_note_num"] == n["s"]["midi_note_num"]
        ]

    postalignthres: float = -1  # not needed
    alignments: List[Tuple[str, Alignment]] = [
        (name, align_piece(name, postalignthres)) for name in BACH10_PIECE_BASENAMES
    ]

    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    for name, alignment in alignments:
        out_path = os.path.join(OUTPUT_PATH, name)
        os.mkdir(out_path)
        stat_file_path = os.path.join(out_path, f"{name}.align.stat")
        align_file_path = os.path.join(out_path, f"{name}.align.txt")
        sf = open(stat_file_path, "w")
        af = open(align_file_path, "w")
        stdout, stderr = alignment_repr(alignment)
        sf.write(stderr)
        af.write(stdout)
        sf.close()
        af.close()

        follower_output = alignment_to_follower_output(alignment)
        ref_contents = process_ref_file(os.path.join(BACH10_PATH, name, f"{name}.txt"))

        res = match(follower_output, ref_contents)
        res_str = json.dumps(res, indent=4)

        res_file_path = os.path.join(out_path, f"{name}.scofo.json")
        rf = open(res_file_path, "w")
        rf.write(res_str)
        rf.close()

    print(f"OUTPUT: {OUTPUT_PATH}")


def bwv846():
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
        "prelude": 0,
        "fugue": 500,
    }

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
            output_path = os.path.join(
                piece_output_path, f"{piece}.{midi_type}score.txt"
            )
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


if __name__ == "__main__":
    repro_args = sys.argv[1:]
    if len(repro_args) != 1:
        eprint(f"Unknown repro args: {repro_args}. Please see README.md")
        sys.exit(1)
    repro_arg = repro_args[0]

    if repro_arg == "bwv846":
        bwv846()
    elif repro_arg == "bach10":
        bach10()
    else:
        eprint(f"Unknown repro arg: {repro_arg}. Please see README.md")
        sys.exit(1)
