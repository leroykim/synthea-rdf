import pandas as pd
import numpy as np
from .settings import USER_TRUST_COLS, ORG_TRUST_COLS, VERACITY_COLS


def generate_user_trust(rows):
    size = (rows, 2)
    return generate_trust_data(size, USER_TRUST_COLS)


def generate_org_trust(rows):
    size = (rows, 1)
    return generate_trust_data(size, ORG_TRUST_COLS)


def generate_veracity(rows):
    size = (rows, 3)
    return generate_trust_data(size, VERACITY_COLS)


def generate_trust_data(size, columns):
    data = pd.DataFrame(
        np.random.uniform(
            low=0.0,
            high=1.0,
            size=size
        ),
        columns=columns
    )
    return data
