from owlready2 import get_ontology, ObjectProperty
from synthea_rdf.util.configuration import Configuration
from synthea_rdf.definitions.classes import *

synthea_ontology = get_ontology(Configuration.synthea_namespace)

with synthea_ontology:
    """
    Allergy object properties
    - isAbout
    - isDiagnosedDuring
    """

    class isAbout(ObjectProperty):
        domain = [Allergy, CarePlan, Condition, ImagingStudy]
        range = [Patient]

    class isDiagnosedDuring(ObjectProperty):
        domain = [Allergy, Condition]
        range = [Encounter]

    """
    CarePlan object properties

    NOTE
    ----
    isAbout is defined in Allergy object properties.
    """

    class isOrderedDuring(ObjectProperty):
        domain = [CarePlan, Device, ImagingStudy, Procedure, Observation]
        range = [Encounter]

    """
    Claim object properties
    """

    class isAssociatedWith(ObjectProperty):
        domain = [Claim, ClaimTransaction]
        range = [Patient, Provider]

    class isFiledBy(ObjectProperty):
        domain = [Claim]
        range = [Provider]

    class hasTransaction(ObjectProperty):
        domain = [Claim]
        range = [ClaimTransaction]

    """
    ClaimTransaction object properties
    
    NOTE
    ----
    isAssociatedWith Patient and Provider is defined in Claim object properties.
    """

    class isTransactionFor(ObjectProperty):
        domain = [ClaimTransaction]
        range = [Claim]

    class hasPlaceOfService(ObjectProperty):
        domain = [ClaimTransaction]
        range = [Organization]

    """
    Condition object properties
    
    NOTE
    ----
    - isAbout is defined in Allergy object properties.
    - isDiagnosedDuring is defined in Allergy object properties.
    """

    """
    Device object properties
    
    NOTE
    ----
    - isOrderedDuring is defined in CarePlan object properties.
    """

    class hasMeasured(ObjectProperty):
        domain = [Device]
        range = [Patient]

    """
    Encounter object properties
    """

    class hasDiagnosed(ObjectProperty):
        domain = [Encounter]
        range = [Allergy, Condition]

    class hasOrdered(ObjectProperty):
        domain = [Encounter]
        range = [CarePlan, Device, ImagingStudy, Procedure]

    class hasPatient(ObjectProperty):
        domain = [Encounter]
        range = [Patient]

    class isPerformedAt(ObjectProperty):
        domain = [Encounter]
        range = [Organization]

    class isPerformedBy(ObjectProperty):
        domain = [Encounter]
        range = [Provider]

    class isCoveredBy(ObjectProperty):
        domain = [Encounter]
        range = [Payer]

    class hasPrescribed(ObjectProperty):
        domain = [Encounter]
        range = [Immunization, Medication]

    """
    ImagingStudy object properties
    
    NOTE
    ----
    - isAbout is defined in Allergy object properties.
    - isOrderedDuring is defined in CarePlan object properties.
    """

    """Immunization object properties"""

    class isPrescribedFor(ObjectProperty):
        domain = [Immunization]
        range = [Patient]

    class isPrescribedDuring(ObjectProperty):
        domain = [Immunization]
        range = [Encounter]

    """
    Medication object properties
    """

    class isPrescribedFor(ObjectProperty):
        domain = [Medication]
        range = [Patient]

    class isPrescribedDuring(ObjectProperty):
        domain = [Medication]
        range = [Encounter]

    class isCoveredBy(ObjectProperty):
        domain = [Medication]
        range = [Payer]

    """
    Observation object properties

    NOTE
    ----
    isOrderedDuring is defined in CarePlan object properties.
    """

    class isAbout(ObjectProperty):
        domain = [Observation]
        range = [Patient]

    """
    Organization object properties
    
    NOTE
    ----
    - hasClaimTransaction is defined in Patient object properties.
    """

    """
    Patient object properties
    """

    class hasAllergy(ObjectProperty):
        domain = [Patient]
        range = [Allergy]

    class hasCarePlan(ObjectProperty):
        domain = [Patient]
        range = [CarePlan]

    class hasClaim(ObjectProperty):
        domain = [Patient]
        range = [Claim]

    class hasClaimTransaction(ObjectProperty):
        domain = [Organization, Patient, Provider]
        range = [ClaimTransaction]

    class hasEmployed(ObjectProperty):
        domain = [Organization]
        range = [Provider]

    class hasHistoryOf(ObjectProperty):
        domain = [Patient]
        range = [Condition, ImagingStudy, Immunization, Medication, Procedure]

    class isMeasuredBut(ObjectProperty):
        domain = [Patient]
        range = [Device]

    class hasPayerTransitionHistory(ObjectProperty):
        domain = [Patient, Payer]
        range = [PayerTransition]

    """
    Payer object properties

    NOTE
    ----
    hasPayerTransitionHistory is defined in Patient object properties.
    """

    class hasCovered(ObjectProperty):
        domain = [Payer]
        range = [Medication]

    """
    PayerTransition object properties
    """

    class hasPatientRecord(ObjectProperty):
        domain = [PayerTransition]
        range = [Patient]

    class hasPayerRecord(ObjectProperty):
        domain = [PayerTransition]
        range = [Payer]

    """
    Procedure object properties

    NOTE
    ----
    isOrderedDuring is defined in CarePlan object properties.
    """

    class isOrderedFor(ObjectProperty):
        domain = [Procedure]
        range = [Patient]

    """
    Provider object properties

    NOTE
    ----
    hasClaimTransaction is defined in Patient object properties.
    """

    class isAffiliatedWith(ObjectProperty):
        domain = [Provider]
        range = [Organization]

    class hasFiled(ObjectProperty):
        domain = [Provider]
        range = [Claim]

    class hasPerformed(ObjectProperty):
        domain = [Provider]
        range = [Encounter]
