from rdflib.namespace import RDF
from alive_progress import alive_bar

from .helper import organization_uri, string_literal, float_literal, patient_uri, encounter_uri, \
    datetime_literal, organization_uri, provider_uri, payer_uri
from .setting import SYN

class Encounter():
    def __init__(self, encounter_df):
        self.encounter_df = encounter_df

    def convert(self, graph):
        with alive_bar(self.encounter_df.shape[0], force_tty=True) as bar:
            for _, row in self.encounter_df.iterrows():
                encounter = encounter_uri(row['Id'])
                graph.add((encounter, RDF.type, SYN.Encounter))
                graph.add((encounter, SYN.start_time, datetime_literal(row['START'])))
                graph.add((encounter, SYN.stop_time, datetime_literal(row['STOP'])))
                graph.add((encounter, SYN.encounterdPatient, patient_uri(row['PATIENT'])))
                graph.add((encounter, SYN.assessedIn, organization_uri(row['ORGANIZATION'])))
                graph.add((encounter, SYN.assessedBy, provider_uri(row['PROVIDER'])))
                graph.add((encounter, SYN.paidBy, payer_uri(row['PAYER'])))
                graph.add((encounter, SYN.encounter_class, string_literal(row['ENCOUNTERCLASS'])))
                graph.add((encounter, SYN.encounter_code, string_literal(row['CODE'])))
                graph.add((encounter, SYN.encounter_description, string_literal(row['DESCRIPTION'])))
                graph.add((encounter, SYN.base_encounter_cost, float_literal(row['BASE_ENCOUNTER_COST'])))
                graph.add((encounter, SYN.total_claim_cost, float_literal(row['TOTAL_CLAIM_COST'])))
                graph.add((encounter, SYN.payer_coverage, float_literal(row['PAYER_COVERAGE'])))
                graph.add((encounter, SYN.reason_code, string_literal(row['REASONCODE'])))
                graph.add((encounter, SYN.reason_description, string_literal(row['REASONDESCRIPTION'])))
                bar()