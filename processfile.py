from typing import NewType, List, Tuple, TypedDict
from sharedtypes import RefFileLine, NoteInfo, FollowerOutputLine


def process_input_file(input_file_path: str) -> List[FollowerOutputLine]:
    f = open(input_file_path)
    t = f.read().strip()
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
    t = f.read().strip()
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


def process_score_file(score_file_path: str) -> List[NoteInfo]:
    f = open(score_file_path)
    t = f.read().strip()
    return process_score_text(t)


def process_score_text(text: str) -> List[NoteInfo]:
    def process_line(line: str) -> NoteInfo:
        ls = line.split()
        if len(ls) < 2:
            raise ValueError(f"Too few entries on line: {line}")
        return {"note_start": float(ls[0]), "midi_note_num": int(ls[1])}

    return list(map(process_line, text.splitlines()))
