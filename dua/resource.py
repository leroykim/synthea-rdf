from abc import ABC, abstractmethod
from alive_progress import alive_bar
from rdflib import Literal, URIRef
from rdflib.namespace import RDF
from .settings import DUA, SYN


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
        '''
        Should change dataCustodian and recipient values.
        It should be id instead of their names
        Synthea organization name format: SYN:organization_{organization_id}
        '''
        rows = self.__resource_df.shape[0]
        with alive_bar(rows, force_tty=True, title='Data Usage Agreement Conversion') as bar:
            for index, row in self.__resource_df.iterrows():
                dua = dua_uri(index)
                data_security_plan = data_security_plan_uri(index)
                term_and_termination = term_and_termination_uri(index)
                
                graph.add((dua, RDF.type, DUA.DataUsageAgreement))
                graph.add((dua, DUA.hasDataCustodian, organization_uri(row['dataCustodian'])))
                graph.add((dua, DUA.hasRecipient, organization_uri(row['recipient'])))
            

                # Data Security Plan
                graph.add((data_security_plan, RDF.type, DUA.DataSecurityPlan))
                graph.add((data_security_plan, DUA.dataSecurityPlanAccess, plain_literal(row['dataSecurityPlanAccess'])))
                graph.add((data_security_plan, DUA.dataSecurityPlanProtection, plain_literal(row['dataSecurityPlanProtection'])))
                graph.add((data_security_plan, DUA.dataSecurityPlanStorage, plain_literal(row['dataSecurityPlanStorage'])))
                graph.add((dua, DUA.hasDataSecurityPlan, data_security_plan))

                # Term and Termination
                graph.add((term_and_termination, RDF.type, DUA.TermAndTermination))
                graph.add((term_and_termination, DUA.terms, plain_literal(row['terms'])))
                graph.add((term_and_termination, DUA.terminationCause, plain_literal(row['terminationCause'])))
                graph.add((term_and_termination, DUA.terminationEffect, plain_literal(row['terminationEffect'])))
                graph.add((dua, DUA.hasTermAndTermination, term_and_termination))

                # Permitted Use or Disclosure
                permitted_use_or_disclosure = permitted_use_or_disclosure_uri(row['permittedUseOrDisclosure'])
                graph.add((permitted_use_or_disclosure, RDF.type, DUA.PermittedUseOrDisclosure))
                graph.add((dua, DUA.hasPermittedUseOrDisclosure, permitted_use_or_disclosure_uri(row['permittedUseOrDisclosure'])))
                
                # Requested Data
                requested_data = row['requestedData'].split(",")
                for data in requested_data:
                    graph.add((dua, DUA.requestedData, plain_literal(synthea_uri(data))))

                bar()
                

# Literal help methods

def plain_literal(string):
    return Literal(str(string), datatype=RDF.PlainLiteral)

# Uri help methods

def synthea_uri(name):
    return URIRef(f'{SYN}{name}')

def dua_uri(dua_id):
    return URIRef(f'{DUA}dua_{dua_id}')

def permitted_use_or_disclosure_uri(dua_id):
    return URIRef(f'{DUA}{dua_id}')

def data_security_plan_uri(dua_id):
    # Permitted Usage or Disclosure
    return URIRef(f'{DUA}data_security_plan_{dua_id}')

def term_and_termination_uri(dua_id):
    # Permitted Usage or Disclosure
    return URIRef(f'{DUA}term_and_termination_{dua_id}')

def organization_uri(organization_id):
    return URIRef(f'{SYN}organization_{organization_id}')
