from typing import NewType, List, Tuple, TypedDict


class FollowerOutputLine(TypedDict):
    est_time: int  # 1. estimated note onset time in performance audio file (ms)
    det_time: int  # 2. detection time relative to performance audio file (ms)
    note_start: int  # 3. note start time in score (ms)


def process_file(input_file_path: str) -> List[FollowerOutputLine]:
    f = open(input_file_path)
    t = f.read()
    return process_text(t)


def process_text(text: str) -> List[FollowerOutputLine]:
    def process_line(line: str) -> FollowerOutputLine:
        ls = line.split()
        if len(ls) < 3:
            raise ValueError(f"Too few entries on line: {line}")
        i = list(map(int, ls))
        return {
            "est_time": i[0],
            "det_time": i[1],
            "note_start": i[2],
        }

    return list(map(process_line, text.splitlines()))
