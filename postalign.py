from sharedtypes import Alignment
from typing import Optional, List
from copy import deepcopy


class MismatchFixer:
    def __init__(self, alignment: Alignment, threshold_ms: float):
        self.alignment = deepcopy(alignment)
        self.threshold_ms = threshold_ms

    def fix_mismatches(self) -> Alignment:
        """
        Fix mismatches that have opposite succeeding mismatches.
        Common in parallel notes - the performance score does not guarantee the order
        is correct as specified in the score.

        First finds a performance note that has a mismatch.
        Check if there is a succeeding mismatch that is the opposite of the current mismatch.

        Look up to threshold_ms in score time.

        WARNING: If you intend to run both MismatchFixer and GapFixer, the former needs
        to run first! This is because MismatchFixer depends on score note timings to be ascending.
        GapFixer _may_ perturb the sequence of score note timings.
        """
        for i in range(len(self.alignment)):
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

        Look up to threshold_ms in score time.
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
