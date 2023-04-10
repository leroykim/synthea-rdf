from alive_progress import alive_bar
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import XSD, RDF
from abstract import Resource
from abstract.namespace import TST
from abstract.uri import trustscoreUserUri, trustscoreOrganizationUri
from abstract.literal import floatLiteral


class TrustScore(Resource):
    def __init__(self, df):
        self.__resource_df = df

    @property
    def resource_df(self):
        return self.__resource_df

    @resource_df.setter
    def resource_df(self, value):
        self.__resource_df = value

    # def convert(self, trust_score_df: pd.DataFrame, file_name: str):
    #     graph = Graph()
    #     self.__set_model(graph, self.model_path)
    #     self.__build_user_trust_graph(graph, trust_score_df)
    #     graph.serialize(
    #         destination=f"{self.destination_dir}/{file_name}", format="turtle"
    #     )

    def convert(self, graph):
        rows = self.__resource_df.shape[0]
        with alive_bar(rows, force_tty=True, title="Trust score conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                user = trustscoreUserUri(index)
                graph.add((user, RDF.type, TST.User))
                graph.add(
                    (
                        user,
                        TST.identityTrust,
                        floatLiteral(row["identity_trust"]),
                    )
                )
                graph.add(
                    (
                        user,
                        TST.behaviorTrust,
                        floatLiteral(row["behavior_trust"]),
                    )
                )
                graph.add(
                    (
                        user,
                        TST.isAffiliatedWith,
                        trustscoreOrganizationUri(row["organization"]),
                    )
                )
                graph.add(
                    (
                        trustscoreOrganizationUri(row["organization"]),
                        TST.hasEmployed,
                        user,
                    )
                )
                bar()

        return graph