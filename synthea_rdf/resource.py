from abc import ABC, abstractmethod

from datetime import datetime

from alive_progress import alive_bar
import pandas as pd
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD

from .setting import SYN

class Resource(ABC):
    @abstractmethod
    def __init__(self, df):
        self.__resource_df = df

    @property
    @abstractmethod
    def resource_df(self):
        pass

    @resource_df.setter
    @abstractmethod
    def resource_df(self, value):
        pass

    @abstractmethod
    def convert(self, graph):
        pass

class Encounter(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        with alive_bar(self.__resource_df.shape[0], force_tty=True, title='Encounter Conversion') as bar:
            for _, row in self.__resource_df.iterrows():
                encounter = encounter_uri(row['Id'])
                graph.add((encounter, RDF.type, SYN.Encounter))
                graph.add((encounter, SYN.start_time, datetime_literal(row['START'])))
                graph.add((encounter, SYN.stop_time, datetime_literal(row['STOP'])))
                graph.add((encounter, SYN.encounterdPatient, patient_uri(row['PATIENT'])))
                graph.add((encounter, SYN.assessedIn, organization_uri(row['ORGANIZATION'])))
                graph.add((encounter, SYN.assessedBy, provider_uri(row['PROVIDER'])))
                graph.add((encounter, SYN.paidBy, payer_uri(row['PAYER'])))
                graph.add((encounter, SYN.encounter_class, string_literal(row['ENCOUNTERCLASS'])))
                graph.add((encounter, SYN.encounter_code, string_literal(row['CODE'])))
                graph.add((encounter, SYN.encounter_description, string_literal(row['DESCRIPTION'])))
                graph.add((encounter, SYN.base_encounter_cost, float_literal(row['BASE_ENCOUNTER_COST'])))
                graph.add((encounter, SYN.total_claim_cost, float_literal(row['TOTAL_CLAIM_COST'])))
                graph.add((encounter, SYN.payer_coverage, float_literal(row['PAYER_COVERAGE'])))
                graph.add((encounter, SYN.reason_code, string_literal(row['REASONCODE'])))
                graph.add((encounter, SYN.reason_description, string_literal(row['REASONDESCRIPTION'])))
                bar()

class Observation(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        with alive_bar(self.__resource_df.shape[0], force_tty=True, title='Obvervation Conversion') as bar:
            for index, row in self.__resource_df.iterrows():
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

class Organization(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        with alive_bar(self.__resource_df.shape[0], force_tty=True, title='Organization Conversion') as bar:
            for _, row in self.__resource_df.iterrows():
                organization = organization_uri(row['Id'])
                graph.add((organization, RDF.type, SYN.Organization))
                graph.add((organization, SYN.name, string_literal(row['NAME'])))
                graph.add((organization, SYN.address, string_literal(row['ADDRESS'])))
                graph.add((organization, SYN.city, string_literal(row['CITY'])))
                graph.add((organization, SYN.state, string_literal(row['STATE'])))
                graph.add((organization, SYN.zip, string_literal(row['ZIP'])))
                graph.add((organization, SYN.phone, string_literal(row['PHONE'])))
                graph.add((organization, SYN.revenue, float_literal(row['REVENUE'])))
                graph.add((organization, SYN.utilization, int_literal(row['UTILIZATION'])))
                bar()

class Patient(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        with alive_bar(self.__resource_df.shape[0], force_tty=True, title='Patient Conversion') as bar:
            for _, row in self.__resource_df.iterrows():
                patient =  patient_uri(row['Id'])
                graph.add((patient, RDF.type, SYN.Patient)) # type
                graph.add((patient, SYN.id, string_literal(row['Id']))) # id
                graph.add((patient, SYN.birthdate, date_literal(row['BIRTHDATE']))) # birthdate
                if pd.notnull(row['DEATHDATE']):
                    graph.add((patient, SYN.DEATHDATE, date_literal(row['DEATHDATE']))) # deathdate
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

class Provider(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        with alive_bar(self.__resource_df.shape[0], force_tty=True, title='Provider Conversion') as bar:
            for _, row in self.__resource_df.iterrows():
                provider = provider_uri(row['Id'])
                graph.add((provider, RDF.type, SYN.Provider))
                graph.add((provider, SYN.belongsTo, organization_uri(row['ORGANIZATION'])))
                graph.add((provider, SYN.name, string_literal(row['NAME'])))
                graph.add((provider, SYN.gender, string_literal(row['GENDER'])))
                graph.add((provider, SYN.speciality, string_literal(row['SPECIALITY'])))
                graph.add((provider, SYN.address, string_literal(row['ADDRESS'])))
                graph.add((provider, SYN.city, string_literal(row['CITY'])))
                graph.add((provider, SYN.state, string_literal(row['STATE'])))
                graph.add((provider, SYN.zip, string_literal(row['ZIP'])))
                graph.add((provider, SYN.utilization, int_literal(row['UTILIZATION'])))
                bar()

class Payer(Resource):
    def __init__(self, df):
        self.__resource_df = df
    
    @property
    def resource_df(self):
        return self.__resource_df
    
    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value
    
    def convert(self, graph):
        with alive_bar(self.__resource_df.shape[0], force_tty=True, title='Payer Conversion') as bar:
            for _, row in self.__resource_df.iterrows():
                payer = payer_uri(row['Id'])
                graph.add((payer, RDF.type, SYN.Payer)) # type
                graph.add((payer, SYN.id, string_literal(row['Id']))) # id
                graph.add((payer, SYN.name, string_literal(row['NAME']))) # name
                graph.add((payer, SYN.address, string_literal(row['ADDRESS']))) # address
                graph.add((payer, SYN.city, string_literal(row['CITY']))) # city
                graph.add((payer, SYN.state_headquartered, string_literal(row['STATE_HEADQUARTERED'])))
                graph.add((payer, SYN.zip, string_literal(row['ZIP'])))
                graph.add((payer, SYN.phone, string_literal(row['PHONE'])))
                graph.add((payer, SYN.amount_covered, float_literal(row['AMOUNT_COVERED'])))
                graph.add((payer, SYN.amount_uncovered, float_literal(row['AMOUNT_UNCOVERED'])))
                graph.add((payer, SYN.revenue, float_literal(row['REVENUE'])))
                graph.add((payer, SYN.covered_encounters, int_literal(row['COVERED_ENCOUNTERS'])))
                graph.add((payer, SYN.uncovered_encounters, int_literal(row['UNCOVERED_ENCOUNTERS'])))
                graph.add((payer, SYN.covered_medications, int_literal(row['COVERED_MEDICATIONS']))) 
                graph.add((payer, SYN.uncovered_medications, int_literal(row['UNCOVERED_MEDICATIONS'])))
                graph.add((payer, SYN.covered_procedures, int_literal(row['COVERED_PROCEDURES'])))
                graph.add((payer, SYN.uncovered_procedures, int_literal(row['UNCOVERED_PROCEDURES'])))
                graph.add((payer, SYN.covered_immunizations, int_literal(row['COVERED_IMMUNIZATIONS'])))
                graph.add((payer, SYN.uncovered_immunizations, int_literal(row['UNCOVERED_IMMUNIZATIONS'])))
                graph.add((payer, SYN.unique_customers, int_literal(row['UNIQUE_CUSTOMERS'])))
                graph.add((payer, SYN.qols_avg, float_literal(row['QOLS_AVG'])))
                graph.add((payer, SYN.member_months, int_literal(row['MEMBER_MONTHS'])))
                bar()

##################
# HELPER METHODS #
##################

# Literal helper methods
def date_literal(date):
    return Literal(datetime.strptime(date,'%Y-%m-%d'), datatype=XSD.dateTime)

def datetime_literal(date):
    return Literal(datetime.strptime(date,"%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)

def string_literal(string):
    return Literal(str(string), datatype=XSD.string)

def int_literal(string):
    return Literal(str(string), datatype=XSD.int)

def float_literal(string):
    return Literal(str(string), datatype=XSD.float)

# URI helper methods
def patient_uri(patient_id):
    return URIRef(f'patient_{patient_id}')

def encounter_uri(encounter_id):
    return URIRef(f"encounter_{encounter_id}")

def organization_uri(organization_id):
    return URIRef(f'organization_{organization_id}')

def provider_uri(provider_id):
    return URIRef(f'provider_{provider_id}')

def payer_uri(payer_id):
    return URIRef(f'payer_{payer_id}')

def observation_uri(observation_id):
    return URIRef(f'observation_{observation_id}')