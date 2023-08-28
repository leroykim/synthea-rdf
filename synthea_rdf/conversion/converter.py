from abc import ABC, abstractmethod
from alive_progress import alive_bar
from owlready2 import Ontology
from pandas import DataFrame
from synthea_rdf.definitions.classes import *


class Converter(ABC):
    def __init__(self, df: DataFrame, ontology: Ontology):
        self.resource_df = df
        self.ontoloty = ontology

    @abstractmethod
    def run(self, graph):
        pass


class AllergyConverter(Converter):
    def __init__(self, df: DataFrame, ontology: Ontology):
        super().__init__(df, ontology)

    def run(self, graph):
        with alive_bar(len(self.resource_df)) as bar:
            for row in self.resource_df.itertuples():
                allergy = Allergy()
                # Data properties
                allergy.description.append(row.DESCRIPTION)
                allergy.encounterId.append(row.ENCOUNTER)
                allergy.startDate.append(row.START)
                allergy.system.append(row.SYSTEM)
                allergy.patientId.append(row.PATIENT)
                # Object properties
                allergy.isAbout.append(row.PATIENT)
                allergy.isDiagnosedDuring.append(row.ENCOUNTER)

                bar()
