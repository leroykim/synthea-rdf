# synthea_rdf
Semantic web representation for the Synthea.

## Usage
```python
from rdflib import Graph
from synthea_rdf import patient, encounter, observation, organization, provider

g = Graph()
g.parse("ontology/synthea_ontology.owl", format="n3")

patient_df = pd.read_csv("csv/patients.csv", dtype={'ZIP':str})
for index, row in patient_df.iterrows():
    patient.convert(g, row)

encounter_df = pd.read_csv("csv/encounters.csv")
for index, row in encounter_df.iterrows():
    encounter.convert(g, row)

observation_df = pd.read_csv("csv/observations.csv")
for index, row in observation_df.iterrows():
    observation.convert(g, row, index)

organization_df = pd.read_csv("csv/organizations.csv")
for index, row in organization_df.iterrows():
    organization.convert(g, row)

provider_df = pd.read_csv("csv/providers.csv")
for index, row in provider_df.iterrows():
    provider.convert(g, row)
```