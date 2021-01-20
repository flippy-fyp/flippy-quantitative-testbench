import os
import re
import time
from typing import Dict, Tuple, List
from midi import process_midi
from align import ASMAligner, alignment_repr
from sharedtypes import Alignment, NoteInfo
from utils import eprint
from processfile import process_score_file

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


if __name__ == "__main__":
    postalignthres: float = -1 
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

    print(f"OUTPUT: {OUTPUT_PATH}")
