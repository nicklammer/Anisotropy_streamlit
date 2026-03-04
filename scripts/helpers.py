# Helper functions

import pandas as pd

def drop_empty_rows_columns(df_input):
    df_output = df_input.dropna(axis=1, how="all")
    df_output = df_output.dropna(axis=0, how="all")

    return df_output


def get_titration_indices_row(titration_range_split):

    return [
        str(t)
        for t in range(int(titration_range_split[0]), int(titration_range_split[1]) + 1)
    ]


def get_titration_indices_column(titration_range_split, column_labels):

    start_idx = 0
    end_idx = -1

    for i, label in enumerate(column_labels):
        # Get alphabet labels, record indices within array of labels
        if label == titration_range_split[0]:
            start_idx = i

        if label == titration_range_split[1]:
            end_idx = i

    # Get labels required for titration range
    return column_labels[start_idx:end_idx]