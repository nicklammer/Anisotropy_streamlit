# Functions that coordinate processing inputs, fitting, and plotting

import pandas as pd

from . import process_data, fit, plot


def process_anisotropy(data_dict, fit_dict, plot_dict, table_style, tmpdir):

    data_dict["parallel table"] = process_data.drop_empty_rows_columns(data_dict["parallel table"])
    data_dict["perpendicular table"] = process_data.drop_empty_rows_columns(data_dict["perpendicular table"])

    df_aniso = process_data.calculate_anisotropy(data_dict["parallel table"], data_dict["perpendicular table"])
    df_sample_data = process_data.convert_df_to_dict(
        df_aniso, data_dict["sample table"], data_dict["titration direction"])
    
    # Merge all dataframes
    df_all = pd.merge(data_dict["sample table"], table_style, on="unique name")
    df_all = pd.merge(df_all, df_sample_data, on="unique name")

    # Add ligand concentration to fit_dict for ease of use
    # fit_dict["ligand concentration"] = dict(zip(
    #     data_dict["sample table"]["Sample label"],
    #     data_dict["sample table"]["Ligand concentration"]
    # ))

    fit_functions = {
        "Simplified binding isotherm": fit.getkdfit,
        "Quadratic": fit.getquadfit,
        "Hill fit": fit.gethillfit,
        "Multi-step": fit.getmultifit
    }

    chosen_fit_function = fit_functions[fit_dict["fit type"]]

    fit_results_dict = {}

    for i, row in df_all.iterrows():
        # Re-package needed info for fitting and plotting
        # TODO: rewrite this 
        # sample_dict = {}
        # sample_dict["name"] = row["Sample label"]
        # sample_dict["ligand concentration"] = row["Ligand concentration"]
        # sample_dict["units"] = row["Units"]

        # sample_dict["concentration"] = row["concentration"]
        unique_name = row["unique name"]
        x = row["concentration"]
        y = row["anisotropy"]

        fit_results_dict[unique_name] = chosen_fit_function(x, y, fit_dict, row["units"])
