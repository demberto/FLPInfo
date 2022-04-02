![Powered by: PyFLP](https://img.shields.io/badge/powered%20by-PyFLP-blue)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/demberto/flpinfo/main)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flpinfo)
![PyPI](https://img.shields.io/pypi/v/flpinfo)
![PyPI - Status](https://img.shields.io/pypi/status/flpinfo)
![PyPI - License](https://img.shields.io/pypi/l/flpinfo)
![Lines of code](https://img.shields.io/tokei/lines/github/demberto/flpinfo)
![Code Style: Black](https://img.shields.io/badge/code%20style-black-black)

# FLPInfo

> Prints basic information about an FL Studio project file (.flp).

## ▶ Usage

```
>>> flpinfo <path_to_flp>

Title:            My FLP, My Song
Artist(s):        Who else than me?
Genre:            Unique
Tempo (BPM):      420.0
Project URL:      https://google.com
FL Version:       21.0.0.6969
Channel(s):       10 [Piano, Lead, Chord, ...]
Arrangement(s):   1 [Arrangement]
Pattern(s):       2 [Clap, Hats]
```

## 💲 Command-line options

```
flpinfo [-h] [-v] [--no-color] flp

positional arguments:
  flp     The location of FLP to show information about. Zipped FLPs are not yet supported.

optional arguments:
  -h, --help     show this help message and exit
  --full-lists   Lists will not appear truncated.
  --no-color     Disables colored output
```

## 🚀 TODO

- Long comments cause incorrect formatting
- Zipped FLPs

## 📜 License

FLPInfo is licensed under the [GNU Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html).
