import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Testbench for score-following/alignment"
    )

    parser.add_argument(
        "--input", type=str, help="Input file of alignment output", required=True
    )
    parser.add_argument(
        "--reference", type=str, help="Path to reference result file", required=True
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file of testbench calculation",
        default="stdout",
    )

    args = parser.parse_args()
    input = args.input
    output = args.output
