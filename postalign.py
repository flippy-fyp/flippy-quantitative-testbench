from sharedtypes import Alignment, NoteInfo
from typing import Optional, List, Tuple
from copy import deepcopy


class PostAlign:
    def __init__(self, alignment: Alignment, threshold_ms: float):
        self.alignment = deepcopy(alignment)
        self.threshold_ms = threshold_ms

    def postalign(self) -> Alignment:
        i = 0
        while i < len(self.alignment):
            el_p = self.alignment[i]["p"]
            el_s = self.alignment[i]["s"]

            next_indices = self._get_threshold_range(i)

            incr_i = True

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
                # the func returns True if the gap is merged.
                # if it is fixed we need to NOT increment i--if two gaps are merged we need to
                # look at the current index again. if the score notes are swapped we still need to look
                # at the current one again.
                incr_i = not self._fix_gap_el_s(el_s, i)

            if incr_i:
                i += 1
        return self.alignment

    def _fix_gap_el_s(
        self,
        el_s: NoteInfo,
        i: int,
    ) -> bool:
        """
        el_s has a gap score note. Try to fix it.

        Return True if fixed
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
                        return True
            elif cand_el_p is not None:
                # cand_el["s"] is a gap
                # check if the note matches
                if cand_el_p["midi_note_num"] == el_s["midi_note_num"]:
                    # match, now we need to merge them
                    self.alignment[j]["s"] = deepcopy(el_s)
                    del self.alignment[i : i + 1]
                    return True
        return False

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
            if cand_el_p is not None and cand_el_s is not None:
                if cand_el_s["midi_note_num"] != cand_el_p["midi_note_num"]:
                    # mismatch--check if cand_el_s matches ours
                    if cand_el_s["midi_note_num"] == el_p["midi_note_num"]:
                        self._swap_score_note(i, j)
                        return
            elif cand_el_s is not None:
                # cand_el["p"] is a gap
                # check if the note matches
                if cand_el_s["midi_note_num"] == el_p["midi_note_num"]:
                    # match, now we need to merge them
                    self.alignment[i]["s"] = deepcopy(cand_el_s)
                    del self.alignment[j : j + 1]
                    return
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
            if cand_el_p is not None and cand_el_s is not None:
                if cand_el_s["midi_note_num"] != cand_el_p["midi_note_num"]:
                    # mismatch too--check if cand_el_s matches ours
                    if cand_el_s["midi_note_num"] == el_p["midi_note_num"]:
                        self._swap_score_note(i, j)
                        return
            elif cand_el_s is not None:
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

        for j in range(i + 1, len(self.alignment)):
            cand = self.alignment[j]
            if cand["s"] is not None:
                if abs(cand["s"]["note_start"] - curr_score_time) > self.threshold_ms:
                    break
            next_indices.append(j)

        return next_indices

    def _swap_score_note(self, i: int, j: int):
        self.alignment[i]["s"], self.alignment[j]["s"] = (
            self.alignment[j]["s"],
            self.alignment[i]["s"],
        )


class MismatchFixer:
    def __init__(self, alignment: Alignment, threshold_ms: float):
        self.alignment = deepcopy(alignment)
        self.threshold_ms = threshold_ms

    def fix_mismatches(self) -> Alignment:
        """
        Fix mismatches that have opposite succeeding mismatches.
        Common in parallel notes - the performance score does not guarantee the order
        is correct as specified in the score.

        First finds (backwards to make sure the closest mismatch always takes priority)
        a performance note that has a mismatch.
        Check if there is a succeeding mismatch that is the opposite of the current mismatch.

        Look up to threshold_ms in performance time.
        """
        # walk backwards so we always do it with the closest mismatch
        for i in range(len(self.alignment) - 1, -1, -1):
            el = self.alignment[i]
            if (
                el["p"] is not None
                and el["s"] is not None
                and el["p"]["midi_note_num"] != el["s"]["midi_note_num"]
            ):
                # mismatch
                p = el["p"]
                s = el["s"]
                score_time = s["note_start"]
                for j in range(i + 1, len(self.alignment)):
                    cand = self.alignment[j]
                    if cand["s"] is not None:
                        # break out if we're too far away
                        s_cand = cand["s"]
                        if s_cand["note_start"] - score_time > self.threshold_ms:
                            break
                        if cand["p"] is not None:
                            p_cand = cand["p"]
                            if (
                                p["midi_note_num"] == s_cand["midi_note_num"]
                                and s["midi_note_num"] == p_cand["midi_note_num"]
                            ):
                                # opposite mismatch, swap the score note
                                self.alignment[i]["s"], self.alignment[j]["s"] = (
                                    self.alignment[j]["s"],
                                    self.alignment[i]["s"],
                                )

        return self.alignment


class GapFixer:
    def __init__(self, alignment: Alignment, threshold_ms: float):
        self.alignment = deepcopy(alignment)
        self.threshold_ms = threshold_ms

    def fix_gaps(self) -> Alignment:
        """
        Fix gaps that have matching notes but separated by other matched notes.
        Common in parallel notes - the performance score does not guarantee the order
        is correct as specified in the score.

        First finds a performance note that has a gap score note.
        Check if there is a preceding/succeeding gap that matches the note in the reference score.

        Look up to threshold_ms in performance time.
        """
        i = 0
        while i < len(self.alignment):
            el = self.alignment[i]
            if el["p"] is not None and el["s"] is None:
                el_p = el["p"]

                found_match = False
                preceding_timestamp: Optional[float] = None

                # walk backwards
                for j in range(i - 1, -1, -1):
                    cand_el = self.alignment[j]

                    cand_p = cand_el["p"]
                    cand_s = cand_el["s"]

                    if cand_s is not None:
                        # make sure not too far off in score
                        if preceding_timestamp is None:
                            preceding_timestamp = cand_s["note_start"]
                        else:
                            if (
                                abs(preceding_timestamp - cand_s["note_start"])
                                > self.threshold_ms
                            ):
                                break

                        if cand_p is None:
                            # found gap in P
                            if cand_s["midi_note_num"] == el_p["midi_note_num"]:
                                self.alignment[i]["s"] = deepcopy(cand_s)

                                found_match = True
                                i -= 1
                                del self.alignment[j : j + 1]
                                break

                if not found_match:
                    # walk forwards, not found backwards
                    succeeding_timestamp: Optional[float] = None
                    for j in range(i + 1, len(self.alignment)):
                        cand_el = self.alignment[j]

                        cand_p = cand_el["p"]
                        cand_s = cand_el["s"]

                        if cand_s is not None:
                            # make sure not too far off in score
                            if succeeding_timestamp is None:
                                succeeding_timestamp = cand_s["note_start"]
                            else:
                                if (
                                    abs(succeeding_timestamp - cand_s["note_start"])
                                    > self.threshold_ms
                                ):
                                    break

                            if cand_p is None:
                                # found gap in P
                                if cand_s["midi_note_num"] == el_p["midi_note_num"]:
                                    self.alignment[i]["s"] = deepcopy(cand_s)

                                    found_match = True
                                    del self.alignment[j : j + 1]
                                    break

            i += 1
        return self.alignment
