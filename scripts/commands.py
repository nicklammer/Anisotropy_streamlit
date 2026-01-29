# Functions that coordinate processing inputs, fitting, and plotting

import pandas as pd
import shutil
import os

from . import process_data, fit, plot


def process_anisotropy(data_dict, fit_dict, plot_dict, table_style, tmpdir):

    outdir_plots = f"{tmpdir}/plots"
    os.makedirs(outdir_plots, exist_ok = True)

    data_dict["parallel table"] = process_data.drop_empty_rows_columns(data_dict["parallel table"])
    data_dict["perpendicular table"] = process_data.drop_empty_rows_columns(data_dict["perpendicular table"])

    df_aniso = process_data.calculate_anisotropy(data_dict["parallel table"], data_dict["perpendicular table"])
    df_sample_data = process_data.convert_df_to_dict_anisotropy(
        df_aniso, data_dict["sample table"], data_dict["titration direction"])
    
    # Merge all dataframes
    df_all = pd.merge(data_dict["sample table"], table_style, on="unique name")
    df_all = pd.merge(df_all, df_sample_data, on="unique name")

    # Add units to data df
    df_all["units"] = data_dict["units"]

    # Add ligand concentration to fit_dict for ease of use
    # fit_dict["ligand concentration"] = dict(zip(
    #     data_dict["sample table"]["Sample label"],
    #     data_dict["sample table"]["Ligand concentration"]
    # ))

    fit_results_dict = fit_data(df_all, fit_dict, "anisotropy")

    df_all = df_all.merge(pd.DataFrame.from_dict(fit_results_dict), on="unique name")

    total_num_plots = max(df_all["Plot"])

    for i in range(1, total_num_plots + 1):
        # subset df_all using i and Plot column
        # make plot title using i
        # need to run plot function
        # save output to file in tmpdir

        df_subset = df_all[df_all["Plot"] == i]
        plot_title = f"{plot_dict['plot title']}_{str(i)}"
        filename = f"{plot_dict['filename']}_{str(i)}"

        plot.logplot(df_subset, "anisotropy", plot_title, filename, plot_dict, outdir_plots)

    zip_path = shutil.make_archive(outdir_plots, 'zip', outdir_plots)

    return zip_path



def fit_data(df_all, fit_dict, y_type):

    fit_functions = {
        "Simplified binding isotherm": fit.getkdfit,
        "Quadratic": fit.getquadfit,
        "Hill fit": fit.gethillfit,
        "Multi-step": fit.getmultifit
    }

    chosen_fit_function = fit_functions[fit_dict["fit type"]]

    # This should be made into a dataframe after the loop below
    fit_results_dict = {
        "unique name": [],
        "x fit": [],
        "y fit": [],
        "y norm": [],
        "parameters": [],
    }

    for i, row in df_all.iterrows():
        # Re-package needed info for fitting and plotting

        # For the fitting, I think we output a dataframe and merge again
        # for consistency 
        unique_name = row["unique name"]
        x = row["concentration"]
        y = row[y_type]

        x_fit, y_fit, y_norm, parameters_dict = chosen_fit_function(x, y, row["units"], fit_dict)

        fit_results_dict["unique name"].append(unique_name)
        fit_results_dict["x fit"].append(x_fit)
        fit_results_dict["y fit"].append(y_fit)
        fit_results_dict["y norm"].append(y_norm)
        fit_results_dict["parameters"].append(parameters_dict)

    return fit_results_dict