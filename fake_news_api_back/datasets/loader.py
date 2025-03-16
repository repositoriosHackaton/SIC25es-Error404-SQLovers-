import pandas as pd
import os
from django.conf import settings

DATASET_PATH = os.path.join(settings.BASE_DIR, "datasets/raw/")

def load_dataset():
    true_df = pd.read_csv(os.path.join(DATASET_PATH, "onlytrue1000.csv"))
    fake_df = pd.read_csv(os.path.join(DATASET_PATH, "onlyfakes1000.csv"))

    true_df["label"] = 0
    fake_df["label"] = 1

    df = pd.concat([true_df, fake_df]).reset_index(drop=True)
    return df
