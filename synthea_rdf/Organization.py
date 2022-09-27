from rdflib.namespace import RDF
from alive_progress import alive_bar

from .helper import organization_uri, string_literal, int_literal, float_literal, organization_uri
from .setting import SYN

class Organization():
    def __init__(self, organization_df):
        self.organization_df = organization_df

    def convert(self, graph):
        with alive_bar(self.organization_df.shape[0], force_tty=True) as bar:
            for _, row in self.organization_df.iterrows():
                organization = organization_uri(row['Id'])
                graph.add((organization, RDF.type, SYN.Organization))
                graph.add((organization, SYN.name, string_literal(row['NAME'])))
                graph.add((organization, SYN.address, string_literal(row['ADDRESS'])))
                graph.add((organization, SYN.city, string_literal(row['CITY'])))
                graph.add((organization, SYN.state, string_literal(row['STATE'])))
                graph.add((organization, SYN.zip, string_literal(row['ZIP'])))
                graph.add((organization, SYN.phone, string_literal(row['PHONE'])))
                graph.add((organization, SYN.revenue, float_literal(row['REVENUE'])))
                graph.add((organization, SYN.utilization, int_literal(row['UTILIZATION'])))
                bar()