from processfile import FollowerOutputLine, RefFileLine
from typing import List, Tuple, Dict, TypedDict
import numpy as np

# Misaligned notes are events in the score that are recognized but are
# too far (regarding a given threshold θe, e.g. 300 ms) from
# the reference alignment to be considered correct.
MISALIGN_THRESHOLD_MS = 300


class MatchResult(TypedDict):
    miss_rate: float  # percentage of missed score events
    misalign_rate: float  # percentage of misaligned events with absolute error > MISALIGN_THRESHOLD_MS
    piece_completion: float  # percentage of events followed until follower hangs
    average_latency: float  # for non-misaligned events: shows the over measure of latency of the system
    average_absolute_offset: float  # for non-misaligned events: shows the reactivity of the follower
    variance_of_error: float  # for non-misaligned events: shows the imprecision or spread of the alignment error
    average_imprecision: float  # for non-misaligned events: shows the global imprecision
    precision_rate: float  # percentage of correctly detected notes


def match(
    scofo_output: List[FollowerOutputLine],
    ref: List[RefFileLine],
) -> MatchResult:
    num_misaligned = 0

    # for non-misaligned events
    errors: List[float] = []
    non_misaligned_errors: List[float] = []
    latencies: List[float] = []
    offsets: List[float] = []

    last_aligned_event_index = 0

    ref_p = preprocess_ref(ref)

    for x in scofo_output:
        t = (x["note_start"], x["midi_note_num"])

        if t not in ref_p:
            # reporting events not in the score should not be possible--ignoring here
            continue

        tru_time, idx = ref_p[t]

        # error is defined as the time lapse between the alignment positions of corresponding events in
        # the reference and the estimated alignment time
        # t_e - t_r
        error = x["est_time"] - tru_time
        errors.append(error)
        if abs(error) > MISALIGN_THRESHOLD_MS:
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

    res: MatchResult = {
        "miss_rate": safe_div((float(len(ref)) - len(errors)), len(ref)),
        "misalign_rate": safe_div(float(num_misaligned), len(ref)),
        "piece_completion": safe_div(float(last_aligned_event_index), len(ref)),
        "average_latency": safe_div(float(sum(latencies)), len(latencies)),
        "average_absolute_offset": safe_div(
            float(sum(abs(o) for o in offsets)), len(offsets)
        ),
        "variance_of_error": safe_var(non_misaligned_errors),
        "average_imprecision": safe_div(
            float(sum(abs(e) for e in non_misaligned_errors)),
            len(non_misaligned_errors),
        ),
        "precision_rate": safe_div(len(non_misaligned_errors), len(ref)),
    }
    return res


def safe_div(a: float, b: int) -> float:
    # return 0 if denominator is 0
    if b == 0:
        return 0.0
    return a / b


def safe_var(l: List[float]) -> float:
    # return 0 if empty list
    if len(l) == 0:
        return 0.0
    return np.var(l)


def preprocess_ref(ls: List[RefFileLine]) -> Dict[Tuple[float, int], Tuple[float, int]]:
    """
    gets a map from the note_start and midi_note_num dict to the tru_time and index
    """
    return {
        (ls[i]["note_start"], ls[i]["midi_note_num"]): (ls[i]["tru_time"], i)
        for i in range(len(ls))
    }