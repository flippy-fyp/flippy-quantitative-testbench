# Flippy Quantitative Testbench

(Real-time) Musical Score Audio Alignment (Score-following) Testbench and utilities.

### Requirements
- Cloned repository with all submodules
```bash
git clone <REPO_URL> --recurse-submodules
```
- Python 3 (Tested on Python 3.8, Ubuntu 20.04)

## Setup
- Requirements: `pip install -r requirements.txt`
- Initialise pre-commit: `pre-commit install`

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
    "mean_absolute_offset": 0.20000000000000007,
    "miss_num": 0,
    "misalign_num": 0,
    "total_num": 2,
    "precision_rate": 1.0
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
10.0 100.0 0
// GAP: 20.0 1 - GAP
30.0 200.0 2
// GAP: GAP - 300.0 3
40.0 400.0 3
// MISMATCH: 50.0 0 - 500.0 2
60.0 600.0 1
// MISMATCH: 70.0 4 - 700.0 2

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
4.882802734375 60
514.6474082031249 62
1010.2518857421874 64
1505.8563632812497 64
1505.8563632812497 67
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

Note that the first column of the Reference Score (i.e. the true note onset time) is used as the MIDI onset.

# Results Reproduction

These scripts reproduce results shown in the [project report](https://arxiv.org/abs/2205.03247).

To run everything:
```bash
python repro.py
```

## Bach10 Dataset for ASM Alignment Benchmarking
```bash
python repro.py bach10
```

Produces output in `data/bach10/output-<TIME>`.

## BWV846 Dataset for ASM Alignment Benchmarking
```bash
python repro.py bwv846
```

Logs will indicate where artifacts are stored.

Alternatively, see commands to run in `data/bwv846/script.txt`.

# References

Testbench written based on the [MIREX Score Following](https://www.music-ir.org/mirex/wiki/2006:Score_Following_Proposal) standards and [jthickstun's alignment evaluation implementation](https://github.com/jthickstun/alignment-eval).

See Part II of the [project report](https://arxiv.org/abs/2205.03247) for more information.

<!-- ### Differences from MIREX evaluation
- Uses fourth column of alignment output to uniquely identify notes instead of an ID--hence, the fourth column is mandatory instead of optional as in MIREX -->


# Contributing

* File bugs and/or feature requests in the [GitHub repository](https://github.com/flippy/flippy-quantitative-testbench)
* Pull requests are welcome in the [GitHub repository](https://github.com/flippy/flippy-quantitative-testbench)
* Buy me a Coffee ☕️ via [PayPal](https://paypal.me/lhl2617)

# Citing

## BibTeX
```
@misc{https://doi.org/10.48550/arxiv.2205.03247,
  doi = {10.48550/ARXIV.2205.03247},
  url = {https://arxiv.org/abs/2205.03247},
  author = {Lee, Lin Hao},
  keywords = {Sound (cs.SD), Audio and Speech Processing (eess.AS), FOS: Computer and information sciences, FOS: Computer and information sciences, FOS: Electrical engineering, electronic engineering, information engineering, FOS: Electrical engineering, electronic engineering, information engineering},
  title = {Musical Score Following and Audio Alignment},
  publisher = {arXiv},
  year = {2022},
  copyright = {Creative Commons Attribution 4.0 International}
}
```
