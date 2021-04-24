from .processfile import FollowerOutputLine, RefFileLine
from typing import Iterator, List, NewType, Optional, TypedDict, Tuple, Dict
import numpy as np  # type: ignore
from sortedcontainers import SortedDict  # type: ignore


PreprocessedRef = NewType(  # type: ignore
    "PreprocessedRef", "SortedDict[float, Dict[float, Tuple[float, int]]]"
)

# Misaligned notes are events in the score that are recognized but are
# too far (regarding a given threshold θe, e.g. 300 ms) from
# the reference alignment to be considered correct.
MISALIGN_THRESHOLD_MS_DEFAULT = 300


class MatchResult(TypedDict):
    miss_rate: float  # percentage of missed score events
    misalign_rate: float  # percentage of misaligned events with absolute error > misalign_threshold_ms
    piece_completion: float  # percentage of events followed until follower hangs

    # for non-misaligned events
    std_of_error: float
    mean_absolute_error: float
    std_of_latency: float
    mean_latency: float
    std_of_offset: float
    mean_absolute_offset: float

    miss_num: int  # number of missed score events
    misalign_num: int  # number of misaligned score events
    total_num: int  # total number of score events
    precision_rate: float  # 1 - miss_rate - misalign_rate


def match(
    scofo_output: List[FollowerOutputLine],
    ref: List[RefFileLine],
    misalign_threshold_ms: int = MISALIGN_THRESHOLD_MS_DEFAULT,
) -> MatchResult:
    num_misaligned = 0

    errors: List[float] = []
    non_misaligned_errors: List[float] = []

    # for non-misaligned events
    latencies: List[float] = []
    offsets: List[float] = []

    last_aligned_event_index = 0

    ref_p = preprocess_ref(ref)

    for x in scofo_output:
        candidate_note = get_note_from_ref(x["note_start"], x["midi_note_num"], ref_p)
        if candidate_note is None:
            # reporting events not in the score should not be possible--ignoring here
            # ref may also not contain all notes -- give the follower the benefit of the doubt
            continue

        tru_time, idx = candidate_note

        # error is defined as the time lapse between the alignment positions of corresponding events in
        # the reference and the estimated alignment time
        # t_e - t_r
        error = x["est_time"] - tru_time
        errors.append(error)
        if abs(error) > misalign_threshold_ms:
            num_misaligned += 1
            continue

        non_misaligned_errors.append(error)
        last_aligned_event_index = idx

        # latency of a detection is the difference between the time a detection is made
        # and the estimated note onset time
        # t_d - t_e > 0
        latency = x["det_time"] - x["est_time"]
        latencies.append(latency)

        # offset is the lag between the time the event occurred and the reporting of the detection
        # t_d - t_r
        offset = x["det_time"] - tru_time
        offsets.append(offset)

    last_aligned_event_index = (
        last_aligned_event_index + 1 if len(non_misaligned_errors) > 0 else 0
    )
    total_num = len(ref)
    miss_num = len(ref) - len(errors)
    miss_rate = safe_div(float(miss_num), total_num)
    misalign_rate = safe_div(float(num_misaligned), total_num)
    precision_rate = 1.0 - miss_rate - misalign_rate

    res: MatchResult = {
        "miss_rate": miss_rate,
        "misalign_rate": misalign_rate,
        "piece_completion": safe_div(float(last_aligned_event_index), len(ref)),
        "std_of_error": safe_std(non_misaligned_errors),
        "mean_absolute_error": mean_abs(non_misaligned_errors),
        "std_of_latency": safe_std(latencies),
        "mean_latency": mean(latencies),
        "std_of_offset": safe_std(offsets),
        "mean_absolute_offset": mean_abs(offsets),
        "miss_num": miss_num,
        "misalign_num": num_misaligned,
        "total_num": total_num,
        "precision_rate": precision_rate,
    }
    return res


def mean(l: List[float]) -> float:
    return safe_div(sum(l), len(l))


def mean_abs(l: List[float]) -> float:
    return safe_div(float(sum(abs(x) for x in l)), len(l))


def safe_div(a: float, b: int) -> float:
    # return 0 if denominator is 0
    if b == 0:
        return 0.0
    return a / b


def safe_std(l: List[float]) -> float:
    # return 0 if empty list
    if len(l) == 0:
        return 0.0
    return float(np.std(l))


def preprocess_ref(ls: List[RefFileLine]) -> PreprocessedRef:
    """
    Gets a SortedDict mapping from note_start to midi_note_num to tru_time and index
    """
    res: PreprocessedRef = SortedDict()

    for i in range(len(ls)):
        l = ls[i]
        if l["note_start"] not in res:
            res[l["note_start"]] = {}
        res[l["note_start"]][l["midi_note_num"]] = (l["tru_time"], i)

    return res


def get_note_from_ref(
    note_start: float, midi_note_num: int, ref: PreprocessedRef, bound_ms: float = 1.0
) -> Optional[Tuple[float, int]]:
    """
    Returns the tru_time and index of the note if found exactly or within a certain bound neighbouring the ref.
    """
    # Short path: found exactly
    if note_start in ref and midi_note_num in ref:
        return ref[note_start][midi_note_num]

    # Long path: find within the bounds
    closest_note_start_after_generator: Iterator[float] = ref.irange(
        minimum=note_start - bound_ms,
    )

    n = next(closest_note_start_after_generator, None)
    while n is not None:
        if abs(n - note_start) > bound_ms:
            return None
        if midi_note_num in ref[n]:
            return ref[n][midi_note_num]

        n = next(closest_note_start_after_generator, None)
    return None
