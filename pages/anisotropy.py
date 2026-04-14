"""
Analyze Fluorescence Anisotropy page.
"""
import streamlit as st
import pandas as pd

from ui import tabs
from pages.base_page import init_session_state, setup_temp_processing, setup_download_buttons, setup_page_header
from scripts.commands import process_fit_data


def fit_and_plot(tmpdir):
    """
    Process fit and plot data for anisotropy assay.
    
    This function is wrapped by setup_temp_processing which handles:
    - Creating temporary directory
    - Saving output zip to session_state
    - Updating download button state
    
    Args:
        tmpdir: Temporary directory path
    
    Returns:
        Tuple containing (outzip_path, plot_list)
    """
    # Call the shared processing function for anisotropy
    outzip_path, plot_list = process_fit_data(
        data_dict, fit_dict, plot_dict, table_style, tmpdir
    )
    return outzip_path, plot_list


st.set_page_config(layout="wide")

init_session_state()
data_dict = {}
fit_dict = {}
plot_dict = {}

setup_page_header("Analyze Fluorescence Anisotropy", "anisotropy.md")
setup_download_buttons(setup_temp_processing(fit_and_plot))

# Data tabs setup
data_tab, fit_tab, plot_tab, style_tab, view_tab = st.tabs([
    "Data", "Fit options", "Plot options", "Style options", "Plot view"
])

# Initialize data with page-specific configuration
data_dict = tabs.data_tab_table_anisotropy(data_tab, data_dict)
data_dict = tabs.data_tab_sample_info(data_tab, data_dict)

# Initialize fit options
fit_dict = tabs.fit_options_tab(fit_tab, fit_dict)

# Initialize plot options
plot_dict = tabs.plot_options_tab(plot_tab, plot_dict, len(data_dict["sample names"]))

# Initialize style options - this always runs to generate the style table
# The style table will have empty rows if no samples are loaded
table_style = tabs.style_options_tab(
    style_tab,
    data_dict["sample table"]["Sample label"],
    data_dict["sample table"]["unique name"],
    plot_dict["number of plots"],
)

# Display plots if available
tabs.plot_view_tab(view_tab, st.session_state.plot_list)