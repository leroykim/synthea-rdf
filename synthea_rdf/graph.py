from pathlib import Path
from rdflib import Graph, Literal
from .resource import Encounter, Observation, Organization, Patient, Payer, Provider
from .settings import SYN

class GraphBuilder():
    def __init__(self, model_path, persistence=None):
        if persistence == "sqlite":
            self.__init_sqlite()
        else:
            self.graph = Graph()


        self.__set_model(model_path)
        self.patient_df = None
        self.encounter_df = None
        self.observation_df = None
        self.organization_df = None
        self.provider_df = None
        self.payer_df = None

    def build(self):
        # if model_path is not None:
        #     self.__set_model(model_path)
        # else:
        #     print("Model path required!")
        #     return

        if self.patient_df is None:
            print("Patient data frame file must be provided!")
            return

        self.__convert_patient()
        self.__convert_encounter()
        self.__convert_observation()
        self.__convert_organization()
        self.__convert_provider()
        self.__convert_payer()

        return self.graph

    def __init_sqlite(self):
        self.graph = Graph('SQLAlchemy', identifier='synthea_graph')
        persistence_path = Path('.')/'persistence'
        persistence_path.mkdir(exist_ok=True)
        dbfile_path = persistence_path/'synthea_patient.sqlite'
        dburi = Literal(f"sqlite:///{dbfile_path}")
        if not dbfile_path.is_file():
            self.graph.open(dburi, create=True)
        else:
            self.graph.open(dburi)
    
    def __set_model(self, model_path):
        self.graph.parse(model_path, format="n3")
        self.graph.bind("syn", SYN)
        self.namespace_manager = self.graph.namespace_manager

        print(f"Model has {len(self.graph)} triples.")

    def __convert_patient(self):
        if self.patient_df is not None:
            patient = Patient(self.patient_df)
            patient.convert(self.graph)
        else:
            print("Patient_df is not set.")

    def __convert_encounter(self):
        if self.encounter_df is not None:
            encounter = Encounter(self.encounter_df)
            encounter.convert(self.graph)
        else:
            print("Encounter_df is not set.")
    
    def __convert_observation(self):
        if self.observation_df is not None:
            observation = Observation(self.observation_df)
            observation.convert(self.graph)
        else:
            print("Observation_df is not set.")
    
    def __convert_organization(self):
        if self.organization_df is not None:
            organization = Organization(self.organization_df)
            organization.convert(self.graph)
        else:
            print("Organization_df is note set.")

    def __convert_provider(self):
        if self.provider_df is not None:
            provider = Provider(self.provider_df)
            provider.convert(self.graph)
        else:
            print("Provider_df is not set.")

    def __convert_payer(self):
        if self.payer_df is not None:
            payer = Payer(self.payer_df)
            payer.convert(self.graph)
        else:
            print("Payer_df is not set.")