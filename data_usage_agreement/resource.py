from abc import ABC, abstractmethod
from alive_progress import alive_bar
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from .settings import DUA


class Resource(ABC):
    @abstractmethod
    def __init__(self, df):
        self.__resource_df = df

    @property
    @abstractmethod
    def resource_df(self):
        pass

    @resource_df.setter
    @abstractmethod
    def resource_df(self, value):
        pass

    @abstractmethod
    def convert(self, graph):
        pass

class DataUsageAgreement(Resource):
    def __init__(self, resource_df):
        self.__resource_df = resource_df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    def convert(self, graph):
        rows = self.__resource_df.shape[0]
        with alive_bar(rows, force_tty=True, title='Data Usage Agreement Conversion') as bar:
            for index, row in self.__resource_df.iterrows():
                dua = dua_uri(index)
                data_security_plan = data_security_plan_uri(index)
                term_and_termination = term_and_termination_uri(index)
                
                graph.add((dua, RDF.type, DUA.DataUsageAgreement))
                graph.add((data_security_plan, RDF.type, DUA.DataSecurityPlan))
                graph.add((term_and_termination, RDF.type, DUA.TermAndTermination))

                # Data Properties
                graph.add((data_security_plan, DUA.dataSecurityPlanAccess, plain_literal(row['dataSecurityPlanAccess'])))
                graph.add((data_security_plan, DUA.dataSecurityPlanProtection, plain_literal(row['dataSecurityPlanProtection'])))
                graph.add((data_security_plan, DUA.dataSecurityPlanStorage, plain_literal(row['dataSecurityPlanStorage'])))
                graph.add((term_and_termination, DUA.term, plain_literal(row['term'])))
                graph.add((term_and_termination, DUA.terminationCase, plain_literal(row['terminationCase'])))
                graph.add((term_and_termination, DUA.terminationEffect, plain_literal(row['terminationEffect'])))

                # Object Properties
                graph.add((dua, DUA.hasDataCustodian, get_uri(row['dataCustodian'])))
                graph.add((dua, DUA.hasDataDataSecurityPlan, data_security_plan))
                graph.add((dua, DUA.hasTermAndTermination, term_and_termination))
                graph.add((dua, DUA.hasPermittedUseOrDisclosure, get_uri(row['permittedUseOrDisclosure'])))
                graph.add((dua, DUA.hasRecipient, get_uri(row['recipient'])))

                # Requested Data
                requested_data = row['requestedData'].split(',')
                for data in requested_data:
                    graph.add((dua, DUA.hasRequestedData, get_uri(data)))
                

# Literal help methods

def plain_literal(string):
    return Literal(str(string), datatype=RDF.PlainLiteral)

# Uri help methods

def get_uri(name):
    return URIRef(f'{DUA}{name}')

def dua_uri(dua_id):
    return URIRef(f'{DUA}dua_{dua_id}')

def permitted_use_or_disclosure_uri(dua_id):
    return URIRef(f'{DUA}permitted_use_or_disclosure_{dua_id}')

def data_security_plan_uri(dua_id):
    # Permitted Usage or Disclosure
    return URIRef(f'{DUA}data_security_plan_{dua_id}')

def term_and_termination_uri(dua_id):
    # Permitted Usage or Disclosure
    return URIRef(f'{DUA}term_and_termination_{dua_id}')
