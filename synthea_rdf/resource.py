from abc import ABC, abstractmethod
from rdflib.namespace import RDF
from alive_progress import alive_bar
import pandas as pd
from .settings import SYN, TST
from .trust import generate_user_trust, generate_org_trust, generate_veracity
from .literal import (
    uuid_literal,
    snomedct_literal,
    loinc_literal,
    date_literal,
    datetime_literal,
    plain_literal,
    int_literal,
    float_literal,
    udi_literal,
    dicom_uid_literal,
    dicom_dcm_literal,
    dicom_sop_literal,
)
from .uri import (
    allergy_uri,
    careplan_uri,
    claim_uri,
    claimtransaction_uri,
    condition_uri,
    patient_uri,
    encounter_uri,
    organization_uri,
    provider_uri,
    payer_uri,
    observation_uri,
    device_uri,
    imagingstudy_uri,
)


class Resource(ABC):
    @abstractmethod
    def __init__(self, df):
        self.__resource_df = df

    @property
    @abstractmethod
    def resource_df(self):
        pass

    @resource_df.setter
    @abstractmethod
    def resource_df(self, value):
        pass

    @abstractmethod
    def convert(self, graph):
        pass


class Encounter(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        """
        Object properties covered by other resource conversion:
            - syn:hasOrdered
                - [x] syn:CarePlan
                - [x] syn:Device
                - [ ] syn:Procedure
                - [ ] syn:Supply
                - [ ] syn:ImagingStudy
                - [ ] syn:Observation
            - syn:hasDiagnosed
                - [x] syn:Condition
                - [x] syn:Allergy
            - syn:hasPrescribed
                - [ ] syn:Immunization
                - [ ] syn:Medication

        """
        rows = self.__resource_df.shape[0]
        veracity = generate_veracity(rows)
        with alive_bar(rows, force_tty=True, title="Encounter Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the encounter class individual
                encounter = encounter_uri(row["Id"])
                organization = organization_uri(row["ORGANIZATION"])
                patient = patient_uri(row["PATIENT"])
                provider = provider_uri(row["PROVIDER"])
                payer = payer_uri(row["PAYER"])

                # Data Properties
                graph.add((encounter, RDF.type, SYN.Encounter))
                graph.add((encounter, SYN.id, uuid_literal(row["Id"])))
                graph.add((encounter, SYN.start, datetime_literal(row["START"])))
                graph.add((encounter, SYN.patientId, uuid_literal(row["PATIENT"])))
                graph.add((encounter, SYN.organizationId, uuid_literal(row["ORGANIZATION"])))
                graph.add((encounter, SYN.providerId, uuid_literal(row["PROVIDER"])))
                graph.add((encounter, SYN.payerId, uuid_literal(row["PAYER"])))
                graph.add((encounter, SYN.encounterClass, plain_literal(row["ENCOUNTERCLASS"])))
                graph.add((encounter, SYN.code, snomedct_literal(row["CODE"])))
                graph.add((encounter, SYN.description, plain_literal(row["DESCRIPTION"])))
                graph.add((encounter, SYN.baseEncounterCost, float_literal(row["BASE_ENCOUNTER_COST"])))
                graph.add((encounter, SYN.totalClaimCost, float_literal(row["TOTAL_CLAIM_COST"])))
                graph.add((encounter, SYN.payerCoverage, float_literal(row["PAYER_COVERAGE"])))

                # Object Properties
                graph.add((encounter, SYN.hasPatient, patient))
                graph.add((encounter, SYN.isPerformedAt, organization))
                graph.add((encounter, SYN.isPerformedBy, provider))
                graph.add((provider, SYN.hasPerformed, encounter))
                graph.add((encounter, SYN.isCoveredBy, payer))

                # Veracity
                # graph.add(
                #     (
                #         encounter,
                #         TST.credibility,
                #         float_literal(veracity.iloc[index]["credibility"]),
                #     )
                # )
                # graph.add(
                #     (
                #         encounter,
                #         TST.objectivity,
                #         float_literal(veracity.iloc[index]["objectivity"]),
                #     )
                # )
                # graph.add(
                #     (
                #         encounter,
                #         TST.trustfulness,
                #         float_literal(veracity.iloc[index]["trustfulness"]),
                #     )
                # )

                bar()


class Observation(Resource):
    """
    Object properties covered by other resource conversion:
        - [ ] syn:Patient syn:hasHistoryOf syn:Observation
        - [ ] syn:Encounter syn:hasOrdered syn:Observation
    """

    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        rows = self.__resource_df.shape[0]
        veracity = generate_veracity(rows)
        with alive_bar(rows, force_tty=True, title="Obvervation Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the observation class individual
                observation = observation_uri(index)

                # Data Properties
                graph.add((observation, RDF.type, SYN.Observation))
                graph.add((observation, SYN.dateTime, datetime_literal(row["DATE"])))
                graph.add((observation, SYN.patientId, uuid_literal(row["PATIENT"])))
                if pd.notnull(row["ENCOUNTER"]):
                    graph.add((observation, SYN.encounterId, uuid_literal(row["ENCOUNTER"])))
                graph.add((observation, SYN.code, loinc_literal(row["CODE"])))
                graph.add((observation, SYN.description, plain_literal(row["DESCRIPTION"])))
                graph.add((observation, SYN.value, plain_literal(row["VALUE"])))
                graph.add((observation, SYN.type, plain_literal(row["TYPE"])))

                # Object Properties
                if pd.notnull(row["ENCOUNTER"]):
                    graph.add((observation, SYN.isOrderedDuring, encounter_uri(row["ENCOUNTER"])))
                graph.add((observation, SYN.isAbout, patient_uri(row["PATIENT"])))

                # Veracity
                # graph.add(
                #     (
                #         observation,
                #         TST.credibility,
                #         float_literal(veracity.iloc[index]["credibility"]),
                #     )
                # )
                # graph.add(
                #     (
                #         observation,
                #         TST.objectivity,
                #         float_literal(veracity.iloc[index]["objectivity"]),
                #     )
                # )
                # graph.add(
                #     (
                #         observation,
                #         TST.trustfulness,
                #         float_literal(veracity.iloc[index]["trustfulness"]),
                #     )
                # )

                bar()


class Organization(Resource):
    # This class use TRUST_IRI for now.
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        """
        Object properties covered by other resource conversion:
            - [x] syn:Organization syn:hasClaimTransaction syn:ClaimTransaction
            - [ ] syn:Organization syn:isResponsibleFor syn:Encounter
            - [x] syn:Organization syn:hasEmployed syn:Provider
        """
        rows = self.__resource_df.shape[0]
        reputation = generate_org_trust(rows)
        with alive_bar(rows, force_tty=True, title="Organization Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the organization class individual
                organization = organization_uri(row["Id"])

                # Data Properties
                graph.add((organization, RDF.type, SYN.Organization))
                graph.add((organization, SYN.id, uuid_literal(row["Id"])))
                graph.add((organization, SYN.name, plain_literal(row["NAME"])))
                graph.add((organization, SYN.address, plain_literal(row["ADDRESS"])))
                graph.add((organization, SYN.city, plain_literal(row["CITY"])))
                graph.add((organization, SYN.revenue, float_literal(row["REVENUE"])))
                graph.add((organization, SYN.utilization, int_literal(row["UTILIZATION"])))

                # Object Properties

                # Reputation
                # graph.add(
                #     (
                #         organization,
                #         TST.reputation,
                #         float_literal(reputation.iloc[index]["reputation"]),
                #     )
                # )

                bar()


class Patient(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        """
        Object properties covered by other resource conversion:
            - [x] syn:Patient syn:hasAllergy syn:Allergy
            - syn:Patient syn:hasHistoryOf
                - [ ] syn:Observation
                - [x] syn:Condition
                - [ ] syn:Procedure
                - [ ] syn:Medication
                - [ ] syn:Immunization
                - [ ] syn:ImagingStudy
                - [ ] syn:Supply
            - [x] syn:Patient syn:isMeasuredBy syn:Device
            - [x] syn:Patient syn:hasCarePlan syn:CarePlan
            - [ ] syn:Patient syn:hasEncounter syn:Encounter
            - [x] syn:Patient syn:hasClaim syn:Claim
            - [x] syn:Patient syn:hasClaimTransaction syn:ClaimTransaction
            - [ ] syn:Patient syn:hasPayerTransitionHistory syn:PayerTransition
        """
        rows = self.__resource_df.shape[0]
        user_trust = generate_user_trust(rows)
        with alive_bar(rows, force_tty=True, title="Patient Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the patient class individual
                patient = patient_uri(row["Id"])

                # Data Properties
                # graph.add((patient, RDF.type, SYN.Patient))  # type
                graph.add((patient, SYN.id, uuid_literal(row["Id"])))  # id
                graph.add((patient, SYN.birthdate, date_literal(row["BIRTHDATE"])))  # birthdate
                graph.add((patient, SYN.ssn, plain_literal(row["SSN"])))  # ssn
                graph.add((patient, SYN.first, plain_literal(row["FIRST"])))
                graph.add((patient, SYN.last, plain_literal(row["LAST"])))
                graph.add((patient, SYN.race, plain_literal(row["RACE"])))
                graph.add((patient, SYN.ethnicity, plain_literal(row["ETHNICITY"])))
                graph.add((patient, SYN.gender, plain_literal(row["GENDER"])))
                graph.add((patient, SYN.birthplace, plain_literal(row["BIRTHPLACE"])))
                graph.add((patient, SYN.address, plain_literal(row["ADDRESS"])))
                graph.add((patient, SYN.city, plain_literal(row["CITY"])))
                graph.add((patient, SYN.state, plain_literal(row["STATE"])))
                graph.add((patient, SYN.healthcareExpense, plain_literal(row["HEALTHCARE_EXPENSES"])))
                graph.add((patient, SYN.healthcareCoverage, plain_literal(row["HEALTHCARE_COVERAGE"])))
                graph.add((patient, SYN.income, int_literal(row["INCOME"])))

                # User Trust
                # graph.add(
                #     (
                #         patient,
                #         TST.behavior,
                #         float_literal(user_trust.iloc[index]["behavioral_trust"]),
                #     )
                # )
                # graph.add(
                #     (
                #         patient,
                #         TST.identity,
                #         float_literal(user_trust.iloc[index]["identity_trust"]),
                #     )
                # )

                bar()


class Provider(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        """
        Object properties covered by other resource conversion:
            - [x] syn:Provider syn:hasPerformed syn:Encounter
            - [x] syn:Provider syn:hasClaimTransaction syn:ClaimTransaction
            - [x] syn:Provider syn:hasFiled syn:Claim
        """
        rows = self.__resource_df.shape[0]
        user_trust = generate_user_trust(rows)
        with alive_bar(rows, force_tty=True, title="Provider Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the provider class individual
                provider = provider_uri(row["Id"])
                organization = organization_uri(row["ORGANIZATION"])  # for object property

                # Data Properties
                graph.add((provider, RDF.type, SYN.Provider))
                graph.add((provider, SYN.id, uuid_literal(row["Id"])))
                graph.add((provider, SYN.organizationId, uuid_literal(row["ORGANIZATION"])))
                graph.add((provider, SYN.name, plain_literal(row["NAME"])))
                graph.add((provider, SYN.gender, plain_literal(row["GENDER"])))
                graph.add((provider, SYN.speciality, plain_literal(row["SPECIALITY"])))
                graph.add((provider, SYN.address, plain_literal(row["ADDRESS"])))
                graph.add((provider, SYN.city, plain_literal(row["CITY"])))
                graph.add((provider, SYN.utilization, int_literal(row["UTILIZATION"])))

                # Object Properties
                graph.add((provider, SYN.isAffiliatedWith, organization_uri(row["ORGANIZATION"])))
                graph.add((organization, SYN.hasEmployed, provider))

                # User Trust
                # graph.add(
                #     (
                #         provider,
                #         TST.behavior,
                #         float_literal(user_trust.iloc[index]["behavioral_trust"]),
                #     )
                # )
                # graph.add(
                #     (
                #         provider,
                #         TST.identity,
                #         float_literal(user_trust.iloc[index]["identity_trust"]),
                #     )
                # )

                bar()


class Payer(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        """
        Object properties covered by other resource conversion:
            - [ ] syn:Payer syn:hasCovered syn:Encounter
            - [ ] syn:Payer syn:hasCovered syn:Medication
            - [ ] syn:Payer syn:hasPayerTransitionHistory syn:PayerTransition
        """
        rows = self.__resource_df.shape[0]
        user_trust = generate_user_trust(rows)
        with alive_bar(rows, force_tty=True, title="Payer Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the payer class individual
                payer = payer_uri(row["Id"])

                # Data Properties
                # graph.add((payer, RDF.type, SYN.Payer))  # type
                graph.add((payer, SYN.id, uuid_literal(row["Id"])))  # id
                graph.add((payer, SYN.name, plain_literal(row["NAME"])))
                graph.add((payer, SYN.amountCovered, float_literal(row["AMOUNT_COVERED"])))
                graph.add((payer, SYN.amountUncovered, float_literal(row["AMOUNT_UNCOVERED"])))
                graph.add((payer, SYN.revenue, float_literal(row["REVENUE"])))
                graph.add((payer, SYN.coveredEncounters, int_literal(row["COVERED_ENCOUNTERS"])))
                graph.add((payer, SYN.uncoveredEncounters, int_literal(row["UNCOVERED_ENCOUNTERS"])))
                graph.add((payer, SYN.coveredMedications, int_literal(row["COVERED_MEDICATIONS"])))
                graph.add((payer, SYN.uncoveredMedications, int_literal(row["UNCOVERED_MEDICATIONS"])))
                graph.add((payer, SYN.coveredProcedures, int_literal(row["COVERED_PROCEDURES"])))
                graph.add((payer, SYN.uncoveredProcedures, int_literal(row["UNCOVERED_PROCEDURES"])))
                graph.add((payer, SYN.coveredImmunizations, int_literal(row["COVERED_IMMUNIZATIONS"])))
                graph.add((payer, SYN.uncoveredImmunizations, int_literal(row["UNCOVERED_IMMUNIZATIONS"])))
                graph.add((payer, SYN.uniqueCustomers, int_literal(row["UNIQUE_CUSTOMERS"])))
                graph.add((payer, SYN.qolsAvg, float_literal(row["QOLS_AVG"])))
                graph.add((payer, SYN.memberMonths, int_literal(row["MEMBER_MONTHS"])))

                # Object Properties

                # User Trust
                # graph.add(
                #     (
                #         payer,
                #         TST.behavior,
                #         float_literal(user_trust.iloc[index]["behavioral_trust"]),
                #     )
                # )
                # graph.add(
                #     (
                #         payer,
                #         TST.identity,
                #         float_literal(user_trust.iloc[index]["identity_trust"]),
                #     )
                # )

                bar()


class Allergy(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        """
        Issue:
            - [ ] There are no allergy data in the dataset (10 patients)
                  so I should test this conversion with a larger dataset.
            - [ ] syn:code should be decided by the syn:system
        """
        rows = self.__resource_df.shape[0]
        with alive_bar(rows, force_tty=True, title="Allergy Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the allergy class individual
                allergy = allergy_uri(row["Id"])
                patient = patient_uri(row["PATIENT"])
                encounter = encounter_uri(row["ENCOUNTER"])

                # Data Properties
                graph.add((allergy, SYN.start, date_literal(row["START"])))
                graph.add((allergy, SYN.patientId, uuid_literal(row["PATIENT"])))
                graph.add((allergy, SYN.encounterId, uuid_literal(row["ENCOUNTER"])))
                graph.add((allergy, SYN.system, plain_literal(row["SYSTEM"])))
                graph.add((allergy, SYN.description, plain_literal(row["DESCRIPTION"])))

                # Object Properties
                graph.add((allergy, SYN.isAbout, patient))
                graph.add((patient, SYN.hasAllergy, allergy))
                graph.add((allergy, SYN.isDiagnosedDuring, encounter))
                graph.add((encounter, SYN.hasDiagnosed, allergy))

                bar()


class CarePlan(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        rows = self.__resource_df.shape[0]
        with alive_bar(rows, force_tty=True, title="CarePlan Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the careplan class individual
                careplan = careplan_uri(row["Id"])
                patient = patient_uri(row["PATIENT"])
                encounter = encounter_uri(row["ENCOUNTER"])

                # Data Properties
                graph.add((careplan, SYN.start, date_literal(row["START"])))
                graph.add((careplan, SYN.patientId, uuid_literal(row["PATIENT"])))
                graph.add((careplan, SYN.encounterId, uuid_literal(row["ENCOUNTER"])))
                graph.add((careplan, SYN.code, snomedct_literal(row["CODE"])))
                graph.add((careplan, SYN.description, plain_literal(row["DESCRIPTION"])))
                graph.add((careplan, SYN.reasonCode, snomedct_literal(row["REASONCODE"])))
                graph.add((careplan, SYN.reasonDescription, plain_literal(row["REASONDESCRIPTION"])))

                # Object Properties
                graph.add((careplan, SYN.isAbout, patient))
                graph.add((patient, SYN.hasCarePlan, careplan))
                graph.add((careplan, SYN.isOrderedDuring, encounter))
                graph.add((encounter, SYN.hasOrdered, careplan))

                bar()


class Claim(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        """
        Object properties covered by other resource conversion:
            - [x] syn:Claim syn:hasTransaction syn:ClaimTransaction
        """
        rows = self.__resource_df.shape[0]
        with alive_bar(rows, force_tty=True, title="Claim Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the claim class individual
                claim = claim_uri(row["Id"])
                patient = patient_uri(row["PATIENTID"])
                provider = provider_uri(row["PROVIDERID"])

                # Data Properties
                graph.add((claim, SYN.id, uuid_literal(row["Id"])))
                graph.add((claim, SYN.patientId, uuid_literal(row["PATIENTID"])))
                graph.add((claim, SYN.providerId, uuid_literal(row["PROVIDERID"])))
                graph.add((claim, SYN.departmentId, uuid_literal(row["DEPARTMENTID"])))
                graph.add((claim, SYN.patientDepartmentId, uuid_literal(row["PATIENTDEPARTMENTID"])))
                graph.add((claim, SYN.currentIllnessDate, datetime_literal(row["CURRENTILLNESSDATE"])))
                graph.add((claim, SYN.serviceDate, datetime_literal(row["SERVICEDATE"])))

                # Object Properties
                graph.add((claim, SYN.isAssociatedWith, patient))
                graph.add((patient, SYN.hasClaim, claim))
                graph.add((claim, SYN.isFiledBy, provider))
                graph.add((provider, SYN.hasFiled, claim))


class ClaimTransaction(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        rows = self.__resource_df.shape[0]
        with alive_bar(rows, force_tty=True, title="ClaimTransaction Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the claimtransaction class individual
                claimtransaction = claimtransaction_uri(row["ID"])
                claim = claim_uri(row["CLAIMID"])
                patient = patient_uri(row["PATIENTID"])
                provider = provider_uri(row["PROVIDERID"])
                organization = organization_uri(row["PLACEOFSERVICE"])

                # Data Properties
                graph.add((claimtransaction, SYN.id, uuid_literal(row["ID"])))
                graph.add((claimtransaction, SYN.claimId, uuid_literal(row["CLAIMID"])))
                graph.add((claimtransaction, SYN.chargeId, uuid_literal(row["CHARGEID"])))
                graph.add((claimtransaction, SYN.patientId, uuid_literal(row["PATIENTID"])))
                graph.add((claimtransaction, SYN.type, plain_literal(row["TYPE"])))
                graph.add((claimtransaction, SYN.placeOfService, uuid_literal(row["PLACEOFSERVICE"])))
                graph.add((claimtransaction, SYN.procedureCode, snomedct_literal(row["PROCEDURECODE"])))
                graph.add((claimtransaction, SYN.providerId, uuid_literal(row["PROVIDERID"])))

                # Object Properties
                graph.add((claimtransaction, SYN.isTransactionFor, claim))
                graph.add((claim, SYN.hasTransaction, claimtransaction))
                graph.add((claimtransaction, SYN.isAssociatedWith, patient))
                graph.add((patient, SYN.hasClaimTransaction, claimtransaction))
                graph.add((claimtransaction, SYN.isAssociatedWith, provider))
                graph.add((provider, SYN.hasClaimTransaction, claimtransaction))
                graph.add((claimtransaction, SYN.hasPlaceOfService, organization))
                graph.add((organization, SYN.hasClaimTransaction, claimtransaction))

                bar()


class Condition(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        rows = self.__resource_df.shape[0]
        with alive_bar(rows, force_tty=True, title="Condition Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the condition class individual
                condition = condition_uri(index)
                patient = patient_uri(row["PATIENT"])
                encounter = encounter_uri(row["ENCOUNTER"])

                # Data Properties
                graph.add((condition, SYN.startDate, date_literal(row["START"])))
                graph.add((condition, SYN.patientId, uuid_literal(row["PATIENT"])))
                graph.add((condition, SYN.encounterId, uuid_literal(row["ENCOUNTER"])))
                graph.add((condition, SYN.code, snomedct_literal(row["CODE"])))
                graph.add((condition, SYN.description, plain_literal(row["DESCRIPTION"])))

                # Object Properties
                graph.add((condition, SYN.isAbout, patient))
                graph.add((patient, SYN.hasHistoryOf, condition))
                graph.add((condition, SYN.isDiagnosedDuring, encounter))
                graph.add((encounter, SYN.hasDiagnosed, condition))

                bar()


class Device(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        rows = self.__resource_df.shape[0]
        with alive_bar(rows, force_tty=True, title="Device Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the device class individual
                device = device_uri(index)
                patient = patient_uri(row["PATIENT"])
                encounter = encounter_uri(row["ENCOUNTER"])

                # Data Properties
                graph.add((device, SYN.startDateTime, datetime_literal(row["START"])))
                graph.add((device, SYN.patientId, uuid_literal(row["PATIENT"])))
                graph.add((device, SYN.encounterId, uuid_literal(row["ENCOUNTER"])))
                graph.add((device, SYN.code, snomedct_literal(row["CODE"])))
                graph.add((device, SYN.description, plain_literal(row["DESCRIPTION"])))
                graph.add((device, SYN.udi, udi_literal(row["UDI"])))

                # Object Properties
                graph.add((device, SYN.hasMeasured, patient))
                graph.add((patient, SYN.isMeasuredBy, device))
                graph.add((device, SYN.isOrderedDuring, encounter))
                graph.add((encounter, SYN.hasOrdered, device))

                bar()


class ImagingStudy(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        """
        Issue:
            - [ ] There are no ImagingStudy data in the dataset (10 patients)
                  so I should test this conversion with a larger dataset.
        """
        rows = self.__resource_df.shape[0]
        with alive_bar(rows, force_tty=True, title="ImagingStudy Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Create name of the imagingstudy class individual
                imagingstudy = imagingstudy_uri(index)
                patient = patient_uri(row["PATIENT"])
                encounter = encounter_uri(row["ENCOUNTER"])

                # Data Properties
                graph.add((imagingstudy, SYN.id, uuid_literal(row["Id"])))
                graph.add((imagingstudy, SYN.dateTime, datetime_literal(row["DATE"])))
                graph.add((imagingstudy, SYN.patientId, uuid_literal(row["PATIENT"])))
                graph.add((imagingstudy, SYN.encounterId, uuid_literal(row["ENCOUNTER"])))
                graph.add((imagingstudy, SYN.seriesUid, dicom_uid_literal(row["SERIES_UID"])))
                graph.add((imagingstudy, SYN.bodySiteCode, snomedct_literal(row["BODYSITE_CODE"])))
                graph.add((imagingstudy, SYN.bodySiteDescription, plain_literal(row["BODYSITE_DESCRIPTION"])))
                graph.add((imagingstudy, SYN.modalityCode, dicom_dcm_literal(row["MODALITY_CODE"])))
                graph.add((imagingstudy, SYN.modalityDescription, plain_literal(row["MODALITY_DESCRIPTION"])))
                graph.add((imagingstudy, SYN.instanceUid, dicom_uid_literal(row["INSTANCE_UID"])))
                graph.add((imagingstudy, SYN.sopCode, dicom_sop_literal(row["SOP_CODE"])))
                graph.add((imagingstudy, SYN.sopDescription, plain_literal(row["SOP_DESCRIPTION"])))
                graph.add((imagingstudy, SYN.procedureCode, snomedct_literal(row["PROCEDURE_CODE"])))

                # Object Properties
                graph.add((imagingstudy, SYN.isAbout, patient))
                graph.add((patient, SYN.hasHistoryOf, imagingstudy))
                graph.add((imagingstudy, SYN.isOrderedDuring, encounter))
                graph.add((encounter, SYN.hasOrdered, imagingstudy))

                bar()


class Immunization(Resource):
    ...


class Medication(Resource):
    ...


class PayerTransition(Resource):
    ...


class Procedure(Resource):
    ...


class Supply(Resource):
    ...
