from pathlib import Path
from rdflib import Graph, Literal
from .resource import (
    Allergy,
    CarePlan,
    Claim,
    ClaimTransaction,
    Condition,
    Device,
    Encounter,
    ImagingStudy,
    Immunization,
    Medication,
    Observation,
    Organization,
    Patient,
    Payer,
    PayerTransition,
    Procedure,
    Provider,
    Supply,
)
from .settings import SYN  # , DUA


class GraphBuilder:
    def __init__(self, model_path, persistence=None):  # , include_dua: bool = False):
        if persistence == "sqlite":
            self.__init_sqlite()
        else:
            self.graph = Graph()
        self.model_path = model_path
        self.setModel(self.graph)

        self.allergy_df = None
        self.carePlan_df = None
        self.claim_df = None
        self.claimTransaction_df = None
        self.condition_df = None
        self.device_df = None
        self.encounter_df = None
        self.imagingStudy_df = None
        self.immunization_df = None
        self.medication_df = None
        self.observation_df = None
        self.organization_df = None
        self.patient_df = None
        self.payer_df = None
        self.payerTransition_df = None
        self.procedure_df = None
        self.provider_df = None
        self.supply_df = None

        # self.include_dua = include_dua
        # self.dua_class = None
        # self.dua_df = None

    def build(self):
        self.convertAllergy(self.allergy_df, self.graph)
        self.convertCarePlan(self.carePlan_df, self.graph)
        self.convertClaim(self.claim_df, self.graph)
        self.convertClaimTransaction(self.claimTransaction_df, self.graph)
        self.convertCondition(self.condition_df, self.graph)
        self.convertDevice(self.device_df, self.graph)
        self.convertEncounter(self.encounter_df, self.graph)
        self.convertImagingStudy(self.imagingStudy_df, self.graph)
        self.convertImmunization(self.immunization_df, self.graph)
        self.convertMedication(self.medication_df, self.graph)
        self.convertObservation(self.observation_df, self.graph)
        self.convertOrganization(self.organization_df, self.graph)
        self.convertPatient(self.patient_df, self.graph)
        self.convertPayer(self.payer_df, self.graph)
        self.convertPayerTransition(self.payerTransition_df, self.graph)
        self.convertProcedure(self.procedure_df, self.graph)
        self.convertProvider(self.provider_df, self.graph)
        self.convertSupply(self.supply_df, self.graph)

        # if self.include_dua:
        #    self.convert_dua()

        return self.graph

    def setModel(self, graph):
        graph.parse(self.model_path, format="n3")
        graph.bind("syn", SYN)
        # self.graph.bind("", SYN)
        # self.namespace_manager = self.graph.namespace_manager

        print(f"Model has {len(self.graph)} triples.")

    def convertAllergy(self, allergy_df=None, graph=None):
        if allergy_df is not None and graph is not None:
            allergy = Allergy(allergy_df)
            allergy.convert(graph)
        else:
            print("allergy_df is not set.")

    def convertCarePlan(self, careplan_df=None, graph=None):
        if careplan_df is not None and graph is not None:
            careplan = CarePlan(careplan_df)
            careplan.convert(graph)
        else:
            print("careplan_df is not set.")

    def convertClaim(self, claim_df=None, graph=None):
        if claim_df is not None and graph is not None:
            claim = Claim(claim_df)
            claim.convert(graph)
        else:
            print("claim_df is not set.")

    def convertClaimTransaction(self, claimTransaction_df=None, graph=None):
        if claimTransaction_df is not None and graph is not None:
            claimTransaction = ClaimTransaction(claimTransaction_df)
            claimTransaction.convert(graph)
        else:
            print("claimTransaction_df is not set.")

    def convertCondition(self, condition_df=None, graph=None):
        if condition_df is not None and graph is not None:
            condition = Condition(condition_df)
            condition.convert(graph)
        else:
            print("condition_df is not set.")

    def convertDevice(self, device_df=None, graph=None):
        if device_df is not None and graph is not None:
            device = Device(device_df)
            device.convert(graph)
        else:
            print("device_df is not set.")

    def convertEncounter(self, encounter_df=None, graph=None):
        if encounter_df is not None and graph is not None:
            encounter = Encounter(encounter_df)
            encounter.convert(graph)
        else:
            print("encounter_df is not set.")

    def convertImagingStudy(self, imagingStudy_df=None, graph=None):
        if imagingStudy_df is not None and graph is not None:
            imagingStudy = ImagingStudy(imagingStudy_df)
            imagingStudy.convert(graph)
        else:
            print("imagingStudy_df is not set.")

    def convertImmunization(self, immunization_df=None, graph=None):
        if immunization_df is not None and graph is not None:
            immunization = Immunization(immunization_df)
            immunization.convert(graph)
        else:
            print("immunization_df is not set.")

    def convertMedication(self, medication_df=None, graph=None):
        if medication_df is not None and graph is not None:
            medication = Medication(medication_df)
            medication.convert(graph)
        else:
            print("medication_df is not set.")

    def convertObservation(self, observation_df=None, graph=None):
        if observation_df is not None and graph is not None:
            observation = Observation(observation_df)
            observation.convert(graph)
        else:
            print("observation_df is not set.")

    def convertOrganization(self, organization_df=None, graph=None):
        if organization_df is not None and graph is not None:
            organization = Organization(organization_df)
            organization.convert(graph)
        else:
            print("organization_df is note set.")

    def convertPatient(self, patient_df=None, graph=None):
        if patient_df is not None and graph is not None:
            patient = Patient(patient_df)
            patient.convert(graph)
        else:
            print("patient_df is not set.")

    def convertPayer(self, payer_df=None, graph=None):
        if payer_df is not None and graph is not None:
            payer = Payer(payer_df)
            payer.convert(graph)
        else:
            print("payer_df is not set.")

    def convertPayerTransition(self, payerTransition_df=None, graph=None):
        if payerTransition_df is not None and graph is not None:
            payerTransition = PayerTransition(payerTransition_df)
            payerTransition.convert(graph)
        else:
            print("payerTransition_df is not set.")

    def convertProcedure(self, procedure_df=None, graph=None):
        if procedure_df is not None and graph is not None:
            procedure = Procedure(procedure_df)
            procedure.convert(graph)
        else:
            print("procedure_df is not set.")

    def convertProvider(self, provider_df=None, graph=None):
        if provider_df is not None and graph is not None:
            provider = Provider(provider_df)
            provider.convert(graph)
        else:
            print("provider_df is not set.")

    def convertSupply(self, supply_df=None, graph=None):
        if supply_df is not None and graph is not None:
            supply = Supply(supply_df)
            supply.convert(graph)
        else:
            print("supply_df is not set.")

    # def __init_sqlite(self):
    #     self.graph = Graph("SQLAlchemy", identifier="synthea_graph")
    #     persistence_path = Path(".") / "persistence"
    #     persistence_path.mkdir(exist_ok=True)
    #     dbfile_path = persistence_path / "synthea_patient.sqlite"
    #     dburi = Literal(f"sqlite:///{dbfile_path}")
    #     if not dbfile_path.is_file():
    #         self.graph.open(dburi, create=True)
    #     else:
    #         self.graph.open(dburi)

    # def convert_dua(self, dua_df=None, graph=None):
    #     if dua_df is not None and graph is not None:
    #         dua = self.dua_class(self.dua_df)
    #         dua.convert(self.graph)
    #     else:
    #         print("DUA_df is not set.")
