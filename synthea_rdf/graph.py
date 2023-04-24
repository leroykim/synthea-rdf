from pathlib import Path
from rdflib import Graph
import pandas as pd
from dua import resource as dua_resource
from trustscore import resource as trust_resource
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
from abstract.namespace import SYN, DUA, TST
from .memory import usage


class GraphBuilder:
    def __init__(
        self,
        csv_dir: str,
        model_path: str,
        include_dua: bool = False,
        include_trustscore: bool = False,
    ):
        self.RESOURCE_DICT = {
            "allergies.csv": self.convertAllergy,
            "careplans.csv": self.convertCarePlan,
            "claims.csv": self.convertClaim,
            "claim_transactions.csv": self.convertClaimTransaction,
            "conditions.csv": self.convertCondition,
            "devices.csv": self.convertDevice,
            "encounters.csv": self.convertEncounter,
            "imaging_studies.csv": self.convertImagingStudy,
            "immunizations.csv": self.convertImmunization,
            "medications.csv": self.convertMedication,
            "observations.csv": self.convertObservation,
            "organizations.csv": self.convertOrganization,
            "patients.csv": self.convertPatient,
            "payer_transitions.csv": self.convertPayerTransition,
            "payers.csv": self.convertPayer,
            "procedures.csv": self.convertProcedure,
            "providers.csv": self.convertProvider,
            "supplies.csv": self.convertSupply,
        }
        # Optional Trustscore and DUA
        self.include_dua = include_dua
        self.include_trustscore = include_trustscore

        self.graph = Graph()
        self.csv_dir = Path(csv_dir)
        self.setModel(model_path)

    def serialize(self, destination: str):
        return self.graph.serialize(destination=destination)

    def build(self):
        self.convert()
        return self.graph

    def convert(self):
        for file, func in self.RESOURCE_DICT.items():
            resource_path = Path(self.csv_dir / file)
            if Path(resource_path).exists():
                resource_df = pd.read_csv(resource_path)
                func(resource_df)
                usage()
                del resource_df
                usage()

        if self.include_dua:
            dua_df = pd.read_csv(self.csv_dir / "dua.csv")
            self.convertDUA(dua_df)
            usage()
            del dua_df
            usage()

        if self.include_trustscore:
            trustscore_df = pd.read_csv(self.csv_dir / "trustscore.csv")
            self.convertTrustscore(trustscore_df)
            usage()
            del trustscore_df

    def setModel(self, model_path):
        self.graph.parse(model_path, format="n3")
        self.graph.bind("syn", SYN)
        if self.include_dua:
            self.graph.bind("dua", DUA)
        if self.include_trustscore:
            self.graph.bind("tst", TST)
        print(f"Model has {len(self.graph)} triples.")

    def convertAllergy(self, allergy_df=None):
        allergy = Allergy(allergy_df)
        allergy.convert(self.graph)

    def convertCarePlan(self, carePlan_df=None):
        careplan = CarePlan(carePlan_df)
        careplan.convert(self.graph)

    def convertClaim(self, claim_df=None):
        claim = Claim(claim_df)
        claim.convert(self.graph)

    def convertClaimTransaction(self, claimTransaction_df=None):
        claimTransaction = ClaimTransaction(claimTransaction_df)
        claimTransaction.convert(self.graph)

    def convertCondition(self, condition_df=None):
        condition = Condition(condition_df)
        condition.convert(self.graph)

    def convertDevice(self, device_df=None):
        device = Device(device_df)
        device.convert(self.graph)

    def convertEncounter(self, encounter_df=None):
        encounter = Encounter(encounter_df)
        encounter.convert(self.graph)

    def convertImagingStudy(self, imagingStudy_df=None):
        imagingStudy = ImagingStudy(imagingStudy_df)
        imagingStudy.convert(self.graph)

    def convertImmunization(self, immunization_df=None):
        immunization = Immunization(immunization_df)
        immunization.convert(self.graph)

    def convertMedication(self, medication_df=None):
        medication = Medication(medication_df)
        medication.convert(self.graph)

    def convertObservation(self, observation_df=None):
        observation = Observation(observation_df)
        observation.convert(self.graph)

    def convertOrganization(self, organization_df=None):
        organization = Organization(organization_df)
        organization.convert(self.graph)

    def convertPatient(self, patient_df=None):
        patient = Patient(patient_df)
        patient.convert(self.graph)

    def convertPayer(self, payer_df=None):
        payer = Payer(payer_df)
        payer.convert(self.graph)

    def convertPayerTransition(self, payerTransition_df=None):
        payerTransition = PayerTransition(payerTransition_df)
        payerTransition.convert(self.graph)

    def convertProcedure(self, procedure_df=None):
        procedure = Procedure(procedure_df)
        procedure.convert(self.graph)

    def convertProvider(self, provider_df=None):
        provider = Provider(provider_df)
        provider.convert(self.graph)

    def convertSupply(self, supply_df=None):
        supply = Supply(supply_df)
        supply.convert(self.graph)

    def convertDUA(self, dua_df):
        dua = dua_resource.DataUsageAgreement(dua_df)
        dua.convert(self.graph)

    def convertTrustscore(self, trustscore_df):
        trust = trust_resource.TrustScore(trustscore_df)
        trust.convert(self.graph)
