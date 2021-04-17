import json
from .processfile import process_follower_input_file, process_ref_file
from .match import match


def bench(align_path: str, ref_path: str) -> str:
    scofo_output = process_follower_input_file(align_path)
    ref_contents = process_ref_file(ref_path)

    res = match(scofo_output, ref_contents)
    res_str = json.dumps(res, indent=4)

    return res_str
