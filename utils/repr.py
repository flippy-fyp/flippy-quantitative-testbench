from typing import List, Tuple
from utils.sharedtypes import NoteInfo, Alignment


def alignment_repr(alignment: Alignment) -> Tuple[str, str]:
    stdout = ""
    stderr = ""

    num_mismatches = 0
    num_pgaps = 0
    num_sgaps = 0

    for al in alignment:
        p = al["p"]
        s = al["s"]

        if p is None and s is None:
            raise ValueError("Alignment invalid: p and s both None!")

        if p is not None and s is not None:
            if p["midi_note_num"] == s["midi_note_num"]:
                # match
                stdout += f'{round(p["note_start"])} {round(s["note_start"])} {p["midi_note_num"]}\n'
            else:
                # mismatch
                num_mismatches += 1
                stdout += f'// MISMATCH: {round(p["note_start"])} {p["midi_note_num"]} - {round(s["note_start"])} {s["midi_note_num"]}\n'

        if p is None and s is not None:
            # gap in performance
            num_pgaps += 1
            stdout += f'// GAP: GAP - {round(s["note_start"])} {s["midi_note_num"]}\n'
        if p is not None and s is None:
            # gap in score
            num_sgaps += 1
            stdout += f'// GAP: {round(p["note_start"])} {p["midi_note_num"]} - GAP\n'

    stderr += f"Length of alignment: {len(alignment)}\n"
    stderr += f"Total number of gaps in performance: {num_pgaps}\n"
    stderr += f"Total number of gaps in score: {num_sgaps}\n"
    stderr += f"Total number of mismatches: {num_mismatches}\n"

    return (stdout, stderr)


def noteinfos_repr(ns: List[NoteInfo]) -> str:
    return "\n".join([f'{round(n["note_start"])} {n["midi_note_num"]}' for n in ns])
