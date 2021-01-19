from typing import TypedDict, Optional, List


class NoteInfo(TypedDict):
    note_start: float  # note start time (ms)
    midi_note_num: int  # MIDI note number


class RefFileLine(TypedDict):
    tru_time: float  # true note onset time in performance audio file (ms)
    note_start: float  # note start time in score (ms)
    midi_note_num: int  # MIDI note number in score (int)


# https://www.music-ir.org/mirex/wiki/2018:Real-time_Audio_to_Score_Alignment_(a.k.a_Score_Following)
class FollowerOutputLine(TypedDict):
    est_time: float  # 1. estimated note onset time in performance audio file (ms)
    det_time: float  # 2. detection time relative to performance audio file (ms)
    note_start: float  # 3. note start time in score (ms)
    midi_note_num: int  # 4. MIDI note number in score (int)


class AlignmentElem(TypedDict):
    # if gap in either, value is None
    p: Optional[NoteInfo]  # note in performance
    s: Optional[NoteInfo]  # note in score


Alignment = List[AlignmentElem]
