# 🕸️ SYNTHEA RDF
[![KnAcc Lab](https://tinyurl.com/knacclogo)](https://knacc.umbc.edu/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)

Semantic web representation for the [Synthea<sup>TM</sup>](https://github.com/synthetichealth/synthea) and CSVs to Turtle (.ttl) conversion tool.

![synthea_ontology](synthea_ontology/synthea_ontology.png)


## :hammer: Installation
### Method 1: Poetry
[Poetry installation guide](https://python-poetry.org/docs/)
1. clone the repo
2. `python3 -m venv .venv`
3. `source .venv/bin/activate`
4. `poetry install`

:electric_plug: activate `.venv` environment everytime before using `synthea-rdf` by running `source .venv/bin/activate` command.

### Method 2: Pip
```bash
pip install synthea-rdf
```

## :zap: Usage
### Conversion
All conversion configurations should be specified in [`configuration.yaml`](configuration.yaml).

Here is a sample `configuration.yaml`.

```yaml
model_path: synthea_ontology/synthea_ontology.ttl
synthea_csv_path: ../synthea/output/1000k/csv
output_path: result/1000k
chunk_size: 300000
include_dua: True
include_trustscore: True
skip:
  - allergies.csv
  - careplans.csv
  - claims_transactions.csv
  - claims.csv
  - conditions.csv
  - devices.csv
  - encounters.csv
  - imaging_studies.csv
  - immunizations.csv
  - medications.csv
  - observations.csv
  - organizations.csv
  - patients.csv
  - patient_expenses.csv
  - payer_transitions.csv
do_shutdown: False
```

After specification, simply run:

```bash
python3 conversion.py
```

### Running conversion process with [TMUX](https://github.com/tmux/tmux/wiki)

The bigger the data size, the more time that the data conversion needs. In this case, it would be better to use CLI in the background and check the progress time to time. The best way is to run the process in a [TMUX](https://github.com/tmux/tmux/wiki) session and detach it. It is possible to check the progress by attaching the TMUX session.

Example:
1. `$ tmux`
2. `$ python3 conversion.py`
3. Press `[CTRL]+[b]`, then `[d]` to detach the TMUX session.
4. Now it is okay to log off. (:warning:DO NOT SHUT DOWN THE MACHINE!!)
5. `$ tmux a` to attach the session and check the progress

### Trust Score and DUA generation
Use [Trust score and Data Usage Agreement (DUA) generator](trustscore_dua_generator_gui.py) to generate optional `Trust Score` and `DUA` data.

```bash
python3 trustscore_dua_generator.py
```
![trustscore_dua_generator](synthea_ontology/trustscore_dua_generator.png)
