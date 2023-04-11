from alive_progress import alive_bar
from rdflib.namespace import RDF, RDFS
from abstract import Resource
from abstract.namespace import DUA, SYN
from abstract.literal import plainLiteral
from abstract.uri import (
    syntheaUri,
    duaUri,
    permittedUseOrDisclosureUri,
    dataSecurityPlanUri,
    termAndTerminationUri,
    organizationUri,
)


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
        """
        Should change dataCustodian and recipient values.
        It should be id instead of their names
        Synthea organization name format: SYN:organization_{organization_id}
        """
        # Data Custodian Organization
        data_custodian = organizationUri("dataCustodian")
        graph.add((data_custodian, RDF.type, SYN.Organization))
        graph.add((data_custodian, RDFS.label, plainLiteral("DataCustodian")))

        # Organizations
        rows = self.__resource_df.shape[0]
        for index, row in self.__resource_df.iterrows():
            organization = organizationUri(row["recipient"])
            graph.add((organization, RDF.type, SYN.Organization))
            graph.add((organization, RDFS.label, plainLiteral(f"Organization_{index}")))

        # Data Usage Agreement
        with alive_bar(
            rows, force_tty=True, title="Data Usage Agreement Conversion"
        ) as bar:
            for index, row in self.__resource_df.iterrows():
                dua = duaUri(index)
                data_security_plan = dataSecurityPlanUri(index)
                term_and_termination = termAndTerminationUri(index)

                graph.add((dua, RDF.type, DUA.DataUsageAgreement))
                graph.add((dua, RDFS.label, plainLiteral(f"DUA_{index}")))
                graph.add(
                    (
                        dua,
                        DUA.hasDataCustodian,
                        data_custodian,
                    )
                )
                graph.add((dua, DUA.hasRecipient, organizationUri(row["recipient"])))

                # Data Security Plan
                graph.add((data_security_plan, RDF.type, DUA.DataSecurityPlan))
                graph.add(
                    (
                        data_security_plan,
                        DUA.dataSecurityPlanAccess,
                        plainLiteral(row["dataSecurityPlanAccess"]),
                    )
                )
                graph.add(
                    (
                        data_security_plan,
                        DUA.dataSecurityPlanProtection,
                        plainLiteral(row["dataSecurityPlanProtection"]),
                    )
                )
                graph.add(
                    (
                        data_security_plan,
                        DUA.dataSecurityPlanStorage,
                        plainLiteral(row["dataSecurityPlanStorage"]),
                    )
                )
                graph.add((dua, DUA.hasDataSecurityPlan, data_security_plan))

                # Term and Termination
                graph.add((term_and_termination, RDF.type, DUA.TermAndTermination))
                graph.add((term_and_termination, DUA.terms, plainLiteral(row["terms"])))
                graph.add(
                    (
                        term_and_termination,
                        DUA.terminationCause,
                        plainLiteral(row["terminationCause"]),
                    )
                )
                graph.add(
                    (
                        term_and_termination,
                        DUA.terminationEffect,
                        plainLiteral(row["terminationEffect"]),
                    )
                )
                graph.add((dua, DUA.hasTermAndTermination, term_and_termination))

                # Permitted Use or Disclosure
                permitted_use_or_disclosure = permittedUseOrDisclosureUri(
                    row["permittedUseOrDisclosure"]
                )
                graph.add(
                    (
                        permitted_use_or_disclosure,
                        RDF.type,
                        DUA.PermittedUseOrDisclosure,
                    )
                )
                graph.add(
                    (
                        dua,
                        DUA.hasPermittedUseOrDisclosure,
                        permittedUseOrDisclosureUri(row["permittedUseOrDisclosure"]),
                    )
                )

                # Requested Data
                requested_data = row["requestedData"].split(",")
                for data in requested_data:
                    graph.add((dua, DUA.requestedData, plainLiteral(syntheaUri(data))))

                bar()
