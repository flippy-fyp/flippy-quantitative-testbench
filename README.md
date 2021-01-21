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
- `<ALIGNMENT_OUTPUT>`: Four columns each line, see `sharedtypes.py::FollowerOutputLine`.
- `<REFERENCE_RESULT_FILE>`: Three columns each line, see `sharedtypes.py::RefFileLine`.

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
Produces testbench reference data from performance and reference scores. Uses a variation of the Needleman-Wunsch algorithm for optimal global alignment. The output follows the `<REFERENCE_RESULT_FILE>` format as per `sharedtypes.py::RefFileLine`. Mismatches and gaps are reported as in the Sample Usage example below.

#### Usage help
```bash
python align.py -h
```

#### Sample Usage
```bash
$ python align.py --pscore ./data/sample_txt/sample_pscore.txt --rscore ./data/sample_txt/sample_rscore.txt
Running PostAlign with threshold 0
10.000 100.000 0
// GAP: 20.000 1 - GAP
30.000 200.000 2
// GAP: GAP - 300.000 3
40.000 400.000 3
// MISMATCH: 50.000 0 - 500.000 2
60.000 600.000 1
// MISMATCH: 70.000 4 - 700.000 2

Length of alignment: 8
Total number of gaps in performance: 1
Total number of gaps in score: 1
Total number of mismatches: 2
```
Note that the first and last four lines are output to `stderr` and that other lines are output to `stdout`.

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

#### Sample Usage
```bash
$ python musicxml.py --input ./data/sample_musicxmls/prelude.mxl        
0.0 60
208.33325 64
416.6665 67
624.99975 72
833.333 76
1041.66625 67
1249.9995 72
1458.33275 76
...
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

# Scripts

### Bach10 Dataset for ASM Alignment Benchmarking
Requires [Bach10 dataset v1.1](http://www2.ece.rochester.edu/projects/air/resource.html) in `data/bach10/Bach10_v1.1`.

```bash
python script_bach10.py
```

Produces output in `data/bach10/output-<TIME>`.

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
