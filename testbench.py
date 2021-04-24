import argparse
import json
from utils.bench import bench

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
        "--misalign_threshold",
        type=int,
        help="Misalign threshold in ms",
        default=300,
    )

    args = parser.parse_args()
    align_path = args.align
    ref_path = args.ref

    res = bench(align_path, ref_path)

    res_str = json.dumps(res, indent=4)

    print(res_str)
