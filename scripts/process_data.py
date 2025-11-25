# Process plate data

import pandas as pd
import numpy as np

def calculate_anisotropy(df_parallel, df_perpendicular):
    # Check if both dataframes have the same shape
    if df_parallel.shape != df_perpendicular.shape:
        raise ValueError("DataFrames must have the same shape.")

    # Define the anisotropy calculation function
    def _anisotropy_equation(parallel_value, perpendicular_value):
        return ((parallel_value-perpendicular_value)/(parallel_value + 2 * perpendicular_value))

    # Calculate anisotropy for each element where both values are not NaN
    none_mask = df_parallel.notna() & df_perpendicular.notna()
    df_anisotropy = pd.DataFrame(
        np.where(none_mask, 
                 _anisotropy_equation(df_parallel, df_perpendicular), 
                 None),
        index=df_parallel.index,
        columns=df_parallel.columns
    )

    return df_anisotropy