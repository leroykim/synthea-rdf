from owlready2 import get_ontology, Thing
from synthea_rdf.util.configuration import Configuration

synthea_ontology = get_ontology(Configuration.synthea_namespace)

with synthea_ontology:

    class Allergy(Thing):
        pass

    class CarePlan(Thing):
        pass

    class Claim(Thing):
        pass

    class ClaimTransaction(Thing):
        pass

    class Condition(Thing):
        pass

    class Device(Thing):
        pass

    class Encounter(Thing):
        pass

    class ImagingStudy(Thing):
        pass

    class Immunization(Thing):
        pass

    class Medication(Thing):
        pass

    class Observation(Thing):
        pass

    class Organization(Thing):
        pass

    class Patient(Thing):
        pass

    class Payer(Thing):
        pass

    class PayerTransition(Thing):
        pass

    class Procedure(Thing):
        pass

    class Provider(Thing):
        pass

    class Supply(Thing):
        pass
