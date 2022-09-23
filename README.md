# synthea_rdf
Semantic web representation for the Synthea.

## Usage
```python
from synthea_rdf import patient

patient_df = pd.read_csv("csv/patients.csv", dtype={'ZIP':str})
for index, row in patient_df.iterrows():
    patient.convert(g, row)
```