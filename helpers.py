# helper functions and variables
import streamlit as st
import pandas as pd

column_config_sample_table = {
        "Sample label": st.column_config.TextColumn(),
        "Titration row/column": st.column_config.TextColumn(),
        "Titration range": st.column_config.TextColumn(),
        "Starting concentration": st.column_config.NumberColumn(),
        "Dilution factor": st.column_config.NumberColumn(),
        "Ligand concentration": st.column_config.NumberColumn(),
        "Units": st.column_config.SelectboxColumn(options = ["nM", "uM", "mM"], 
                                                  default = 0),
        "Excluded wells": st.column_config.TextColumn()
    }

def generate_empty_plate() -> pd.DataFrame:
    # generates a table based on a 384-well plate
    # TODO: column typing

    ROW_IDX = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
    ]

    COLUMNS = range(1,25)

    plate_dict = dict([(column, [None] * 16) for column in COLUMNS])

    empty_plate = pd.DataFrame.from_dict(plate_dict)

    empty_plate.set_index(pd.Series(ROW_IDX), inplace=True)

    return empty_plate

def generate_sample_table(number_of_samples) -> pd.DataFrame:
    # Generates sample info table

    empty_column = [None] * number_of_samples

    table_dict = {
        "Sample label": empty_column,
        "Titration row/column": empty_column,
        "Titration range": empty_column,
        "Starting concentration": empty_column,
        "Dilution factor": empty_column,
        "Ligand concentration": empty_column,
        "Units": empty_column,
        "Excluded wells": empty_column
    }

    sample_table = pd.DataFrame.from_dict(table_dict)

    return sample_table