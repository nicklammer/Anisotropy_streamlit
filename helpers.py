# helper functions and variables
import streamlit as st
import pandas as pd
from string import ascii_uppercase

import plot_styles

column_config_data_plate = dict(
    [(str(column), st.column_config.NumberColumn()) for column in range(1, 25)]
)

column_config_sample_table = {
    "Sample label": st.column_config.TextColumn(),
    "Titration row/column": st.column_config.TextColumn(),
    "Titration range": st.column_config.TextColumn(),
    "Starting concentration": st.column_config.NumberColumn(),
    "Dilution factor": st.column_config.NumberColumn(),
    "Ligand concentration": st.column_config.NumberColumn(),
    "Units": st.column_config.SelectboxColumn(options=["nM", "uM", "mM"], default=0),
    "Excluded wells": st.column_config.TextColumn(),
}

column_config_style_table = {
    "Sample": st.column_config.TextColumn(),
    "Color": st.column_config.SelectboxColumn(
        options=list(plot_styles.color_dict.keys())
    ),
    "Marker style": st.column_config.SelectboxColumn(
        options=list(plot_styles.marker_dict.keys())
    ),
    "Line style": st.column_config.SelectboxColumn(
        options=list(plot_styles.line_dict.keys())
    ),
}


def generate_empty_plate() -> pd.DataFrame:
    # Generate a table based on a 384-well plate

    # Get A-P in a list
    ROW_IDX = [letter for letter in ascii_uppercase[0:16]]

    COLUMNS = range(1, 25)

    plate_dict = dict([(column, [None] * 16) for column in COLUMNS])

    empty_plate = pd.DataFrame.from_dict(plate_dict)

    empty_plate.set_index(pd.Series(ROW_IDX), inplace=True)

    return empty_plate


def generate_sample_table(number_of_samples) -> pd.DataFrame:
    # Generate sample info table

    empty_column = [None] * number_of_samples

    table_dict = {
        "Sample label": empty_column,
        "Titration row/column": empty_column,
        "Titration range": empty_column,
        "Starting concentration": empty_column,
        "Dilution factor": empty_column,
        "Ligand concentration": empty_column,
        "Units": empty_column,
        "Excluded wells": empty_column,
    }

    sample_table = pd.DataFrame.from_dict(table_dict)

    return sample_table


def generate_plot_style_table(sample_names) -> pd.DataFrame:
    # Generate table for choosing line and marker styles

    color_names = list(plot_styles.color_dict.keys())
    marker_names = list(plot_styles.marker_dict.keys())
    line_names = list(plot_styles.line_dict.keys())

    table_dict = {
        "Sample": sample_names,
        "Color": color_names[0 : len(sample_names)],
        "Marker style": [marker_names[0]] * len(sample_names),
        "Line style": [line_names[1]] * len(sample_names),
    }

    plot_style_table = pd.DataFrame.from_dict(table_dict)

    return plot_style_table
