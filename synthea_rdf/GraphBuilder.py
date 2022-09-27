from rdflib import Graph
from . import Encounter, Observation, Organization, Patient, Provider

class GraphBuilder():
    def __init__(self):
        self.graph = None
        self.patient_df = None
        self.encounter_df = None
        self.observation_df = None
        self.organization_df = None
        self.provider_df = None

    def build(self):
        if self.patient_df is None:
            print("Patient data frame file must be provided!")
            return

        self.__convert_patient()
        self.__convert_encounter()
        self.__convert_observation()
        self.__convert_organization()
        self.__convert_provider

    def get_graph(self):
        return self.graph

    def __convert_patient(self):
        if self.patient_df is not None:
            patient = Patient(self.patient_df)
            patient.convert(self.graph)

    def __convert_encounter(self):
        if self.encounter_df is not None:
            encounter = Encounter(self.encounter_df)
            encounter.convert(self.graph)
    
    def __convert_observation(self):
        if self.observation_df is not None:
            observation = Observation(self.organization_df)
            observation.convert(self.graph)
    
    def __convert_organization(self):
        if self.organization_df is not None:
            organization = Organization(self.organization_df)
            organization.convert(self.graph)

    def __convert_provider(self):
        if self.provider_df is not None:
            provider = Provider(self.provider_df)
            provider.convert(self.graph)