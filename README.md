# 🕸️ SYNTHEA RDF
[![KnAcc Lab](https://tinyurl.com/knacclogo)](https://knacc.umbc.edu/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)

Semantic web representation for the [Synthea<sup>TM</sup>](https://github.com/synthetichealth/synthea) and CSVs to Turtle (.ttl) conversion tool.

![synthea_ontology](synthea_ontology/synthea_ontology.png)

## :hammer: Usage
### Installation
```bash
pip install synthea-rdf
```

### Graphical User Interface
There are user interfaces in the `gui` directory:
- [Synthea CSV to RDF converter](gui/synthea_converter.py)
- [Trust score and Data Usage Agreement (DUA) generator](gui/trustscore_dua_generator.py)

```bash
python3 synthea_converter.py
```
![synthea_converter](synthea_ontology/synthea_converter.png)

```bash
python3 trustscore_dua_generator.py
```
![trustscore_dua_generator](synthea_ontology/trustscore_dua_generator.png)
