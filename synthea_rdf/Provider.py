from rdflib.namespace import RDF
from alive_progress import alive_bar

from .helper import organization_uri, string_literal, int_literal, organization_uri, provider_uri
from .setting import SYN

class Proider():
    def __init__(self, provider_df):
        self.provider_df = provider_df

    def convert(self, graph):
        with alive_bar(self.provider_df.shape[0], force_tty=True) as bar:
            for _, row in self.provider_df.iterrows():
                provider = provider_uri(row['Id'])
                graph.add((provider, RDF.type, SYN.Provider))
                graph.add((provider, SYN.belongsTo, organization_uri(row['ORGANIZATION'])))
                graph.add((provider, SYN.name, string_literal(row['NAME'])))
                graph.add((provider, SYN.gender, string_literal(row['GENDER'])))
                graph.add((provider, SYN.speciality, string_literal(row['SPECIALITY'])))
                graph.add((provider, SYN.name, string_literal(row['NAME'])))
                graph.add((provider, SYN.address, string_literal(row['ADDRESS'])))
                graph.add((provider, SYN.city, string_literal(row['CITY'])))
                graph.add((provider, SYN.state, string_literal(row['STATE'])))
                graph.add((provider, SYN.zip, string_literal(row['ZIP'])))
                graph.add((provider, SYN.utilization, int_literal(row['UTILIZATION'])))
                bar()
    