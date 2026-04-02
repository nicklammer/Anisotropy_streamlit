# Process plate data

import pandas as pd
import numpy as np

from . import helpers


def calculate_anisotropy(df_parallel, df_perpendicular):

    # Define the anisotropy calculation function
    def _anisotropy_equation(parallel_value, perpendicular_value):
        return (parallel_value - perpendicular_value) / (
            parallel_value + 2 * perpendicular_value
        )

    # Calculate anisotropy for each element where both values are not NaN
    none_mask = df_parallel.notna() & df_perpendicular.notna()
    df_anisotropy = pd.DataFrame(
        np.where(
            none_mask, _anisotropy_equation(df_parallel, df_perpendicular), np.nan
        ),
        index=df_parallel.index,
        columns=df_parallel.columns,
    )

    return df_anisotropy


# def compile_anisotropy(
#     df_anisotropy, table_samples, titration_direction
# ) -> pd.DataFrame:
#     # Compiles anisotropy and concentration data for each sample

#     # Transpose input data if titrations were performed column-wise
#     if titration_direction == "Columns":
#         df_anisotropy = df_anisotropy.T

#     df_sample_data = table_samples.apply(
#         get_data_over_titration, axis=1, args=(df_anisotropy, titration_direction, "anisotropy")
#     )

#     return df_sample_data

def compile_data_assay_concentration(
    df_data, table_samples, titration_direction, assay
) -> pd.DataFrame:
    # Compiles assay data and concentration data for each sample

    # Transpose input data if titrations were performed column-wise
    if titration_direction == "Columns":
        df_data = df_data.T

    df_sample_data = table_samples.apply(
        get_data_over_titration, axis=1, args=(df_data, titration_direction, assay)
    )

    return df_sample_data

def compile_data_assay_concentration_from_csv(
    df_data, assay
) -> pd.DataFrame:
    # Compiles assay data and concentration data for each sample

    data_dict = {
        "unique name": [],
        "concentration": [],
        assay: []
    }

    sample_idx = 0
    for column in df_data.columns:

        if "concentration" in str(column).lower():
            data_dict["concentration"].append(df_data[column].dropna().to_list())

        elif assay in str(column).lower():
            data_dict[assay].append(df_data[column].dropna().to_list())

            sample_name = column.lower().split(f"{assay} ")[1]
            data_dict["unique name"].append(f"{str(sample_idx)}_{sample_name}")

            sample_idx += 1

    df_sample_data = pd.DataFrame.from_dict(data_dict)

    return df_sample_data

def get_data_over_titration(row, df_input, titration_direction, assay):

    # unpack row
    titration_idx = row["Titration row/column"]
    titration_range = row["Titration range"]
    excluded_wells = row["Excluded wells"]
    starting_conc = row["Starting concentration"]
    dilution_factor = row["Dilution factor"]

    # get row from input dataframe
    input_row = df_input.loc[titration_idx]

    # parse titration range
    titration_range_split = titration_range.split("-")

    if titration_direction == "Rows":
        # Row-wise is default and range works for column names
        titration_indices = helpers.get_titration_indices_row(titration_range_split)

    else:
        # Column-wise is alt method and requires more work to get a range (because of alphabetical indices)
        column_labels = df_input.columns.values
        titration_indices = helpers.get_titration_indices_column(
            titration_range_split, column_labels
        )

    # subset row of data using list of column names/indices
    input_row = input_row.loc[titration_indices]

    # calculate serial dilution over titration range
    concentration_list = [
        starting_conc / (dilution_factor**i) for i in range(len(input_row))
    ]
    # create pd.Series to mirror the data row above
    concentration_row = pd.Series(concentration_list, index=input_row.index)

    # drop excluded wells
    if excluded_wells:
        excluded_wells_list = [well.strip() for well in excluded_wells.split(",")]
        input_row = input_row.drop(
            labels=excluded_wells_list, errors="ignore"
        )
        concentration_row = concentration_row.drop(
            labels=excluded_wells_list, errors="ignore"
        )

    return pd.Series(
        {
            "unique name": row["unique name"],
            "concentration": concentration_row.to_list(),
            assay: input_row.to_list(),
        }
    )