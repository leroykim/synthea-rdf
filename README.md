# 🕸️ SYNTHEA RDF
[![KnAcc Lab](https://tinyurl.com/knacclogo)](https://knacc.umbc.edu/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)

Semantic web representation for the [Synthea<sup>TM</sup>](https://github.com/synthetichealth/synthea) and CSVs to Turtle (.ttl) conversion tool.

![synthea_ontology](synthea_ontology/synthea_ontology.png)

> Synthea ontology and conversion method v1.0 are done.
> WIP minor fixes.

## :hammer: Usage
### Single CSV
```python
from from pathlib import Path
from synthea_rdf.graph import GraphBuilder

MODEL_PATH = "./synthea_ontology/synthea_ontology.ttl"
CSV_DIR = "./csv"
DEST_PATH = "./result"

builder = GraphBuilder(CSV_DIR, MODEL_PATH)
builder.convertEncounter()
builder.serialize(destination=Path(DEST_PATH)/"encounter.ttl")
```

### All CSV
```python
from pathlib import Path
from synthea_rdf.graph import GraphBuilder

MODEL_PATH = "./synthea_ontology/synthea_ontology.ttl"
CSV_DIR = "./csv"
DEST_PATH = "./result"

builder = GraphBuilder(CSV_DIR, MODEL_PATH)
graph = builder.build()
graph.serialize(destination=Path(DEST_PATH) / "all.ttl")
```

## :warning: Issues
- [ ] Confusing naming convention for the following data properties:

        - syn:start
        - syn:startDate
        - syn:startDateTime
        - syn:date
        - syn:dateTime

- [ ] There are no `Allergy` and `ImagingStudy` data in the test dataset. Testing required with a larger dataset.
    - [ ] Test `Allergy`
    - [ ] Test `ImagingStudy`