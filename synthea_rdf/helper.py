from rdflib import Literal, URIRef
from datetime import datetime
from rdflib.namespace import XSD

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

# URIRef helper methods
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