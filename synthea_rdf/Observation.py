from rdflib.namespace import RDF
from alive_progress import alive_bar

from .helper import datetime_literal, string_literal, patient_uri, observation_uri, encounter_uri
from .setting import SYN

class Observation():
    def __init__(self, observation_df):
        self.observation_df = observation_df

    def convert(self, graph):
        with alive_bar(self.observation_df.shape[0], force_tty=True) as bar:
            for index, row in self.observation_df.iterrows():
                observation = observation_uri(index)
                graph.add((observation, RDF.type, SYN.Observation))
                graph.add((observation, SYN.date, datetime_literal(row['DATE'])))
                graph.add((observation, SYN.observedPatient, patient_uri(row['PATIENT'])))
                graph.add((observation, SYN.isFromEncounter, encounter_uri(row['ENCOUNTER'])))
                graph.add((observation, SYN.category, string_literal(row['CATEGORY'])))
                graph.add((observation, SYN.observation_code, string_literal(row['CODE'])))
                graph.add((observation, SYN.observation_description, string_literal(row['DESCRIPTION'])))
                graph.add((observation, SYN.value, string_literal(row['VALUE'])))
                graph.add((observation, SYN.units, string_literal(row['UNITS'])))
                graph.add((observation, SYN.type, string_literal(row['TYPE'])))
                bar()