# Introduction

This repository is built to provide an easy object-oriented interface for muselsl for use in hackathons, personal projects, etc..

See these files in the src folder


Additionally, several python files in the root folder and serve as live examples as part of
a DSP and Gesture Recognition workshop that I instruct.

## Code Sources

This project relies on BlueMuse:

https://github.com/kowalej/BlueMuse.git

and muselsl:

https://github.com/alexandrebarachant/muse-lsl.git

 ```
 @misc{muse-lsl,
  author       = {Alexandre Barachant and
                  Dano Morrison and
                  Hubert Banville and
                  Jason Kowaleski and
                  Uri Shaked and
                  Sylvain Chevallier and
                  Juan Jesús Torre Tresols},
  title        = {muse-lsl},
  month        = may,
  year         = 2019,
  doi          = {10.5281/zenodo.3228861},
  url          = {https://doi.org/10.5281/zenodo.3228861}
}
 
 ```

## Installation

All this examples assume a working BlueMuse connection on a windows pc.

download the required python packages with:

 `pip install -r requirements.txt`
 
run file [MuseReaderSlidesExamples.py](MuseReaderSlidesExamples.py) without modifications and with a working BlueMuse connection to see the setup is working.

## Usage

[MuseReaderSlidesExamples.py](MuseReaderSlidesExamples.py) has various documented examples on how to use this package. change the function being called at the end of the file for different examples