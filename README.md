
[![KnAcc Lab][1]](https://knacc.umbc.edu/)
# SYNTHEA RDF [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)

Semantic web representation for the Synthea and CSVs to Turtle (.ttl) conversion tool.

![synthea_ontology](synthea_ontology/synthea_ontology.png)

> Synthea ontology v1.0 is done, but conversion tool is under development.

## Usage
```python
import pandas as pd
from synthea_rdf.graph import GraphBuilder

patient_df = pd.read_csv("csv/patients.csv", dtype={'ZIP':str})
encounter_df = pd.read_csv("csv/encounters.csv")
observation_df = pd.read_csv("csv/observations.csv")
organization_df = pd.read_csv("csv/organizations.csv")
provider_df = pd.read_csv("csv/providers.csv")
payer_df = pd.read_csv("csv/payers.csv")

model_path = "ontology/synthea_ontology.owl"

builder = GraphBuilder()
# Or,
# builder = GraphBuilder(persistence='sqlite')
# for SQLite backup. -> too slow though.

builder.patient_df = patient_df
builder.encounter_df = encounter_df
builder.observation_df = observation_df
builder.organization_df = organization_df
builder.provider_df = provider_df
builder.payer_df = payer_df

graph = builder.build(model_path="ontology/synthea_ontology.owl")

graph.serialize(destination="ontology/test_result.owl")
```

[1]: https://img.shields.io/badge/-UMBC_KnAcc_Lab-black?style=flat&logoWidth=50&logo=data:image/jpeg;base64,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