# Functions for creating tabs. Hopefully keeps page files clean.
import streamlit as st
import helpers


def data_tab_selffill(tab, parameters):
    tab.write("Parallel fluorescence")
    table_parallel = tab.data_editor(
        helpers.generate_empty_plate(), key="parallel", disabled=["_index"]
    )

    tab.write("Perpendicular fluorescence")
    table_perpendicular = tab.data_editor(
        helpers.generate_empty_plate(), key="perpendicular", disabled=["_index"]
    )

    number_of_samples = tab.number_input("How many samples do you have?", min_value = 1, 
                     value = 1)

    parameters["titration direction"] = tab.selectbox(
        "Titrated in rows or columns?", options=["Rows", "Columns"]
    )

    table_samples = tab.data_editor(
        helpers.generate_sample_table(number_of_samples), key="samples", hide_index = True, num_rows = "dynamic",
        column_config = helpers.column_config_sample_table
    )

    parameters["assay type"] = tab.selectbox(
        "Anisotropy or polarization?", options=["Anisotropy", "Polarization"]
    )

    # TODO: probably a better way to package up the tables
    return parameters, table_samples, table_parallel, table_perpendicular

def fit_options_tab(tab, parameters):
    tab.write("Select type of fit:")
    parameters["fit type"] = tab.selectbox(
        "Select type of fit", options=["Simplified binding isotherm", "Hill fit", "Multi-step"]
    )

    if parameters["fit type"] == "Simplified binding isotherm":
        simplified_fit_options()
    
    elif parameters["fit type"] == "Hill fit":



def simplified_fit_options():