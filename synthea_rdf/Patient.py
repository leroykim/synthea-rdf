from rdflib.namespace import RDF
import pandas as pd
from alive_progress import alive_bar

from .helper import date_literal, string_literal, int_literal, float_literal, patient_uri
from .setting import SYN

class Patient():
    def __init__(self, patient_df):
        self.patient_df = patient_df

    def convert(self, graph):
        with alive_bar(self.patient_df.shape[0], force_tty=True) as bar:
            for _, row in self.patient_df.iterrows():
                patient =  patient_uri(row['Id'])
                graph.add((patient, RDF.type, SYN.Patient)) # type
                graph.add((patient, SYN.id, string_literal(row['Id']))) # id
                graph.add((patient, SYN.birthdate, date_literal(row['BIRTHDATE']))) # birthdate
                if pd.notnull(row['DEATHDATE']):
                    graph.add(patient, SYN.DEATHDATE, date_literal(row['DEATHDATE'])) # deathdate
                graph.add((patient, SYN.ssn, string_literal(row['SSN']))) # ssn
                graph.add((patient, SYN.drivers, string_literal(row['DRIVERS']))) # drivers license
                graph.add((patient, SYN.passport, string_literal(row['PASSPORT'])))
                graph.add((patient, SYN.firstname, string_literal(row['FIRST'])))
                graph.add((patient, SYN.lastname, string_literal(row['LAST'])))
                graph.add((patient, SYN.marital, string_literal(row['MARITAL'])))
                graph.add((patient, SYN.race, string_literal(row['RACE'])))
                graph.add((patient, SYN.ethnicity, string_literal(row['ETHNICITY'])))
                graph.add((patient, SYN.gender, string_literal(row['GENDER'])))
                graph.add((patient, SYN.birthplace, string_literal(row['BIRTHPLACE'])))
                graph.add((patient, SYN.address, string_literal(row['ADDRESS'])))
                graph.add((patient, SYN.city, string_literal(row['CITY'])))
                graph.add((patient, SYN.state, string_literal(row['STATE'])))
                graph.add((patient, SYN.county, string_literal(row['COUNTY'])))
                graph.add((patient, SYN.zip, string_literal(row['ZIP'])))
                graph.add((patient, SYN.healthcare_coverage, float_literal(row['HEALTHCARE_COVERAGE'])))
                graph.add((patient, SYN.healthcare_expenses, float_literal(row['HEALTHCARE_EXPENSES'])))
                graph.add((patient, SYN.income, int_literal(row['INCOME'])))
                bar()