import random
from pathlib import Path
from pandas import DataFrame
from lorem_text import lorem
from .constants import DUA_COLS, PERMITTED_USE_OR_DISCLOSURE, DATA_CLASSES


class DUAGenerator:
    """
    In this class we use:
        - DUA_COUNT: Number of organizations who has DUA with the data custodian.
        - DUA_COLS: Name of the columns to generate DUA records.
        - PERMITTED_USE_OR_DISCLOSURE: Each DUA will have one permitted use or disclosure from this list.
        - RANDOM_SEED: Random seed for data generation consistency.

    Colums:
        - dataCustodian: data custodian id (not name)
        - recipient: data recipient id (not name)
        - requestdData: three categories from DATA_CLAASS in settings.py
        - permittedUseOrDisclosure: one categories from PERMITTED_USE_OR_DISCLOSURE in settings.py

        * Values of columns below are lorem ipsum for now *
        - terms
        - terminationCause
        - terminationEffect
        - dataSecurityPlanAccess
        - dataSecurityPlanProtection
        - dataSecurityPlanStorage

    TODO:
        - Refactor two methods
    """

    def __init__(self):
        self.organization_df = None  # not used in the current version of the code.
        self.rows = None  # not used in the current version of the code.

    def generate_dua(
        self,
        num_organization: int,
        save_path: str,
        num_requested_data: int = 3,
        seed: int = 7,
    ):
        """
        This method generates DUA records in the simplest way. Organizations generated by this
        methods does not match any organizations in the Synthea dataset.
        """

        print("Generating DUA...")
        print("Number of organizations: ", num_organization)
        print("Number of requested data: ", num_requested_data)
        print("Random seed: ", seed)

        data_custodian_id = "data_custodian"
        data_custodian_dummy = [data_custodian_id for i in range(num_organization)]
        data_recipients_id = list(range(num_organization))
        random.seed(seed)
        permittedUseOrDisclosure = [
            random.choice(PERMITTED_USE_OR_DISCLOSURE) for i in range(num_organization)
        ]
        requested_data = [
            self.__get_requested_data(num_requested_data)
            for i in range(num_organization)
        ]

        term = [lorem.sentence() for i in range(num_organization)]
        terminationEffect = [lorem.sentence() for i in range(num_organization)]
        terminationCause = [lorem.sentence() for i in range(num_organization)]
        storage = [lorem.sentence() for i in range(num_organization)]
        access = [lorem.sentence() for i in range(num_organization)]
        protection = [lorem.sentence() for i in range(num_organization)]

        dua_df = DataFrame(
            list(
                zip(
                    data_custodian_dummy,
                    data_recipients_id,
                    requested_data,
                    permittedUseOrDisclosure,
                    term,
                    terminationCause,
                    terminationEffect,
                    access,
                    protection,
                    storage,
                )
            ),
            columns=DUA_COLS,
        )
        save_path = Path(save_path).resolve()
        dua_df.to_csv(f"{save_path}/dua.csv")

        return dua_df

    def __get_recipients(self):
        # First organization (index 0) is the data custodian.
        # Refer to `get_data_custodian` method belwo.
        organizations = self.organization_df["Id"].tolist()
        return organizations[1:]

    def __get_data_custodian(self):
        return self.organization_df["Id"].tolist()[0]

    def __get_requested_data(self, num_requested_data: int = 3):
        requested_data = random.sample(DATA_CLASSES, num_requested_data)
        return ",".join(requested_data)

    def generate_dua_from_synthea(
        self, organization_df: DataFrame, save_path: str, num_requested_data: int = 3
    ):
        """
        WARNING: This method is not used in the current version of the code.

        This method generate DUA records from the Synthea dataset. It assumes that organizatoins
        in the Synthea dataset exchange data with each other. Therefore, every organization in the
        organizations csv will have DUA records.
        """
        self.organization_df = organization_df
        self.rows = organization_df.shape[0]

        data_custodian = self.__get_data_custodian()
        data_custodian_dummy = [data_custodian for i in range(self.rows)]
        random.seed(self.random_seed)
        permittedUseOrDisclosure = [
            random.choice(PERMITTED_USE_OR_DISCLOSURE) for i in range(self.rows)
        ]
        recipient = self.__get_recipients()

        requested_data = [
            self.__get_requested_data(num_requested_data) for i in range(self.rows)
        ]

        term = [lorem.sentence() for i in range(self.rows)]
        terminationEffect = [lorem.sentence() for i in range(self.rows)]
        terminationCause = [lorem.sentence() for i in range(self.rows)]
        storage = [lorem.sentence() for i in range(self.rows)]
        access = [lorem.sentence() for i in range(self.rows)]
        protection = [lorem.sentence() for i in range(self.rows)]

        dua_df = DataFrame(
            list(
                zip(
                    data_custodian_dummy,
                    recipient,
                    requested_data,
                    permittedUseOrDisclosure,
                    term,
                    terminationCause,
                    terminationEffect,
                    access,
                    protection,
                    storage,
                )
            ),
            columns=DUA_COLS,
        )

        dua_df.to_csv(save_path)

        return dua_df
