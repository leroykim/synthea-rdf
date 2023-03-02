from rdflib import Namespace

SYNTHEA_IRI = "https://knacc.umbc.edu/dae-young/kim/ontologies/synthea#"
TRUST_IRI = "https://knacc.umbc.edu/leroy/ontologies/trust#"
DATA_EXCHANGE_IRI = "https://knacc.umbc.edu/leroy/ontologies/data-exchange#"
DUA_IRI = "https://knacc.umbc.edu/leroy/ontologies/data-usage-agreement#"

SYN = Namespace(SYNTHEA_IRI)
TST = Namespace(TRUST_IRI)
DEX = Namespace(DATA_EXCHANGE_IRI)
DUA = Namespace(DUA_IRI)

USER_TRUST_COLS = ["behavioral_trust", "identity_trust"]
VERACITY_COLS = ["credibility", "objectivity", "trustfulness"]
ORG_TRUST_COLS = ["reputation"]
