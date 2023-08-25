from owlready2 import get_ontology, DataProperty
from synthea_rdf.util.configuration import Configuration
from synthea_rdf.definitions.classes import *

synthea_ontology = get_ontology(Configuration.synthea_namespace)

# with synthea_ontology:
