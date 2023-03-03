from pathlib import Path
from rdflib import Graph, Literal
from .resource import Encounter, Observation, Organization, Patient, Payer, Provider
from .settings import SYN, DUA


class GraphBuilder:
    def __init__(self, model_path, persistence=None, include_dua: bool = False):
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

        self.include_dua = include_dua
        self.dua_class = None
        self.dua_df = None

    def build(self):
        # if model_path is not None:
        #     self.__set_model(model_path)
        # else:
        #     print("Model path required!")
        #     return

        # if self.patient_df is None:
        #     print("Patient data frame file must be provided!")
        #     return

        self.convert_patient(self.patient_df, self.graph)
        self.convert_encounter(self.encounter_df, self.graph)
        self.convert_observation(self.observation_df, self.graph)
        self.convert_organization(self.organization_df, self.graph)
        self.convert_provider(self.provider_df, self.graph)
        self.convert_payer(self.payer_df, self.graph)

        if self.include_dua:
            self.convert_dua()

        return self.graph

    def __init_sqlite(self):
        self.graph = Graph("SQLAlchemy", identifier="synthea_graph")
        persistence_path = Path(".") / "persistence"
        persistence_path.mkdir(exist_ok=True)
        dbfile_path = persistence_path / "synthea_patient.sqlite"
        dburi = Literal(f"sqlite:///{dbfile_path}")
        if not dbfile_path.is_file():
            self.graph.open(dburi, create=True)
        else:
            self.graph.open(dburi)

    def __set_model(self, model_path):
        self.graph.parse(model_path, format="n3")
        self.graph.bind("syn", SYN)
        # self.graph.bind("", SYN)
        self.namespace_manager = self.graph.namespace_manager

        print(f"Model has {len(self.graph)} triples.")

    def convert_patient(self, patient_df=None, graph=None):
        if patient_df is not None and graph is not None:
            patient = Patient(patient_df)
            patient.convert(graph)
        else:
            print("patient_df is not set.")

    def convert_encounter(self, encounter_df=None, graph=None):
        if encounter_df is not None and graph is not None:
            encounter = Encounter(encounter_df)
            encounter.convert(graph)
        else:
            print("encounter_df is not set.")

    def convert_observation(self, observation_df=None, graph=None):
        if observation_df is not None and graph is not None:
            observation = Observation(observation_df)
            observation.convert(graph)
        else:
            print("observation_df is not set.")

    def convert_organization(self, organization_df=None, graph=None):
        if organization_df is not None and graph is not None:
            organization = Organization(organization_df)
            organization.convert(graph)
        else:
            print("organization_df is note set.")

    def convert_provider(self, provider_df=None, graph=None):
        if provider_df is not None and graph is not None:
            provider = Provider(provider_df)
            provider.convert(graph)
        else:
            print("provider_df is not set.")

    def convert_payer(self, payer_df=None, graph=None):
        if payer_df is not None and graph is not None:
            payer = Payer(payer_df)
            payer.convert(graph)
        else:
            print("payer_df is not set.")

    # def convert_dua(self, dua_df=None, graph=None):
    #     if dua_df is not None and graph is not None:
    #         dua = self.dua_class(self.dua_df)
    #         dua.convert(self.graph)
    #     else:
    #         print("DUA_df is not set.")
