from pathlib import Path
from synthea_rdf.graph import GraphBuilder

MODEL_PATH = "./synthea_ontology/synthea_ontology.ttl"
CSV_DIR = "./csv/Maryland_covid19_patient_10_bin_1"
DEST_PATH = "./test_result"


def test_convert_allergy():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertAllergy()
    assert builder.serialize(destination=Path(DEST_PATH) / "allergy.ttl") == builder.graph


def test_convert_careplan():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertCarePlan()
    assert builder.serialize(destination=Path(DEST_PATH) / "careplan.ttl") == builder.graph


def test_convert_claim():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertClaim()
    assert builder.serialize(destination=f"{DEST_PATH}/claim.ttl") == builder.graph


def test_convert_claimTransaction():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertClaimTransaction()
    assert builder.serialize(destination=f"{DEST_PATH}/claimTransaction.ttl") == builder.graph


def test_convert_condition():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertCondition()
    assert builder.serialize(destination=f"{DEST_PATH}/condition.ttl") == builder.graph


def test_convert_device():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertDevice()
    assert builder.serialize(destination=f"{DEST_PATH}/device.ttl") == builder.graph


def test_convert_encounter():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertEncounter()
    assert builder.serialize(destination=f"{DEST_PATH}/encounter.ttl") == builder.graph


def test_convert_imagingStudy():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertImagingStudy()
    assert builder.serialize(destination=f"{DEST_PATH}/imagingStudy.ttl") == builder.graph


def test_convert_immunization():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertImmunization()
    assert builder.serialize(destination=f"{DEST_PATH}/immunization.ttl") == builder.graph


def test_convert_medication():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertMedication()
    assert builder.serialize(destination=f"{DEST_PATH}/medication.ttl") == builder.graph


def test_convert_observation():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertObservation()
    assert builder.serialize(destination=f"{DEST_PATH}/observation.ttl") == builder.graph


def test_convert_organization():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertOrganization()
    assert builder.serialize(destination=f"{DEST_PATH}/organization.ttl") == builder.graph


def test_convert_patient():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertPatient()
    assert builder.serialize(destination=f"{DEST_PATH}/patient.ttl") == builder.graph


def test_convert_payer():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertPayer()
    assert builder.serialize(destination=f"{DEST_PATH}/payer.ttl") == builder.graph


def test_convert_payerTransition():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertPayerTransition()
    assert builder.serialize(destination=f"{DEST_PATH}/payerTransition.ttl") == builder.graph


def test_convert_procedure():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertProcedure()
    assert builder.serialize(destination=f"{DEST_PATH}/procedure.ttl") == builder.graph


def test_convert_provider():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertProvider()
    assert builder.serialize(destination=f"{DEST_PATH}/provider.ttl") == builder.graph


def test_convert_supply():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    builder.convertSupply()
    assert builder.serialize(destination=f"{DEST_PATH}/supply.ttl") == builder.graph


def test_convert_all():
    builder = GraphBuilder(CSV_DIR, MODEL_PATH)
    graph = builder.build()
    assert graph.serialize(destination=f"{DEST_PATH}/all.ttl") == graph
