from rdflib import URIRef
from .settings import SYN


# URI helper methods
def allergy_uri(id):
    return URIRef(f"{SYN}allergy_{id}")


def careplan_uri(id):
    return URIRef(f"{SYN}carePlan_{id}")


def claim_uri(id):
    return URIRef(f"{SYN}claim_{id}")


def claimtransaction_uri(id):
    return URIRef(f"{SYN}claimTransaction_{id}")


def condition_uri(id):
    return URIRef(f"{SYN}condition_{id}")


def device_uri(id):
    return URIRef(f"{SYN}device_{id}")


def encounter_uri(encounter_id):
    return URIRef(f"{SYN}encounter_{encounter_id}")


def observation_uri(observation_id):
    return URIRef(f"{SYN}observation_{observation_id}")


def organization_uri(organization_id):
    return URIRef(f"{SYN}organization_{organization_id}")


def patient_uri(id):
    return URIRef(f"{SYN}patient_{id}")


def payer_uri(payer_id):
    return URIRef(f"{SYN}payer_{payer_id}")


def provider_uri(provider_id):
    return URIRef(f"{SYN}provider_{provider_id}")
