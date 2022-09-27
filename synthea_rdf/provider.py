from rdflib.namespace import RDF

from .helper import organization_uri, string_literal, int_literal, organization_uri, provider_uri
from .setting import SYN

def convert(graph, provider_df):
    for _, row in provider_df.iterrows():
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
    