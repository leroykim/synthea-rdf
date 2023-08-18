import yaml
from dataclasses import dataclass

with open("configuration.yaml", "r") as configuration_file:
    configuration = yaml.safe_load(configuration_file)


@dataclass
class Configration:
    with open("configuration.yaml", "r") as configuration_file:
        __configuration = yaml.safe_load(configuration_file)

    synthea_namespace: str = __configuration["synthea_namespace"]
