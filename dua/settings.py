from rdflib import Namespace

DUA_IRI = "https://knacc.umbc.edu/dae-young/kim/ontologies/data-usage-agreement#"
SYNTHEA_IRI = "https://knacc.umbc.edu/dae-young/kim/ontologies/synthea#"

DUA = Namespace(DUA_IRI)
SYN = Namespace(SYNTHEA_IRI)

DUA_COLS = [
    "dataCustodian",
    "recipient",
    "requestedData",  # Basic Information
    "permittedUseOrDisclosure",
    "terms",
    "terminationCause",
    "terminationEffect",  # TermAndTermination
    "dataSecurityPlanAccess",
    "dataSecurityPlanProtection",
    "dataSecurityPlanStorage",
]  # Data_Security_Plan

PERMITTED_USE_OR_DISCLOSURE = [
    "treatment",
    "payment",
    "health_care_operations",
    "notification",
    "public_health",
    "limited_data_set",
]


DATA_CLASSES = [
    "Condition",
    "Encounter",
    "Immunization",
    "Medication",
    "Observation",
    "Organization",
    "Patient",
    "Payer",
    "Procedure",
    "Provider",
]
DATA_CLASS_SAMPLE_SIZE = 3

RANDOM_SEED = 7
