from rdflib import Literal
from rdflib.namespace import RDF, XSD
from datetime import datetime
from .settings import SYN


def date_literal(date):
    return Literal(datetime.strptime(date, "%Y-%m-%d"), datatype=XSD.dateTime)


def datetime_literal(date):
    return Literal(datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)


def dicom_dcm_literal(string):
    return Literal(str(string), datatype=SYN["dicom:DICOM-DCM"])


def dicom_sop_literal(string):
    return Literal(str(string), datatype=SYN["dicom:DICOM-SOP"])


def dicom_uid_literal(string):
    return Literal(str(string), datatype=SYN["dicom:UID"])


def float_literal(string):
    return Literal(str(string), datatype=XSD.float)


def hl7_cvx_literal(string):
    return Literal(str(string), datatype=SYN["hl7:CVX"])


def integer_literal(string):
    return Literal(str(string), datatype=XSD.int)


def loinc_literal(string):
    return Literal(str(string), datatype=SYN["loinc:LOINC"])


def plain_literal(string):
    return Literal(str(string), datatype=RDF.PlainLiteral)


def snomedct_literal(string):
    return Literal(str(string), datatype=SYN["snomed:SNOMED-CT"])


def udi_literal(string):
    return Literal(str(string), datatype=SYN["fda:UDI"])


def umls_rxnorm_literal(string):
    return Literal(str(string), datatype=SYN["umls:RxNorm"])


def uuid_literal(string):
    # https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.namespace.html#rdflib.namespace.Namespace
    return Literal(str(string), datatype=SYN["urn:uuid"])
