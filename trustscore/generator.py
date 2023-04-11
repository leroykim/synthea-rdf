import random
import time
import pandas as pd
from pathlib import Path


class TrustScoreGenerator:
    def __init__(self, num_org: int, user_per_org: int):
        """
        Parameters
        ----------
        num_org : int
            The number of organizations.
        user_per_org : int
            The number of users per organization.
        """
        self.num_org = num_org
        self.user_per_org = user_per_org
        self.user_count = num_org * user_per_org

    def generate_trustscore(self, save_path: str):
        """
        This method generates trust score for users and organizations in the simplest way.
        It gives highest trust score to all users and organizations, which is 1.
        """
        user_id = list(range(0, self.user_count))
        user_identity_trust = [1] * self.user_count
        user_behavior_trust = [1] * self.user_count
        affiliated_org = list(range(0, self.num_org)) * self.user_per_org
        org_identity_trust = [1] * self.user_count
        data = {
            "user": user_id,
            "identity_trust": user_identity_trust,
            "behavior_trust": user_behavior_trust,
            "organization": affiliated_org,
            "organization_trust": org_identity_trust,
        }

        print("Generating trust score...")
        print(f"Number of rows of user_id: {len(user_id)}")
        print(f"Number of rows of identity_trust: {len(user_identity_trust)}")
        print(f"Number of rows of behavior_trust: {len(user_behavior_trust)}")
        print(f"Number of rows of org_identity_trust: {len(org_identity_trust)}")

        save_path = Path(save_path).resolve()
        trustscore_df = pd.DataFrame.from_dict(data)
        trustscore_df.to_csv(f"{save_path}/trustscore.csv")
        return trustscore_df


class TrustScoreGeneratorAdvanced:
    def __init__(self, num_org: int, user_per_org: int):
        self.num_org = num_org
        self.user_per_org = user_per_org
        self.user_count = num_org * user_per_org
        self.__ranges = None
        self.__identity_dist = None
        self.__behavior_dist = None
        self.__org_identity_dist = None

    def set_distribution_and_trust(
        self,
        ranges: list[tuple[float, float]],
        identity_dist: list[float],
        behavior_dist: list[float],
        org_identity_dist: list[float],
    ):
        """
        Parameters
        ----------
        ranges : list[tuple[float, float]]
            A list of tuples that contains the minimum and maximum value of the trust score.
        identity_dist : list[float]
            A list of floats that contains the distribution of the identity trust score.
        behavior_dist : list[float]
            A list of floats that contains the distribution of the behavior trust score.
        org_identity_dist : list[float]
            A list of floats that contains the distribution of the organization's identity trust score.
        """
        print(
            f"Length of ranges: {len(ranges)} identity_dist: {len(identity_dist)} behavior_dist: {len(behavior_dist)}"
        )
        if len(identity_dist) != len(ranges):
            raise ValueError(
                "The length of identity_dist must be the same as the length of ranges."
            )
        elif len(behavior_dist) != len(ranges):
            raise ValueError(
                "The length of behavior_dist must be the same as the length of ranges."
            )
        elif len(identity_dist) != len(behavior_dist):
            raise ValueError(
                "The length of identity_dist must be the same as the length of behavior_dist."
            )

        self.__ranges = ranges
        self.__identity_dist = identity_dist
        self.__behavior_dist = behavior_dist
        self.__org_identity_dist = org_identity_dist

    def generate_user_trust(self):
        trust_score_df = self.__generate_user_trustscore()
        # trust_score_df["organization_trust"] = self.__org_identity_dist
        return trust_score_df

    def __generate_user_trustscore(self):
        user_id = range(0, self.user_count)
        identity_weights = [int(x * self.user_count) for x in self.__identity_dist]
        behavior_weights = [int(x * self.user_count) for x in self.__behavior_dist]
        org_identity_weights = [int(x * self.num_org) for x in self.__org_identity_dist]
        identity_trust = self.__generate_random_float(self.__ranges, identity_weights)
        behavior_trust = self.__generate_random_float(self.__ranges, behavior_weights)
        org_identity_trust = self.__generate_random_float(
            self.__ranges, org_identity_weights
        )
        affiliated_organization = [int(x // self.num_org) for x in user_id]
        data = {
            "user": user_id,
            "identity_trust": identity_trust,
            "behavior_trust": behavior_trust,
            "organization": affiliated_organization,
            "organization_trust": org_identity_trust,
        }
        print(
            f"Number of rows of user_id: {len(user_id)} identity_trust: {len(identity_trust)} behavior_trust: {len(behavior_trust)}"
        )
        return pd.DataFrame.from_dict(data)

    def __generate_random_float(self, ranges: list, weights: list):
        result = []
        i = 0
        while i < len(ranges):
            for n in range(weights[i]):
                random.seed(time.time())
                result.append(round(random.uniform(ranges[i][0], ranges[i][1]), 3))
            i += 1
        return result
