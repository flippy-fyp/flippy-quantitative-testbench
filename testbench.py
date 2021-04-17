import argparse
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

    args = parser.parse_args()
    align_path = args.align
    ref_path = args.ref

    print(bench(align_path, ref_path))
