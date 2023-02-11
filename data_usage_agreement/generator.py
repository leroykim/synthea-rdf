import random
import pandas as pd
from lorem_text import lorem
from .settings import DUA_COUNT, DUA_COLS, DATA_CLASSES, DATA_CLASS_SAMPLE_SIZE, PERMITTED_USE_OR_DISCLOSURE, RANDOM_SEED, SAVE_PATH


class DUAGenerator():
    def __init__(self, organization_df: pd.DataFrame):
        '''
        Every parameters are defined in settings.py
        In this class we use:
        - DUA_COUNT: Number of organizations who has DUA with the data custodian.
        - DUA_COLS: Name of the columns to generate DUA records.
        - PERMITTED_USE_OR_DISCLOSURE: Each DUA will have one permitted use or disclosure from this list.
        - RANDOM_SEED: Random seed for data generation consistency.
        '''
        self.organization_df = organization_df

    def generate(self, rows=DUA_COUNT):

        data_custodian = self.get_data_custodian()
        data_custodian_dummy = [data_custodian for i in range(rows)]
        random.seed(RANDOM_SEED)
        permittedUseOrDisclosure = [random.choice(
            PERMITTED_USE_OR_DISCLOSURE) for i in range(rows)]
        recipient = self.get_recipients()

        requested_data = [self.get_requested_data() for i in range(rows)]

        term = [lorem.sentence() for i in range(rows)]
        terminationEffect = [lorem.sentence() for i in range(rows)]
        terminationCause = [lorem.sentence() for i in range(rows)]
        storage = [lorem.sentence() for i in range(rows)]
        access = [lorem.sentence() for i in range(rows)]
        protection = [lorem.sentence() for i in range(rows)]

        dua_df = pd.DataFrame(
            list(zip(
                data_custodian_dummy, recipient, requested_data,
                permittedUseOrDisclosure, term, terminationCause, terminationEffect,
                access, protection, storage)),
            columns=DUA_COLS
        )

        dua_df.to_csv(SAVE_PATH)

        return dua_df

    def get_recipients(self, rows=DUA_COUNT):
        organization_names = self.organization_df['NAME'].tolist()
        return random.sample(organization_names[1:], rows)

    def get_data_custodian(self):
        return self.organization_df['NAME'].tolist()[0]

    def get_requested_data(self):
        requested_data = random.sample(DATA_CLASSES, DATA_CLASS_SAMPLE_SIZE)
        return ",".join(requested_data)