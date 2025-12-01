# Functions that coordinate processing inputs, fitting, and plotting

from . import process_data, fit, plot


def process_inputs_anisotropy(parameters):
    # take parameter dictionary
    # convert data into useful forms
    # decide which functions (aniso vs polar)



def fit_plot_anisotropy(parameters):
    # should this process 1 sample or have a loop integrated?

    # drop columns and rows that only contain NA/None value in input tables
    parameters["parallel table"] = parameters["parallel table"].dropna(axis=1, how="all")
    parameters["parallel table"] = parameters["parallel table"].dropna(axis=0, how="all")

    parameters["perpendicular table"] = parameters["perpendicular table"].dropna(axis=1, how="all")
    parameters["perpendicular table"] = parameters["perpendicular table"].dropna(axis=0, how="all")

    df_aniso = process_data.calculate_anisotropy(parameters["parallel table"], parameters["perpendicular table"])
    aniso_dict, conc_dict = process_data.convert_df_to_dict(df_aniso, parameters["sample table"], parameters["titration direction"])
