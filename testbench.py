import argparse
import json
from processfile import process_input_file, process_ref_file
from match import match

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Testbench for score-following/alignment"
    )

    parser.add_argument(
        "--align", type=str, help="Input file of alignment output", required=True
    )
    parser.add_argument(
        "--ref", type=str, help="Path to reference result file", required=True
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file of testbench calculation",
        default="stdout",
    )

    args = parser.parse_args()
    inp = args.input
    ref = args.ref
    out = args.output

    scofo_output = process_input_file(inp)
    ref_contents = process_ref_file(ref)

    res = match(scofo_output, ref_contents)
    res_str = json.dumps(res, indent=4)

    if out == "stdout":
        print(res_str)
    else:
        f = open(out, "w")
        f.write(res_str)
        f.close()
