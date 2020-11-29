from typing import NewType, List, Tuple, TypedDict


# https://www.music-ir.org/mirex/wiki/2018:Real-time_Audio_to_Score_Alignment_(a.k.a_Score_Following)
class FollowerOutputLine(TypedDict):
    est_time: float  # 1. estimated note onset time in performance audio file (ms)
    det_time: float  # 2. detection time relative to performance audio file (ms)
    note_start: float  # 3. note start time in score (ms)
    midi_note_num: int  # 4. MIDI note number in score (int)


class RefFileLine(TypedDict):
    tru_time: float  # true note onset time in performance audio file (ms)
    note_start: float  # note start time in score (ms)
    midi_note_num: int  # MIDI note number in score (int)


def process_input_file(input_file_path: str) -> List[FollowerOutputLine]:
    f = open(input_file_path)
    t = f.read()
    return process_input_text(t)


def process_input_text(text: str) -> List[FollowerOutputLine]:
    def process_line(line: str) -> FollowerOutputLine:
        ls = line.split()
        if len(ls) < 4:
            raise ValueError(f"Too few entries on line: {line}")
        return {
            "est_time": float(ls[0]),
            "det_time": float(ls[1]),
            "note_start": float(ls[2]),
            "midi_note_num": int(ls[3]),
        }

    return list(map(process_line, text.splitlines()))


def process_ref_file(ref_file_path: str) -> List[RefFileLine]:
    f = open(ref_file_path)
    t = f.read()
    return process_ref_text(t)


def process_ref_text(text: str) -> List[RefFileLine]:
    def process_line(line: str) -> RefFileLine:
        ls = line.split()
        if len(ls) < 3:
            raise ValueError(f"Too few entries on line: {line}")
        return {
            "tru_time": float(ls[0]),
            "note_start": float(ls[1]),
            "midi_note_num": int(ls[2]),
        }

    return list(map(process_line, text.splitlines()))
