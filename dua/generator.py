import random
import pandas as pd
from lorem_text import lorem
from .settings import (
    DUA_COLS,
    DATA_CLASSES,
    DATA_CLASS_SAMPLE_SIZE,
    PERMITTED_USE_OR_DISCLOSURE,
    RANDOM_SEED,
)


class DUAGenerator:
    def __init__(self, organization_df: pd.DataFrame):
        self.organization_df = organization_df
        self.rows = organization_df.shape[0]

    def generate(self, save_path: str):
        """
        Every parameters are defined in settings.py
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
        """

        data_custodian = self.get_data_custodian()
        data_custodian_dummy = [data_custodian for i in range(self.rows)]
        random.seed(RANDOM_SEED)
        permittedUseOrDisclosure = [
            random.choice(PERMITTED_USE_OR_DISCLOSURE) for i in range(self.rows)
        ]
        recipient = self.get_recipients()

        requested_data = [self.get_requested_data() for i in range(self.rows)]

        term = [lorem.sentence() for i in range(self.rows)]
        terminationEffect = [lorem.sentence() for i in range(self.rows)]
        terminationCause = [lorem.sentence() for i in range(self.rows)]
        storage = [lorem.sentence() for i in range(self.rows)]
        access = [lorem.sentence() for i in range(self.rows)]
        protection = [lorem.sentence() for i in range(self.rows)]

        dua_df = pd.DataFrame(
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

    def get_recipients(self):
        # First organization (index 0) is the data custodian.
        # Refer to `get_data_custodian` method belwo.
        organizations = self.organization_df["Id"].tolist()
        return organizations[1:]

    def get_data_custodian(self):
        return self.organization_df["Id"].tolist()[0]

    def get_requested_data(self):
        requested_data = random.sample(DATA_CLASSES, DATA_CLASS_SAMPLE_SIZE)
        return ",".join(requested_data)
