from rdflib import URIRef
from .namespace import SYN, DUA, TST


# Synthea URIs
def allergyUri(id):
    return URIRef(f"{SYN}allergy_{id}")


def carePlanUri(id):
    return URIRef(f"{SYN}carePlan_{id}")


def claimUri(id):
    return URIRef(f"{SYN}claim_{id}")


def claimTransactionUri(id):
    return URIRef(f"{SYN}claimTransaction_{id}")


def conditionUri(id):
    return URIRef(f"{SYN}condition_{id}")


def deviceUri(id):
    return URIRef(f"{SYN}device_{id}")


def encounterUri(encounter_id):
    return URIRef(f"{SYN}encounter_{encounter_id}")


def imagingStudyUri(imagingstudy_id):
    return URIRef(f"{SYN}imagingStudy_{imagingstudy_id}")


def immunizationUri(id):
    return URIRef(f"{SYN}immunization_{id}")


def medicationUri(id):
    return URIRef(f"{SYN}medication_{id}")


def observationUri(observation_id):
    return URIRef(f"{SYN}observation_{observation_id}")


def organizationUri(organization_id):
    return URIRef(f"{SYN}organization_{organization_id}")


def patientUri(id):
    return URIRef(f"{SYN}patient_{id}")


def payerUri(payer_id):
    return URIRef(f"{SYN}payer_{payer_id}")


def payertransitionUri(payertransition_id):
    return URIRef(f"{SYN}payerTransition_{payertransition_id}")


def procedureUri(procedure_id):
    return URIRef(f"{SYN}procedure_{procedure_id}")


def providerUri(provider_id):
    return URIRef(f"{SYN}provider_{provider_id}")


def supplyUri(supply_id):
    return URIRef(f"{SYN}supply_{supply_id}")


# DUA URIs
def syntheaUri(name):
    return URIRef(f"{SYN}{name}")


def duaUri(dua_id):
    return URIRef(f"{DUA}dua_{dua_id}")


def permittedUseOrDisclosureUri(dua_id):
    return URIRef(f"{DUA}{dua_id}")


def dataSecurityPlanUri(dua_id):
    # Permitted Usage or Disclosure
    return URIRef(f"{DUA}data_security_plan_{dua_id}")


def termAndTerminationUri(dua_id):
    # Permitted Usage or Disclosure
    return URIRef(f"{DUA}term_and_termination_{dua_id}")


# def duaOrganizationUri(organization_id):
#     return URIRef(f"{DUA}organization_{organization_id}")


# TrustScore URIs
def trustscoreUserUri(user_id):
    return URIRef(f"{TST}user_{user_id}")


# def trustscoreOrganizationUri(organization_id):
#     return URIRef(f"{TST}organization_{organization_id}")
