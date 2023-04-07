from alive_progress import alive_bar
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import XSD, RDF
from abstract import Resource

TRUST_IRI = "https://knacc.umbc.edu/dae-young/kim/ontologies/trust#"
TRUST = Namespace(TRUST_IRI)


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
                user = self.__userUri(index)
                graph.add((user, RDF.type, TRUST.User))
                graph.add(
                    (
                        user,
                        TRUST.identityTrust,
                        self.__floatLiteral(row["identity_trust"]),
                    )
                )
                graph.add(
                    (
                        user,
                        TRUST.behaviorTrust,
                        self.__floatLiteral(row["behavior_trust"]),
                    )
                )
                graph.add((user, TRUST.isAffiliatedWith, self.__organizationUri("x")))
                graph.add((self.__organizationUri("x"), TRUST.hasEmployed, user))
                bar()

    def __userUri(self, id):
        return URIRef(f"{TRUST}user_{id}")

    def __organizationUri(self, id):
        return URIRef(f"{TRUST}org_{id}")

    def __floatLiteral(self, value):
        return Literal(value, datatype=XSD.float)
