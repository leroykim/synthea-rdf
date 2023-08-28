from datetime import date, time, datetime
from owlready2 import get_ontology, DataProperty
from synthea_rdf.util.configuration import Configuration
from synthea_rdf.definitions.classes import *
from synthea_rdf.definitions.datatypes import *

synthea_ontology = get_ontology(Configuration.synthea_namespace)

with synthea_ontology:
    """
    Allergy data properties:
    - description
    - encounterId
    - startDate
    - system
    - patientId
    """

    class description(DataProperty):
        domain = [
            Allergy,
            CarePlan,
            Condition,
            Device,
            Encounter,
            Immunization,
            Medication,
            Observation,
            Procedure,
            Supply,
        ]
        range = [str]

    class encounterId(DataProperty):
        # Needs custom datatype
        domain = [
            Allergy,
            CarePlan,
            Condition,
            Device,
            ImagingStudy,
            Immunization,
            Medication,
            Observation,
            Procedure,
            Supply,
        ]
        range = [URN_UUID]

    class startDate(DataProperty):
        domain = [Allergy, Condition]
        range = [datetime]

    class system(DataProperty):
        domain = [Allergy]
        range = [str]

    class patientId(DataProperty):
        # Needs custom datatype
        domain = [
            Allergy,
            CarePlan,
            Claim,
            ClaimTransaction,
            Condition,
            Device,
            Encounter,
            Immunization,
            Medication,
            Observation,
            PayerTransition,
            Procedure,
            Supply,
        ]
        range = [URN_UUID]

    """
    CarePlan data properties:
    - code
    - description: defined in Allergy
    - encounterId: defined in Allergy
    - patientId: defined in Allergy
    - reasonCode
    - reasonDescription
    - start
    """

    class code(DataProperty):
        domain = [
            CarePlan,
            Condition,
            Device,
            Encounter,
            Immunization,
            Medication,
            Observation,
            Procedure,
            Supply,
        ]
        range = [SNOMED_CT]

    class reasonCode(DataProperty):
        domain = [CarePlan]
        range = [SNOMED_CT]

    class reasonDescription(DataProperty):
        domain = [CarePlan]
        range = [str]

    class start(DataProperty):
        domain = [CarePlan]
        range = [datetime]

    """
    Claim data properties:
    - currentIllnessDate
    - departmentId
    - id
    - patientDepartmentId
    - patientId: defined in Allergy
    - providerId
    - serviceDate
    """

    class currentIllnessDate(DataProperty):
        domain = [Claim]
        range = [datetime]

    class departmentId(DataProperty):
        domain = [Claim]
        range = [URN_UUID]

    class id(DataProperty):
        domain = [
            Claim,
            ClaimTransaction,
            Encounter,
            ImagingStudy,
            Organization,
            Patient,
            Payer,
            Provider,
        ]
        range = [URN_UUID]

    class patientDepartmentId(DataProperty):
        domain = [Claim]
        range = [URN_UUID]

    class providerId(DataProperty):
        domain = [Claim, ClaimTransaction, Encounter, ImagingStudy]
        range = [URN_UUID]

    class serviceDate(DataProperty):
        domain = [Claim]
        range = [datetime]

    """
    ClaimTransaction data properties:
    - chargeId
    - claimId
    - id: defined in Claim
    - patientId: defined in Allergy
    - placeOfService
    - procedureCode
    - providerId: defined in Claim
    - type
    """

    class chargeId(DataProperty):
        domain = [ClaimTransaction]
        range = [URN_UUID]

    class claimId(DataProperty):
        domain = [ClaimTransaction]
        range = [URN_UUID]

    class placeOfService(DataProperty):
        domain = [ClaimTransaction]
        range = [URN_UUID]

    class procedureCode(DataProperty):
        domain = [ClaimTransaction]
        range = [SNOMED_CT]

    class type(DataProperty):
        domain = [ClaimTransaction, Observation]
        range = [str]

    """
    Condition data properties:
    - code: defined in CarePlan
    - description: defined in Allergy
    - encounterId: defined in Allergy
    - patientId: defined in Allergy
    - startDate: defined in Allergy
    """

    """
    Device data properties:
    - code: defined in CarePlan
    - description: defined in Allergy
    - encounterId: defined in Allergy
    - patientId: defined in Allergy
    - startDateTime
    - udi
    """

    class startDateTime(DataProperty):
        domain = [Device, Encounter, Medication, Procedure]
        range = [datetime]

    class udi(DataProperty):
        domain = [Device]
        range = [FDA_UDI]

    """
    Encounter data properties:
    - baseEncounterCost
    - code: defined in CarePlan
    - description: defined in Allergy
    - encounterClass
    - id: defined in Claim
    - organizationId
    - patientId: defined in Allergy
    - payerCoverage
    - payerId
    - providerId: defined in Claim
    - startDateTime: defined in Device
    - totalClaimCost
    """

    class baseEncounterCost(DataProperty):
        domain = [Encounter]
        range = [float]

    class encounterClass(DataProperty):
        domain = [Encounter]
        range = [str]

    class organizationId(DataProperty):
        domain = [Encounter, Provider]
        range = [URN_UUID]

    class payerCoverage(DataProperty):
        domain = [Encounter, Medication]
        range = [float]

    class payerId(DataProperty):
        domain = [Encounter, Medication, PayerTransition]
        range = [URN_UUID]

    class totalClaimCost(DataProperty):
        domain = [Encounter]
        range = [float]

    """
    ImagingStudy data properties:
    - bodySiteCode
    - bodySiteDescription
    - dateTime
    - encounterId: defined in Allergy
    - id: defined in Claim
    - instanceUid
    - modalityCode
    - modalityDescription
    - patientId: defined in Allergy
    - procedureCode
    - seriesUid
    - sopCode
    - sopDescription
    """

    class bodySiteCode(DataProperty):
        domain = [ImagingStudy]
        range = [SNOMED_CT]

    class bodySiteDescription(DataProperty):
        domain = [ImagingStudy]
        range = [str]

    class dateTime(DataProperty):
        domain = [ImagingStudy, Immunization, Observation]
        range = [datetime]

    class instanceUid(DataProperty):
        domain = [ImagingStudy]
        range = [DICOM_UID]

    class modalityCode(DataProperty):
        domain = [ImagingStudy]
        range = [DICOM_DCM]

    class modalityDescription(DataProperty):
        domain = [ImagingStudy]
        range = [str]

    class procedureCode(DataProperty):
        domain = [ImagingStudy]
        range = [SNOMED_CT]

    class seriesUid(DataProperty):
        domain = [ImagingStudy]
        range = [DICOM_UID]

    class sopCode(DataProperty):
        domain = [ImagingStudy]
        range = [DICOM_SOP]

    class sopDescription(DataProperty):
        domain = [ImagingStudy]
        range = [str]

    """
    Immunization data properties:
    - dateTime: defined in ImagingStudy
    - patientId: defined in Allergy
    - encounterId: defined in Allergy
    - code: defined in CarePlan
    - description: defined in Allergy
    - cost
    """

    class cost(DataProperty):
        domain = [Immunization]
        range = [float]

    """
    Medication data properties:
    - startDateTime: defined in Device
    - patientId: defined in Allergy
    - payerId: defined in Encounter
    - encounterId: defined in Allergy
    - code: defined in CarePlan
    - description: defined in Allergy
    - baseCost
    - payerCoverage: defined in Encounter
    - dispense
    - totalCost
    """

    class baseCost(DataProperty):
        domain = [Medication, Procedure]
        range = [float]

    class dispense(DataProperty):
        domain = [Medication]
        range = [float]

    class totalCost(DataProperty):
        domain = [Medication]
        range = [float]

    """
    Observation data properties:
    - code: defined in CarePlan
    - dateTime: defined in ImagingStudy
    - description: defined in Allergy
    - encounterId: defined in Allergy
    - patientId: defined in Allergy
    - type: defined in ClaimTransaction
    - value
    """

    class value(DataProperty):
        domain = [Observation]
        range = [float]

    """
    Organization data properties:
    - address
    - city
    - id: defined in Claim
    - name
    - revenue
    - utilization
    """

    class address(DataProperty):
        domain = [Organization, Patient, Provider]
        range = [str]

    class city(DataProperty):
        domain = [Organization, Patient, Provider]
        range = [str]

    class name(DataProperty):
        domain = [Organization, Payer, Provider]
        range = [str]

    class revenue(DataProperty):
        domain = [Organization, Payer]
        range = [float]

    class utilization(DataProperty):
        domain = [Organization, Provider]
        range = [int]

    """
    Patient data properties:
    - address: defined in Organization
    - birthDate
    - birthplace
    - city: defined in Organization
    - ethnicity
    - first
    - gender
    - healthcareCoverage
    - healthcareExpense
    - id: defined in Claim
    - income
    - last
    - race
    - ssn
    - state

    NOTE
    ----
    - [ ] Check data type of healthcareCoverage and healthcareExpense.
    """

    class birthDate(DataProperty):
        domain = [Patient]
        range = [datetime]

    class birthplace(DataProperty):
        domain = [Patient]
        range = [str]

    class ethnicity(DataProperty):
        domain = [Patient]
        range = [str]

    class first(DataProperty):
        domain = [Patient]
        range = [str]

    class gender(DataProperty):
        domain = [Patient, Provider]
        range = [str]

    class healthcareCoverage(DataProperty):
        domain = [Patient]
        range = [str]

    class healthcareExpense(DataProperty):
        domain = [Patient]
        range = [str]

    class income(DataProperty):
        domain = [Patient]
        range = [int]

    class last(DataProperty):
        domain = [Patient]
        range = [str]

    class race(DataProperty):
        domain = [Patient]
        range = [str]

    class ssn(DataProperty):
        domain = [Patient]
        range = [str]

    class state(DataProperty):
        domain = [Patient]
        range = [str]

    """
    Payer data properties:
    - amountCovered
    - amountUncovered
    - coveredEncounters
    - coveredImmunizations
    - coveredMedications
    - coveredProcedures
    - id: defined in Claim
    - memberMonths
    - name: defined in Organization
    - qolsAvg
    - revenue: defined in Organization
    - uncoveredEncounters
    - uncoveredImmunizations
    - uncoveredMedications
    - uncoveredProcedures
    - uniqueCustomers
    """

    class amountCovered(DataProperty):
        domain = [Payer]
        range = [float]

    class amountUncovered(DataProperty):
        domain = [Payer]
        range = [float]

    class coveredEncounters(DataProperty):
        domain = [Payer]
        range = [int]

    class coveredImmunizations(DataProperty):
        domain = [Payer]
        range = [int]

    class coveredMedications(DataProperty):
        domain = [Payer]
        range = [int]

    class coveredProcedures(DataProperty):
        domain = [Payer]
        range = [int]

    class memberMonths(DataProperty):
        domain = [Payer]
        range = [int]

    class qolsAvg(DataProperty):
        domain = [Payer]
        range = [float]

    class uncoveredEncounters(DataProperty):
        domain = [Payer]
        range = [int]

    class uncoveredImmunizations(DataProperty):
        domain = [Payer]
        range = [int]

    class uncoveredMedications(DataProperty):
        domain = [Payer]
        range = [int]

    class uncoveredProcedures(DataProperty):
        domain = [Payer]
        range = [int]

    class uniqueCustomers(DataProperty):
        domain = [Payer]
        range = [int]

    """
    PayerTransition data properties:
    - endYear
    - patientId: defined in Allergy
    - payerId: defined in Encounter
    - startYear

    NOTE
    ----
    - [ ] Check data type of endYear and startYear.
    """

    class endYear(DataProperty):
        domain = [PayerTransition]
        range = [datetime]

    class startYear(DataProperty):
        domain = [PayerTransition]
        range = [datetime]

    """
    Procedure data properties:
    - baseCost: defined in Medication
    - code: defined in CarePlan
    - description: defined in Allergy
    - encounterId: defined in Allergy
    - patientId: defined in Allergy
    - startDateTime: defined in Device
    """

    """
    Provider data properties:
    - address: defined in Organization
    - city: defined in Organization
    - gender: defined in Patient
    - id: defined in Claim
    - name: defined in Organization
    - organizationId: defined in Encounter
    - specialty
    - utilization: defined in Organization
    """

    class specialty(DataProperty):
        domain = [Provider]
        range = [str]

    """
    Supply data properties:
    - code: defined in CarePlan
    - date
    - description: defined in Allergy
    - encounterId: defined in Allergy
    - patientId: defined in Allergy
    - quantity
    """

    class date(DataProperty):
        domain = [Supply]
        range = [datetime]

    class quantity(DataProperty):
        domain = [Supply]
        range = [int]
