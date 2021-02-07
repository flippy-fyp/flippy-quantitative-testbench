from utils.sharedtypes import Alignment, NoteInfo
from typing import Optional, List, Tuple
from copy import deepcopy

class PostAlign:
    def __init__(self, alignment: Alignment, threshold_ms: float):
        self.alignment = deepcopy(alignment)
        self.threshold_ms = threshold_ms
        self.two_pass = True

    def postalign(self) -> Alignment:
        self._postalign_backward()
        if self.two_pass:
            # reverse
            self.alignment.reverse()
            # run again
            self._postalign_backward()
            self.alignment.reverse()
        return self.alignment

    def _postalign_backward(self):
        # walk backwards so the closest errors are fixed first
        for i in range(len(self.alignment) - 1, -1, -1):
            el_p = self.alignment[i]["p"]
            el_s = self.alignment[i]["s"]

            next_indices = self._get_threshold_range(i)

            if el_p is not None:
                # el_p OK
                if el_s is not None and el_s["midi_note_num"] != el_p["midi_note_num"]:
                    # mismatch
                    self._fix_mismatch(el_p, el_s, i)
                elif el_s is None:
                    # score gap
                    self._fix_gap_el_p(el_p, i)
            elif el_s is not None:
                # gap in el_p
                self._fix_gap_el_s(el_s, i)

    def _fix_gap_el_s(
        self,
        el_s: NoteInfo,
        i: int,
    ):
        """
        el_s has a gap perf note. Try to fix it.
        """
        next_indices = self._get_threshold_range(i)
        for j in next_indices:
            cand_el = self.alignment[j]
            cand_el_p = cand_el["p"]
            cand_el_s = cand_el["s"]
            if cand_el_p is not None and cand_el_s is not None:
                if cand_el_s["midi_note_num"] != cand_el_p["midi_note_num"]:
                    # mismatch--check if cand_el_p matches ours
                    if cand_el_p["midi_note_num"] == el_s["midi_note_num"]:
                        # match, now we need to swap them
                        self._swap_score_note(i, j)
                        return
            elif cand_el_p is not None:
                # cand_el["s"] is a gap
                # check if the note matches
                if cand_el_p["midi_note_num"] == el_s["midi_note_num"]:
                    # match, now we need to merge them
                    self.alignment[j]["s"] = deepcopy(el_s)
                    del self.alignment[i : i + 1]
                    return

    def _fix_gap_el_p(
        self,
        el_p: NoteInfo,
        i: int,
    ):
        """
        el_p has a gap score note. Try to fix it.
        """
        next_indices = self._get_threshold_range(i)
        for j in next_indices:
            cand_el = self.alignment[j]
            cand_el_p = cand_el["p"]
            cand_el_s = cand_el["s"]
            if cand_el_s is not None:
                if cand_el_p is not None:
                    if cand_el_s["midi_note_num"] != cand_el_p["midi_note_num"]:
                        # mismatch--check if cand_el_s matches ours
                        if cand_el_s["midi_note_num"] == el_p["midi_note_num"]:
                            self._swap_score_note(i, j)
                            return
                else:
                    # cand_el["p"] is a gap
                    # check if the note matches
                    if cand_el_s["midi_note_num"] == el_p["midi_note_num"]:
                        # match, now we need to merge them
                        self.alignment[i]["s"] = deepcopy(cand_el_s)
                        del self.alignment[j : j + 1]
                        return

    def _fix_mismatch(
        self,
        el_p: NoteInfo,
        el_s: NoteInfo,
        i: int,
    ):
        """
        el_p and el_s mismatch. Try to fix it.
        """
        next_indices = self._get_threshold_range(i)
        for j in next_indices:
            cand_el = self.alignment[j]
            cand_el_p = cand_el["p"]
            cand_el_s = cand_el["s"]
            if cand_el_s is not None:
                if cand_el_p is not None:
                    if cand_el_s["midi_note_num"] != cand_el_p["midi_note_num"]:
                        # mismatch too--check if cand_el_s matches ours
                        if cand_el_s["midi_note_num"] == el_p["midi_note_num"]:
                            self._swap_score_note(i, j)
                            return
                else:
                    # cand_el["p"] is a gap
                    # check if the note matches
                    if cand_el_s["midi_note_num"] == el_p["midi_note_num"]:
                        self._swap_score_note(i, j)
                        return

    def _get_threshold_range(self, i: int) -> List[int]:
        """
        get valid indices forwards, with score time within
        the threshold of the current--if available--score time, the closest preceding score
        time and finally the closest succeeding score time.

        Returns (valid indices forwards).
        """

        # first find the closest score time to the current note
        curr_score_time: Optional[float] = None
        for j in range(i, -1, -1):
            cand = self.alignment[j]
            if cand["s"] is not None:
                curr_score_time = cand["s"]["note_start"]
                break
        if curr_score_time is None:
            for j in range(i + 1, len(self.alignment)):
                cand = self.alignment[j]
                if cand["s"] is not None:
                    curr_score_time = cand["s"]["note_start"]
                    break
        if curr_score_time is None:
            # no score time at all, may be a bogus alignment.
            return []

        next_indices: List[int] = []

        # Because score times are perturbed, don't instantly break when the first score_time is over
        # the threshold. Look forward a certain number of notes.
        LOOKFORWARD_LIMIT = 100
        for j in range(i + 1, min(len(self.alignment), i + LOOKFORWARD_LIMIT)):
            cand = self.alignment[j]
            if cand["s"] is not None:
                if abs(cand["s"]["note_start"] - curr_score_time) <= self.threshold_ms:
                    next_indices.append(j)

        return next_indices

    def _swap_score_note(self, i: int, j: int):
        self.alignment[i]["s"], self.alignment[j]["s"] = (
            self.alignment[j]["s"],
            self.alignment[i]["s"],
        )
