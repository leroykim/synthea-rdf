# 🕸️ SYNTHEA RDF
[![KnAcc Lab](https://tinyurl.com/knacclogo)](https://knacc.umbc.edu/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)

Semantic web representation for the [Synthea<sup>TM</sup>](https://github.com/synthetichealth/synthea) and CSVs to Turtle (.ttl) conversion tool.

![synthea_ontology](synthea_ontology/synthea_ontology.png)

## :hammer: Usage
### Installation
```bash
pip install synthea-rdf
```

### Command Line Interface (CLI)
The bigger the data size, the more time that the data conversion needs. In this case, it would be better to use CLI in the background and check the progress time to time. The best way is to run the process in a [TMUX](https://github.com/tmux/tmux/wiki) session and detach it. It is possible to check the progress by attaching TMUX session.

CLI Example:
```bash
python3 conversion.py --include-dua --include-trustscore --ontology ~/synthea-rdf/synthea_ontology/synthea_ontology.ttl --csv-dir ~/synthea/output/1000k/csv --chunk-size 300000 
```

CLI Example with TMUX:
1. `$ tmux`
2. `$ python3 conversion.py --include-dua --include-trustscore --ontology ~/synthea-rdf/synthea_ontology/synthea_ontology.ttl --csv-dir ~/synthea/output/1000k/csv --chunk-size 300000`
3. Press `[CTRL]+[b]`, then `[d]` to detach the TMUX session.
4. Now it is okay to log off.
    > DO NOT SHUT DOWN THE MACHINE!!
5. `$ tmux a` to attach the session and check the progress

### Graphical User Interface (GUI)
There are user interfaces that ends with `_gui.py`.
- [Synthea CSV to RDF converter](synthea_converter_gui.py)
- [Trust score and Data Usage Agreement (DUA) generator](trustscore_dua_generator_gui.py)

```bash
python3 synthea_converter.py
```
![synthea_converter](synthea_ontology/synthea_converter.png)

```bash
python3 trustscore_dua_generator.py
```
![trustscore_dua_generator](synthea_ontology/trustscore_dua_generator.png)
