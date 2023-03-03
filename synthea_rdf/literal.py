from rdflib import Literal
from rdflib.namespace import RDF, XSD
from datetime import datetime
from .settings import SYN


def uuid_literal(string):
    # https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.namespace.html#rdflib.namespace.Namespace
    return Literal(str(string), datatype=SYN["urn:uuid"])


def snomedct_literal(string):
    return Literal(str(string), datatype=SYN["snomed:SNOMED-CT"])


def loinc_literal(string):
    return Literal(str(string), datatype=SYN["loinc:LOINC"])


def udi_literal(string):
    return Literal(str(string), datatype=SYN["fda:UDI"])


def date_literal(date):
    return Literal(datetime.strptime(date, "%Y-%m-%d"), datatype=XSD.dateTime)


def datetime_literal(date):
    return Literal(datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)


def plain_literal(string):
    return Literal(str(string), datatype=RDF.PlainLiteral)


def int_literal(string):
    return Literal(str(string), datatype=XSD.int)


def float_literal(string):
    return Literal(str(string), datatype=XSD.float)
