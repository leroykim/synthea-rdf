from abc import ABC, abstractmethod
from datetime import datetime
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from alive_progress import alive_bar
import pandas as pd
from .settings import SYN, TST
from .trust import generate_user_trust, generate_org_trust, generate_veracity


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
                - [ ] syn:CarePlan
                - [ ] syn:Device
                - [ ] syn:Procedure
                - [ ] syn:Supply
                - [ ] syn:ImagingStudy
                - [ ] syn:Observation
            - syn:hasDiagnosed
                - [ ] syn:Condition
                - [ ] syn:Allergy
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
            - [ ] syn:Organization syn:hasClaimTransaction syn:ClaimTransaction
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
            - [ ] syn:Patient syn:isAllergicTo syn:Allergy
            - syn:Patient syn:hasHistoryOf
                - [ ] syn:Observation
                - [ ] syn:Condition
                - [ ] syn:Procedure
                - [ ] syn:Medication
                - [ ] syn:Immunization
                - [ ] syn:ImagingStudy
                - [ ] syn:Supply
            - [ ] syn:Patient syn:isMeasuredBy syn:Device
            - [ ] syn:Patient syn:isMonitoredBy syn:CarePlan
            - [ ] syn:Patient syn:hasEncounter syn:Encounter
            - [ ] syn:Patient syn:hasClaim syn:Claim
            - [ ] syn:Patient syn:hasClaimTransaction syn:ClaimTransaction
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
            - [ ] syn:Provider syn:hasClaimTransaction syn:ClaimTransaction
            - [ ] syn:Provider syn:hasFiled syn:Claim
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
        rows = self.__resource_df.shape[0]
        user_trust = generate_user_trust(rows)
        with alive_bar(rows, force_tty=True, title="Payer Conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                # Synthea
                payer = payer_uri(row["Id"])
                graph.add((payer, RDF.type, SYN.Payer))  # type
                graph.add((payer, SYN.payer_id, plain_literal(row["Id"])))  # id
                graph.add((payer, SYN.name, plain_literal(row["NAME"])))  # name
                # address
                graph.add((payer, SYN.address, plain_literal(row["ADDRESS"])))
                graph.add((payer, SYN.city, plain_literal(row["CITY"])))  # city
                graph.add(
                    (
                        payer,
                        SYN.state_headquartered,
                        plain_literal(row["STATE_HEADQUARTERED"]),
                    )
                )
                graph.add((payer, SYN.zip, plain_literal(row["ZIP"])))
                graph.add((payer, SYN.phone, plain_literal(row["PHONE"])))
                graph.add((payer, SYN.amount_covered, float_literal(row["AMOUNT_COVERED"])))
                graph.add(
                    (
                        payer,
                        SYN.amount_uncovered,
                        float_literal(row["AMOUNT_UNCOVERED"]),
                    )
                )
                graph.add((payer, SYN.revenue, float_literal(row["REVENUE"])))
                graph.add(
                    (
                        payer,
                        SYN.covered_encounters,
                        int_literal(row["COVERED_ENCOUNTERS"]),
                    )
                )
                graph.add(
                    (
                        payer,
                        SYN.uncovered_encounters,
                        int_literal(row["UNCOVERED_ENCOUNTERS"]),
                    )
                )
                graph.add(
                    (
                        payer,
                        SYN.covered_medications,
                        int_literal(row["COVERED_MEDICATIONS"]),
                    )
                )
                graph.add(
                    (
                        payer,
                        SYN.uncovered_medications,
                        int_literal(row["UNCOVERED_MEDICATIONS"]),
                    )
                )
                graph.add(
                    (
                        payer,
                        SYN.covered_procedures,
                        int_literal(row["COVERED_PROCEDURES"]),
                    )
                )
                graph.add(
                    (
                        payer,
                        SYN.uncovered_procedures,
                        int_literal(row["UNCOVERED_PROCEDURES"]),
                    )
                )
                graph.add(
                    (
                        payer,
                        SYN.covered_immunizations,
                        int_literal(row["COVERED_IMMUNIZATIONS"]),
                    )
                )
                graph.add(
                    (
                        payer,
                        SYN.uncovered_immunizations,
                        int_literal(row["UNCOVERED_IMMUNIZATIONS"]),
                    )
                )
                graph.add((payer, SYN.unique_customers, int_literal(row["UNIQUE_CUSTOMERS"])))
                graph.add((payer, SYN.qols_avg, float_literal(row["QOLS_AVG"])))
                graph.add((payer, SYN.member_months, int_literal(row["MEMBER_MONTHS"])))

                # User Trust
                graph.add(
                    (
                        payer,
                        TST.behavior,
                        float_literal(user_trust.iloc[index]["behavioral_trust"]),
                    )
                )
                graph.add(
                    (
                        payer,
                        TST.identity,
                        float_literal(user_trust.iloc[index]["identity_trust"]),
                    )
                )

                bar()


##################
# HELPER METHODS #
##################

# Literal helper methods


def uuid_literal(string):
    # https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.namespace.html#rdflib.namespace.Namespace
    return Literal(str(string), datatype=SYN["urn:uuid"])


def snomedct_literal(string):
    return Literal(str(string), datatype=SYN["snomed:SNOMED-CT"])


def loinc_literal(string):
    return Literal(str(string), datatype=SYN["loinc:LOINC"])


def date_literal(date):
    return Literal(datetime.strptime(date, "%Y-%m-%d"), datatype=XSD.dateTime)


def datetime_literal(date):
    return Literal(datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)


def plain_literal(string):
    return Literal(str(string), datatype=RDF.PlainLiteral)


def int_literal(string):
    return Literal(str(string), datatype=XSD.int)


def float_literal(string):
    return Literal(str(string), datatype=XSD.float)


# URI helper methods


def careplan_uri(id):
    return URIRef(f"{SYN}carePlan_{id}")


def patient_uri(id):
    return URIRef(f"{SYN}patient_{id}")


def encounter_uri(encounter_id):
    return URIRef(f"{SYN}encounter_{encounter_id}")


def organization_uri(organization_id):
    return URIRef(f"{SYN}organization_{organization_id}")


def provider_uri(provider_id):
    return URIRef(f"{SYN}provider_{provider_id}")


def payer_uri(payer_id):
    return URIRef(f"{SYN}payer_{payer_id}")


def observation_uri(observation_id):
    return URIRef(f"{SYN}observation_{observation_id}")
