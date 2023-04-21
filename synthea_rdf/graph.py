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


class GraphBuilder:
    def __init__(
        self,
        csv_dir: str,
        model_path: str,
        include_dua: bool = False,
        include_trustscore: bool = False,
    ):
        # Optional DUA resources
        self.include_dua = include_dua
        self.dua_df = None

        # Optional TrustScore resources
        self.include_trustscore = include_trustscore
        self.trustscore_df = None

        # Default Synthea resources
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

        self.graph = Graph()
        self.csv_dir = Path(csv_dir)
        self.setModel(model_path)

        # , persistence=None):
        # if persistence == "sqlite":
        #     self.__init_sqlite()
        # else:

    def serialize(self, destination: str):
        return self.graph.serialize(destination=destination)

    def build(self):
        self.readAll()
        self.convertAll()
        return self.graph

    def readAll(self):
        if Path(self.csv_dir / "allergies.csv").exists():
            self.allergy_df = pd.read_csv(self.csv_dir / "allergies.csv")
        if Path(self.csv_dir / "careplans.csv").exists():
            self.carePlan_df = pd.read_csv(self.csv_dir / "careplans.csv")
        if Path(self.csv_dir / "claims.csv").exists():
            self.claim_df = pd.read_csv(self.csv_dir / "claims.csv")
        if Path(self.csv_dir / "claims_transactions.csv").exists():
            self.claimTransaction_df = pd.read_csv(self.csv_dir / "claims_transactions.csv")
        if Path(self.csv_dir / "conditions.csv").exists():
            self.condition_df = pd.read_csv(self.csv_dir / "conditions.csv")
        if Path(self.csv_dir / "devices.csv").exists():
            self.device_df = pd.read_csv(self.csv_dir / "devices.csv")
        if Path(self.csv_dir / "encounters.csv").exists():
            self.encounter_df = pd.read_csv(self.csv_dir / "encounters.csv")
        if Path(self.csv_dir / "imaging_studies.csv").exists():
            self.imagingStudy_df = pd.read_csv(self.csv_dir / "imaging_studies.csv")
        if Path(self.csv_dir / "immunizations.csv").exists():
            self.immunization_df = pd.read_csv(self.csv_dir / "immunizations.csv")
        if Path(self.csv_dir / "medications.csv").exists():
            self.medication_df = pd.read_csv(self.csv_dir / "medications.csv")
        if Path(self.csv_dir / "observations.csv").exists():
            self.observation_df = pd.read_csv(self.csv_dir / "observations.csv")
        if Path(self.csv_dir / "organizations.csv").exists():
            self.organization_df = pd.read_csv(self.csv_dir / "organizations.csv")
        if Path(self.csv_dir / "patients.csv").exists():
            self.patient_df = pd.read_csv(self.csv_dir / "patients.csv")
        if Path(self.csv_dir / "payers.csv").exists():
            self.payer_df = pd.read_csv(self.csv_dir / "payers.csv")
        if Path(self.csv_dir / "payer_transitions.csv").exists():
            self.payerTransition_df = pd.read_csv(self.csv_dir / "payer_transitions.csv")
        if Path(self.csv_dir / "procedures.csv").exists():
            self.procedure_df = pd.read_csv(self.csv_dir / "procedures.csv")
        if Path(self.csv_dir / "providers.csv").exists():
            self.provider_df = pd.read_csv(self.csv_dir / "providers.csv")
        if Path(self.csv_dir / "supplies.csv").exists():
            self.supply_df = pd.read_csv(self.csv_dir / "supplies.csv")

        # self.carePlan_df = pd.read_csv(self.csv_dir / "careplans.csv")
        # self.claim_df = pd.read_csv(self.csv_dir / "claims.csv")
        # self.claimTransaction_df = pd.read_csv(self.csv_dir / "claims_transactions.csv")
        # self.condition_df = pd.read_csv(self.csv_dir / "conditions.csv")
        # self.device_df = pd.read_csv(self.csv_dir / "devices.csv")
        # self.encounter_df = pd.read_csv(self.csv_dir / "encounters.csv")
        # self.imagingStudy_df = pd.read_csv(self.csv_dir / "imaging_studies.csv")
        # self.immunization_df = pd.read_csv(self.csv_dir / "immunizations.csv")
        # self.medication_df = pd.read_csv(self.csv_dir / "medications.csv")
        # self.observation_df = pd.read_csv(self.csv_dir / "observations.csv")
        # self.organization_df = pd.read_csv(self.csv_dir / "organizations.csv")
        # self.patient_df = pd.read_csv(self.csv_dir / "patients.csv")
        # self.payer_df = pd.read_csv(self.csv_dir / "payers.csv")
        # self.payerTransition_df = pd.read_csv(self.csv_dir / "payer_transitions.csv")
        # self.procedure_df = pd.read_csv(self.csv_dir / "procedures.csv")
        # self.provider_df = pd.read_csv(self.csv_dir / "providers.csv")
        # self.supply_df = pd.read_csv(self.csv_dir / "supplies.csv")

        if self.include_dua:
            self.dua_df = pd.read_csv(self.csv_dir / "dua.csv")

        if self.include_trustscore:
            self.trustscore_df = pd.read_csv(self.csv_dir / "trustscore.csv")

    def setModel(self, model_path):
        self.graph.parse(model_path, format="n3")
        self.graph.bind("syn", SYN)
        if self.include_dua:
            self.graph.bind("dua", DUA)
        if self.include_trustscore:
            self.graph.bind("tst", TST)
        print(f"Model has {len(self.graph)} triples.")

    def convertAll(self):
        if self.allergy_df is not None:
            self.convertAllergy()
        if self.carePlan_df is not None:
            self.convertCarePlan()
        if self.claim_df is not None:
            self.convertClaim()
        if self.claimTransaction_df is not None:
            self.convertClaimTransaction()
        if self.condition_df is not None:
            self.convertCondition()
        if self.device_df is not None:
            self.convertDevice()
        if self.encounter_df is not None:
            self.convertEncounter()
        if self.imagingStudy_df is not None:
            self.convertImagingStudy()
        if self.immunization_df is not None:
            self.convertImmunization()
        if self.medication_df is not None:
            self.convertMedication()
        if self.observation_df is not None:
            self.convertObservation()
        if self.organization_df is not None:
            self.convertOrganization()
        if self.patient_df is not None:
            self.convertPatient()
        if self.payer_df is not None:
            self.convertPayer()
        if self.payerTransition_df is not None:
            self.convertPayerTransition()
        if self.procedure_df is not None:
            self.convertProcedure()
        if self.provider_df is not None:
            self.convertProvider()
        if self.supply_df is not None:
            self.convertSupply()

        # self.convertAllergy()
        # self.convertCarePlan()
        # self.convertClaim()
        # self.convertClaimTransaction()
        # self.convertCondition()
        # self.convertDevice()
        # self.convertEncounter()
        # self.convertImagingStudy()
        # self.convertImmunization()
        # self.convertMedication()
        # self.convertObservation()
        # self.convertOrganization()
        # self.convertPatient()
        # self.convertPayer()
        # self.convertPayerTransition()
        # self.convertProcedure()
        # self.convertProvider()
        # self.convertSupply()

        if self.include_dua:
            self.convert_dua()

        if self.include_trustscore:
            self.convert_trustscore()

    def convertAllergy(self):
        if self.allergy_df is None:
            self.allergy_df = pd.read_csv(self.csv_dir / "allergies.csv")
        allergy = Allergy(self.allergy_df)
        allergy.convert(self.graph)

    def convertCarePlan(self):
        if self.carePlan_df is None:
            self.carePlan_df = pd.read_csv(self.csv_dir / "careplans.csv")
        careplan = CarePlan(self.carePlan_df)
        careplan.convert(self.graph)

    def convertClaim(self):
        if self.claim_df is None:
            self.claim_df = pd.read_csv(self.csv_dir / "claims.csv")
        claim = Claim(self.claim_df)
        claim.convert(self.graph)

    def convertClaimTransaction(self):
        if self.claimTransaction_df is None:
            self.claimTransaction_df = pd.read_csv(
                self.csv_dir / "claims_transactions.csv"
            )
        claimTransaction = ClaimTransaction(self.claimTransaction_df)
        claimTransaction.convert(self.graph)

    def convertCondition(self):
        if self.condition_df is None:
            self.condition_df = pd.read_csv(self.csv_dir / "conditions.csv")
        condition = Condition(self.condition_df)
        condition.convert(self.graph)

    def convertDevice(self):
        if self.device_df is None:
            self.device_df = pd.read_csv(self.csv_dir / "devices.csv")
        device = Device(self.device_df)
        device.convert(self.graph)

    def convertEncounter(self):
        if self.encounter_df is None:
            self.encounter_df = pd.read_csv(self.csv_dir / "encounters.csv")
        encounter = Encounter(self.encounter_df)
        encounter.convert(self.graph)

    def convertImagingStudy(self):
        if self.imagingStudy_df is None:
            self.imagingStudy_df = pd.read_csv(self.csv_dir / "imaging_studies.csv")
        imagingStudy = ImagingStudy(self.imagingStudy_df)
        imagingStudy.convert(self.graph)

    def convertImmunization(self):
        if self.immunization_df is None:
            self.immunization_df = pd.read_csv(self.csv_dir / "immunizations.csv")
        immunization = Immunization(self.immunization_df)
        immunization.convert(self.graph)

    def convertMedication(self):
        if self.medication_df is None:
            self.medication_df = pd.read_csv(self.csv_dir / "medications.csv")
        medication = Medication(self.medication_df)
        medication.convert(self.graph)

    def convertObservation(self):
        if self.observation_df is None:
            self.observation_df = pd.read_csv(self.csv_dir / "observations.csv")
        observation = Observation(self.observation_df)
        observation.convert(self.graph)

    def convertOrganization(self):
        if self.organization_df is None:
            self.organization_df = pd.read_csv(self.csv_dir / "organizations.csv")
        organization = Organization(self.organization_df)
        organization.convert(self.graph)

    def convertPatient(self):
        if self.patient_df is None:
            self.patient_df = pd.read_csv(self.csv_dir / "patients.csv")
        patient = Patient(self.patient_df)
        patient.convert(self.graph)

    def convertPayer(self):
        if self.payer_df is None:
            self.payer_df = pd.read_csv(self.csv_dir / "payers.csv")
        payer = Payer(self.payer_df)
        payer.convert(self.graph)

    def convertPayerTransition(self):
        if self.payerTransition_df is None:
            self.payerTransition_df = pd.read_csv(
                self.csv_dir / "payer_transitions.csv"
            )
        payerTransition = PayerTransition(self.payerTransition_df)
        payerTransition.convert(self.graph)

    def convertProcedure(self):
        if self.procedure_df is None:
            self.procedure_df = pd.read_csv(self.csv_dir / "procedures.csv")
        procedure = Procedure(self.procedure_df)
        procedure.convert(self.graph)

    def convertProvider(self):
        if self.provider_df is None:
            self.provider_df = pd.read_csv(self.csv_dir / "providers.csv")
        provider = Provider(self.provider_df)
        provider.convert(self.graph)

    def convertSupply(self):
        if self.supply_df is None:
            self.supply_df = pd.read_csv(self.csv_dir / "supplies.csv")
        supply = Supply(self.supply_df)
        supply.convert(self.graph)

    def convert_dua(self):
        if self.dua_df is None:
            self.dua_df = pd.read_csv(self.csv_dir / "dua.csv")
        dua = dua_resource.DataUsageAgreement(self.dua_df)
        dua.convert(self.graph)

    def convert_trustscore(self):
        if self.trustscore_df is None:
            self.trustscore_df = pd.read_csv(self.csv_dir / "trustscore.csv")
        trust = trust_resource.TrustScore(self.trustscore_df)
        trust.convert(self.graph)

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
