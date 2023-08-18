"""
Warning: The datatype must be declared **BEFORE** loading any ontology that uses it.
"""

from owlready2 import *

"""
SUMMARY
-------
This file contains the definitions for the datatypes used in the Synthea ontology.

NOTE
----
Skip definitions for dateLiteral and dateTimeLiteral

SEE ALSO
--------
abstracts/literal.py
"""


class DICOM_DCM(object):
    def __init__(self, value):
        self.value = value


class DICOM_SOP(object):
    def __init__(self, value):
        self.value = value


class DICOM_UID(object):
    def __init__(self, value):
        self.value = value


class FDA_UDI(object):
    def __init__(self, value):
        self.value = value


class HL7_CVX(object):
    def __init__(self, value):
        self.value = value


class LOINC(object):
    def __init__(self, value):
        self.value = value


class SNOMED_CT(object):
    def __init__(self, value):
        self.value = value


class UMLS_RXNORM(object):
    def __init__(self, value):
        self.value = value


class URN_UUID(object):
    def __init__(self, value):
        self.value = value


declare_datatype(
    DICOM_DCM, "https://www.dicomstandard.org/DICOM-DCM", str, lambda x: str(x.value)
)
declare_datatype(
    DICOM_SOP, "https://www.dicomstandard.org/DICOM-SOP", str, lambda x: str(x.value)
)
declare_datatype(
    DICOM_UID, "https://www.dicomstandard.org/DICOM-UID", str, lambda x: str(x.value)
)
declare_datatype(FDA_UDI, "https://www.fda.gov/udi", str, lambda x: str(x.value))
declare_datatype(HL7_CVX, "https://www.hl7.org/cvx", str, lambda x: str(x.value))
declare_datatype(LOINC, "https://loinc.org", str, lambda x: str(x.value))
declare_datatype(SNOMED_CT, "https://snomed.org", str, lambda x: str(x.value))
declare_datatype(
    UMLS_RXNORM,
    "https://www.nlm.nih.gov/research/umls/rxnorm",
    str,
    lambda x: str(x.value),
)
declare_datatype(
    URN_UUID, "https://www.ietf.org/rfc/rfc4122.txt", str, lambda x: str(x.value)
)
