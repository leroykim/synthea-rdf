from rdflib import Namespace

DUA_IRI = "https://knacc.umbc.edu/leroy/ontologies/data-usage-agreement#"
DUA = Namespace(DUA_IRI)

DUA_COLS = ['dataCustodian','recipient', 'requestedData', # Basic Information
'permittedUseOrDisclosure', 'term', 'terminationCause', 'terminationEffect',  # TermAndTermination
'dataSecurityPlanAccess', 'dataSecurityPlanProtection', 'dataSecurityPlanStorage']  # Data_Security_Plan
DUA_COUNT = 7

PERMITTED_USE_OR_DISCLOSURE = [
    'treatment', 'payment', 'health_care_operations', 'notification', 'public_health', 'limited_data_set']


DATA_CLASSES = ['Condition', 'Encounter', 'Immunization', 'Medication', 'Observation',
                'Organization', 'Patient', 'Payer', 'Procedure', 'Provider']
DATA_CLASS_SAMPLE_SIZE = 3

RANDOM_SEED = 7
SAVE_PATH = "./csv/dua/dua.csv"