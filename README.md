# Flippy Testbench

(Real-time) Musical Score Audio Alignment (Score-following) Testbench.

Written based on the [MIREX Score Following](https://www.music-ir.org/mirex/wiki/2006:Score_Following_Proposal) standards.

Read the [paper](./docs/ISMIR2007_p315_cont.pdf).

## Usage

### Setup
Requirements: Python 3
```bash
pip install -r requirements.txt
```

### Usage help
```bash
python testbench.py -h
```

### Typical usage
```bash
python testbench.py --input <ALIGNMENT_OUTPUT> --ref <REFERENCE_RESULT_FILE> (--output <OUTPUT_RESULT_FILE_PATH>)
```

### File formats 
- `<ALIGNMENT_OUTPUT>`: Four columns each line, see `processfile.py::FollowerOutputLine`.
- `<REFERENCE_RESULT_FILE>`: Three columns each line, see `processfile.py::RefFileLine`.

### Unit Tests 
```bash
python -m unittest
```