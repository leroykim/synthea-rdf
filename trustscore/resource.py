from alive_progress import alive_bar
from rdflib.namespace import RDF, RDFS
from abstract import Resource
from abstract.namespace import TST, SYN
from abstract.uri import trustscoreUserUri, organizationUri
from abstract.literal import floatLiteral, plainLiteral


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
        # Data custodian
        data_custodian = trustscoreUserUri("data_custodian")
        graph.add((data_custodian, RDF.type, TST.User))
        graph.add((data_custodian, RDFS.label, plainLiteral("user_data_custodian")))
        graph.add((data_custodian, TST.credibility, floatLiteral(1.0)))
        graph.add((data_custodian, TST.objectivity, floatLiteral(1.0)))
        graph.add((data_custodian, TST.trustfulness, floatLiteral(1.0)))

        rows = self.__resource_df.shape[0]
        with alive_bar(rows, force_tty=True, title="Trust score conversion") as bar:
            for index, row in self.__resource_df.iterrows():
                user = trustscoreUserUri(index)
                graph.add((user, RDF.type, TST.User))
                graph.add((user, RDFS.label, plainLiteral(f"user_{index}")))
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
                        SYN.isAffiliatedWith,
                        organizationUri(row["organization"]),
                    )
                )
                graph.add(
                    (
                        organizationUri(row["organization"]),
                        SYN.hasEmployed,
                        user,
                    )
                )
                bar()

        return graph
