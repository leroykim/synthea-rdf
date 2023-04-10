from rdflib import Literal
from rdflib.namespace import RDF, XSD
from datetime import datetime
from abstract.namespace import SYN


# Synthea Literals
def dateLiteral(date):
    return Literal(datetime.strptime(date, "%Y-%m-%d"), datatype=XSD.dateTime)


def dateTimeLiteral(date):
    return Literal(datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)


def dicomDcmLiteral(string):
    return Literal(str(string), datatype=SYN["dicom:DICOM-DCM"])


def dicomSopLiteral(string):
    return Literal(str(string), datatype=SYN["dicom:DICOM-SOP"])


def dicomUidLiteral(string):
    return Literal(str(string), datatype=SYN["dicom:UID"])


def fdaUdiLiteral(string):
    return Literal(str(string), datatype=SYN["fda:UDI"])


def floatLiteral(string):
    return Literal(str(string), datatype=XSD.float)


def hl7CvxLiteral(string):
    return Literal(str(string), datatype=SYN["hl7:CVX"])


def integerLiteral(string):
    return Literal(str(string), datatype=XSD.int)


def loincLiteral(string):
    return Literal(str(string), datatype=SYN["loinc:LOINC"])


def plainLiteral(string):
    return Literal(str(string), datatype=RDF.PlainLiteral)


def snomedCtLiteral(string):
    return Literal(str(string), datatype=SYN["snomed:SNOMED-CT"])


def umlsRxnormLiteral(string):
    return Literal(str(string), datatype=SYN["umls:RxNorm"])


def urnUuidLiteral(string):
    # https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.namespace.html#rdflib.namespace.Namespace
    return Literal(str(string), datatype=SYN["urn:uuid"])
