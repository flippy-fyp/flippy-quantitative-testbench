import argparse
from itertools import groupby, chain
from typing import List, Dict, Tuple, Optional, TypedDict
from utils.sharedtypes import NoteInfo, Alignment
from utils.processfile import process_score_file
from utils.eprint import eprint
from utils.postalign import PostAlign
from utils.repr import alignment_repr


class GElem:
    """
    Represents an element in ASMAligner's grid G.
    """

    __allowed = ("n", "score", "left", "down", "diag")

    def __init__(self, **kwargs):
        self.n: Optional[NoteInfo] = None
        self.score: Optional[int] = None
        self.left = False
        self.down = False
        self.diag = False

        for k, v in kwargs.items():
            assert k in self.__class__.__allowed
            setattr(self, k, v)


class ASMAligner:
    def __init__(self, P: List[NoteInfo], S: List[NoteInfo], postalignthres: float):
        self.ALPHA = 1
        self.GAMMA = -1
        self.BETA_HAT = -12
        self._P = sort_parallel_voices(P)
        self._S = sort_parallel_voices(S)
        self._G: Dict[int, Dict[int, GElem]] = {}

        self.postalignthres = postalignthres

    def get_alignment(self) -> Alignment:
        """
        Gets the optimal alignment
        """
        self._set_up()
        self._solve()

        al = self._get_alignment_helper(
            1 + len(self._P),
            1 + len(self._S),
        )
        if al is None:
            raise ValueError("Cannot get alignment")

        if self.postalignthres >= 0:
            eprint(f"Running PostAlign with threshold {self.postalignthres}")
            pa = PostAlign(al, self.postalignthres)
            al = pa.postalign()

        return al

    def _get_alignment_helper(self, x: int, y: int) -> Optional[Alignment]:
        if (x, y) == (1, 1):
            return []

        g = self._get_G(x, y)

        p = self._get_G(x, 0).n
        s = self._get_G(0, y).n

        if g.diag:
            al = self._get_alignment_helper(x - 1, y - 1)
            if al is not None:
                return al + [{"p": p, "s": s}]
        if g.left:
            al = self._get_alignment_helper(x - 1, y)
            if al is not None:
                return al + [{"p": p, "s": None}]
        if g.down:
            al = self._get_alignment_helper(x, y - 1)
            if al is not None:
                return al + [{"p": None, "s": s}]
        return None

    def _set_up(self):
        """
        sets up the grid G
        """
        P = self._P
        S = self._S

        x = 2
        for p in P:
            self._set_G(x, 0, GElem(n=p))
            x += 1

        y = 2
        for s in S:
            self._set_G(0, y, GElem(n=s))
            y += 1

        self._set_G(0, 0, GElem())
        self._set_G(1, 0, GElem())
        self._set_G(0, 1, GElem())
        self._set_G(1, 1, GElem(score=0))

        score_ctr = -1
        for x in range(2, 2 + len(P)):
            self._set_G(x, 1, GElem(score=score_ctr, left=True))
            score_ctr -= 1

        score_ctr = -1
        for y in range(2, 2 + len(S)):
            self._set_G(1, y, GElem(score=score_ctr, down=True))
            score_ctr -= 1

    def _solve(self):
        """
        Starts getting all required scores.
        """
        self._score(
            1 + len(self._P),
            1 + len(self._S),
        )

    def _sim(self, c: NoteInfo, s: NoteInfo) -> int:
        """
        Calculates the similarity score between c and s.
        """
        cn = c["midi_note_num"]
        sn = s["midi_note_num"]
        if cn == sn:
            return self.ALPHA
        return max(self.BETA_HAT, -abs(cn - sn))

    def _score(self, x: int, y: int) -> int:
        """
        Returns the score calculated for G[x][y]
        """
        if x == 0 or y == 0:
            return -100000000

        sc = self._get_G(x, y).score if x in self._G and y in self._G[x] else None
        if sc is None:
            c = self._get_G(x, 0).n
            if c is None:
                raise ValueError(f"_score called with invalid x: {x}")
            s = self._get_G(0, y).n
            if s is None:
                raise ValueError(f"_score called with invalid x: {x}")

            sim_val = self._sim(c, s)

            score_case_1 = self._score(x - 1, y - 1) + sim_val
            score_case_2 = self._score(x - 1, y) + self.GAMMA
            score_case_3 = self._score(x, y - 1) + self.GAMMA

            sc = max(
                score_case_1,
                score_case_2,
                score_case_3,
            )

            self._set_G(
                x,
                y,
                GElem(
                    score=sc,
                    diag=sc == score_case_1,
                    left=sc == score_case_2,
                    down=sc == score_case_3,
                ),
            )
        return sc

    def _set_G(self, x: int, y: int, e: GElem):
        """
        Sets G[x][y]
        """
        if x not in self._G:
            self._G[x] = {}
        self._G[x][y] = e

    def _get_G(self, x: int, y: int) -> GElem:
        """
        Gets G[x][y]
        """
        if x not in self._G:
            raise ValueError(f"No ({x}, ...) in G")
        if y not in self._G[x]:
            raise ValueError(f"No ({x}, {y}) in G")

        return self._G[x][y]


def sort_parallel_voices(notes: List[NoteInfo]) -> List[NoteInfo]:
    """
    Sorts parallel notes in notes in ascending order.
    """
    sorted_grouped_par_notes: List[List[NoteInfo]] = [
        sorted(list(group), key=lambda n: n["midi_note_num"])
        for _, group in groupby(notes, lambda n: n["note_start"])
    ]

    # flatten back
    return list(chain.from_iterable(sorted_grouped_par_notes))


def print_alignment(alignment: Alignment):
    stdout, stderr = alignment_repr(alignment)
    print(stdout)
    eprint(stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Optimal global aligner to produce testbench reference data "
        + "from the performance score and the reference score"
    )

    parser.add_argument(
        "--pscore", type=str, help="Path to performance score", required=True
    )
    parser.add_argument(
        "--rscore", type=str, help="Path to reference score", required=True
    )
    parser.add_argument(
        "--postalignthres",
        type=float,
        help="Threshold (in ms) to run postalignment fixes. Enabled if >= 0. "
        + "Total distance in score time to look backwards/forwards "
        + "for a matching gap. "
        + "Useful for pieces with strong polyphony. Warning: perturbs score data!",
        default=0,
    )

    args = parser.parse_args()
    pscore_path = args.pscore
    rscore_path = args.rscore
    postalignthres = args.postalignthres

    P = process_score_file(pscore_path)
    S = process_score_file(rscore_path)

    aligner = ASMAligner(P, S, postalignthres)
    alignment = aligner.get_alignment()

    print_alignment(alignment)
