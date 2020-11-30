# Flippy Testbench

(Real-time) Musical Score Audio Alignment (Score-following) Testbench and MIDI-to-Score Creation Tool.

Written based on the [MIREX Score Following](https://www.music-ir.org/mirex/wiki/2006:Score_Following_Proposal) standards.

Read the [paper](./docs/ISMIR2007_p315_cont.pdf).


## Differences from MIREX evaluation
- Uses fourth column of alignment output to uniquely identify notes instead of an ID--hence, the fourth column is mandatory instead of optional as in MIREX

## Usage
### Requirements
- Python 3
- Requirements: `pip install -r requirements.txt`

### Testbench

#### Usage help
```bash
python testbench.py -h
```

#### Typical usage
```bash
python testbench.py --align <ALIGNMENT_OUTPUT> --ref <REFERENCE_RESULT_FILE>
```

#### File formats 
- `<ALIGNMENT_OUTPUT>`: Four columns each line, see `processfile.py::FollowerOutputLine`.
- `<REFERENCE_RESULT_FILE>`: Three columns each line, see `processfile.py::RefFileLine`.

#### Sample Usage
```bash
$ python testbench.py --align ./samples/sample_scofo.txt --ref ./samples/sample_ref.txt
{
    "miss_rate": 0.0,
    "misalign_rate": 0.0,
    "piece_completion": 1.0,
    "average_latency": 0.09999999999999998,
    "average_absolute_offset": 0.20000000000000007,
    "variance_of_error": 0.0,
    "average_imprecision": 0.10000000000000009,
    "precision_rate": 1.0
}
```

### MIDI-To-Score Creation Tool

#### Usage help
```bash
python midi.py -h
```
#### Typical usage
```bash
python midi.py --midi <MIDI_PATH>
```

#### Output Score Format
Two columns each line representing note start time (ms, float) and MIDI note number respectively.

#### Sample Usage
```bash
$ python midi.py --midi ./sample_midis/short_demo.mid
4.882802734375 60
514.6474082031249 62
1010.2518857421874 64
1505.8563632812497 64
1505.8563632812497 67
```

## Contributing

### Run unit tests
```bash
python -m unittest
```