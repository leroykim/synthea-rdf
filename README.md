# synthea_rdf
Semantic web representation for the Synthea.

## Usage
```python
from rdflib import Graph
from synthea_rdf import patient, encounter, observation, organization, provider

g = Graph()
g.parse("ontology/synthea_ontology.owl", format="n3")

patient_df = pd.read_csv("csv/patients.csv", dtype={'ZIP':str})
encounter_df = pd.read_csv("csv/encounters.csv")
observation_df = pd.read_csv("csv/observations.csv")
organization_df = pd.read_csv("csv/organizations.csv")
provider_df = pd.read_csv("csv/providers.csv")

patient.convert(g, row)
encounter.convert(g, row)
observation.convert(g, row, index)
organization.convert(g, row)
provider.convert(g, row)
```