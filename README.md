# 🕸️ SYNTHEA RDF
[![KnAcc Lab](https://tinyurl.com/knacclogo)](https://knacc.umbc.edu/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE)

Semantic web representation for the Synthea and CSVs to Turtle (.ttl) conversion tool.

![synthea_ontology](synthea_ontology/synthea_ontology.png)

> Synthea ontology and conversion method v1.0 are done.
> WIP minor fixes.

## :hammer: Usage
### Single CSV
```python
import pandas as pd
from rdflib import Graph
from synthea_rdf.graph import GraphBuilder

MODEL_PATH = "./synthea_ontology/synthea_ontology.ttl"
DIR_PATH = "./csv"
DEST_PATH = "./result"


encounter_df = pd.read_csv(f"{DIR_PATH}/encounters.csv")
graph = Graph()
builder = GraphBuilder(MODEL_PATH)
builder.setModel(graph)
builder.convertEncounter(encounter_df, graph)
graph.serialize(destination=f"{DEST_PATH}/encounter.ttl")
```

### All CSV
> WIP simplified version by reading all CSV in a `DIR_PATH` directory (Synthea provides CSV files in one directory.)

```python
import pandas as pd
from synthea_rdf.graph import GraphBuilder

MODEL_PATH = "./synthea_ontology/synthea_ontology.ttl"
DIR_PATH = "./csv/Maryland_covid19_patient_10_bin_1"
DEST_PATH = "./test_result"

allergy_df = pd.read_csv(f"{DIR_PATH}/allergies.csv")
carePlan_df = pd.read_csv(f"{DIR_PATH}/careplans.csv")
claim_df = pd.read_csv(f"{DIR_PATH}/claims.csv")
claimTransaction_df = pd.read_csv(f"{DIR_PATH}/claims_transactions.csv")
condition_df = pd.read_csv(f"{DIR_PATH}/conditions.csv")
device_df = pd.read_csv(f"{DIR_PATH}/devices.csv")
encounter_df = pd.read_csv(f"{DIR_PATH}/encounters.csv")
imagingStudy_df = pd.read_csv(f"{DIR_PATH}/imaging_studies.csv")
immunization_df = pd.read_csv(f"{DIR_PATH}/immunizations.csv")
medication_df = pd.read_csv(f"{DIR_PATH}/medications.csv")
observation_df = pd.read_csv(f"{DIR_PATH}/observations.csv")
organization_df = pd.read_csv(f"{DIR_PATH}/organizations.csv")
patient_df = pd.read_csv(f"{DIR_PATH}/patients.csv")
payer_df = pd.read_csv(f"{DIR_PATH}/payers.csv")
payerTransition_df = pd.read_csv(f"{DIR_PATH}/payer_transitions.csv")
procedure_df = pd.read_csv(f"{DIR_PATH}/procedures.csv")
provider_df = pd.read_csv(f"{DIR_PATH}/providers.csv")
supply_df = pd.read_csv(f"{DIR_PATH}/supplies.csv")

builder = GraphBuilder(MODEL_PATH)
builder.allergy_df = allergy_df
builder.carePlan_df = carePlan_df
builder.claim_df = claim_df
builder.claimTransaction_df = claimTransaction_df
builder.condition_df = condition_df
builder.device_df = device_df
builder.encounter_df = encounter_df
builder.imagingStudy_df = imagingStudy_df
builder.immunization_df = immunization_df
builder.medication_df = medication_df
builder.observation_df = observation_df
builder.organization_df = organization_df
builder.patient_df = patient_df
builder.payer_df = payer_df
builder.payerTransition_df = payerTransition_df
builder.procedure_df = procedure_df
builder.provider_df = provider_df
builder.supply_df = supply_df

graph = builder.build()
graph.serialize(destination=f"{DEST_PATH}/synthea.ttl")
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