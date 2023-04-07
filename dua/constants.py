DUA_COLS = [
    "dataCustodian",
    "recipient",
    "requestedData",  # Basic Information
    "permittedUseOrDisclosure",
    "terms",
    "terminationCause",
    "terminationEffect",  # TermAndTermination
    "dataSecurityPlanAccess",
    "dataSecurityPlanProtection",
    "dataSecurityPlanStorage",
]  # Data_Security_Plan

PERMITTED_USE_OR_DISCLOSURE = [
    "treatment",
    "payment",
    "health_care_operations",
    "notification",
    "public_health",
    "limited_data_set",
]


DATA_CLASSES = [
    "Condition",
    "Encounter",
    "Immunization",
    "Medication",
    "Observation",
    "Organization",
    "Patient",
    "Payer",
    "Procedure",
    "Provider",
]
