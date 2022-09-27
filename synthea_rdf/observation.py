from rdflib.namespace import RDF

from .helper import datetime_literal, string_literal, patient_uri, observation_uri, encounter_uri
from .setting import SYN

def convert(graph, observation_df):
    for index, row in observation_df.iterrows():
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