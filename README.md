# Flippy Quantitative Testbench

(Real-time) Musical Score Audio Alignment (Score-following) Testbench and utilities.

### Requirements
- Python 3
- Requirements: `pip install -r requirements.txt`

# Testbench

#### Usage help
```bash
python testbench.py -h
```

#### Typical usage
```bash
python testbench.py --align <ALIGNMENT_OUTPUT> --ref <REFERENCE_RESULT_FILE>
```

#### File formats
- `<ALIGNMENT_OUTPUT>`: Four columns each line, see `utils.sharedtypes.py::FollowerOutputLine`.
- `<REFERENCE_RESULT_FILE>`: Three columns each line, see `utils.sharedtypes.py::RefFileLine`.

#### Sample Usage
```bash
$ python testbench.py --align ./data/sample_txt/sample_scofo.txt --ref ./data/sample_txt/sample_ref.txt
{
    "miss_rate": 0.0,
    "misalign_rate": 0.0,
    "piece_completion": 1.0,
    "std_of_error": 0.0,
    "mean_absolute_error": 0.10000000000000009,
    "std_of_latency": 1.1102230246251565e-16,
    "mean_latency": 0.09999999999999998,
    "std_of_offset": 1.1102230246251565e-16,
    "mean_absolute_offset": 0.20000000000000007
}
```

# ASM Score-Aligner
Produces testbench reference data from performance and reference scores. Uses a variation of the Needleman-Wunsch algorithm for optimal global alignment. The output follows the `<REFERENCE_RESULT_FILE>` format as per `utils.sharedtypes.py::RefFileLine`. Mismatches and gaps are reported as in the Sample Usage example below.

#### Usage help
```bash
python align.py -h
```

#### Sample Usage
```bash
$ python align.py --pscore ./data/sample_txt/sample_pscore.txt --rscore ./data/sample_txt/sample_rscore.txt
Running PostAlign with threshold 0
10 100 0
// GAP: 20 1 - GAP
30 200 2
// GAP: GAP - 300 3
40 400 3
// MISMATCH: 50 0 - 500 2
60 600 1
// MISMATCH: 70 4 - 700 2

Length of alignment: 8
Total number of gaps in performance: 1
Total number of gaps in score: 1
Total number of mismatches: 2
```
Note that the first and last four lines (logs) are output to `stderr` and that other lines (actual alignment result) are output to `stdout`.

# Converters
## MIDI to Score Converter
#### Usage help
```bash
python midi.py -h
```
#### Typical usage
```bash
python midi.py --input <MIDI_PATH>
```

#### Output Score Format
Two columns each line representing note start time (ms, float) and MIDI note number respectively.

#### Sample Usage
```bash
$ python midi.py --input ./data/sample_midis/short_demo.mid
5 60
515 62
1010 64
1506 64
1506 67
```

## MusicXML to MIDI/Score Converter

#### Usage help
```bash
python musicxml.py
```

## Score to MIDI Converter
#### Usage help
```bash
python score.py -h
```


## Reference Score to MIDI Converter
#### Usage help
```bash
python refscore .py -h
```

## Results Reproduction

These scripts reproduce results shown in [project report](https://github.com/flippy-fyp/flippy-report/blob/main/main.pdf).

To run everything:
```bash
python repro.py
```

### Bach10 Dataset for ASM Alignment Benchmarking
```bash
python repro.py bach10
```

Produces output in `data/bach10/output-<TIME>`.

### BWV846 Dataset for ASM Alignment Benchmarking
```bash
python repro.py bwv846
```

Logs will indicate where artifacts are stored.

Alternatively, see commands to run in `data/bwv846/script.txt`.
# Contributing

### Run unit tests
```bash
python -m unittest
```

# References

Testbench written based on the [MIREX Score Following](https://www.music-ir.org/mirex/wiki/2006:Score_Following_Proposal) standards and [jthickstun's alignment evaluation implementation](https://github.com/jthickstun/alignment-eval).

See Part II of the [project report](https://github.com/flippy-fyp/flippy-report/blob/main/main.pdf) for more information.

<!-- ### Differences from MIREX evaluation
- Uses fourth column of alignment output to uniquely identify notes instead of an ID--hence, the fourth column is mandatory instead of optional as in MIREX -->
