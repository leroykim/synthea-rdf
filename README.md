# synthea_rdf
Semantic web representation for the Synthea.

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