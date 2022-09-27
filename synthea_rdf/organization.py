from rdflib.namespace import RDF

from .helper import organization_uri, string_literal, int_literal, float_literal, organization_uri
from .setting import SYN

def convert(graph, organization_df):
    for _, row in organization_df.iterrows():
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