import json
from .processfile import process_follower_input_file, process_ref_file
from .match import MISALIGN_THRESHOLD_MS_DEFAULT, MatchResult, match


def bench(
    align_path: str,
    ref_path: str,
    misalign_threshold_ms: int = MISALIGN_THRESHOLD_MS_DEFAULT,
) -> MatchResult:
    scofo_output = process_follower_input_file(align_path)
    ref_contents = process_ref_file(ref_path)
    res = match(scofo_output, ref_contents, misalign_threshold_ms)
    return res
