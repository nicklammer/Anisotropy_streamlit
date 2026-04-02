import streamlit as st
import pandas as pd
import tempfile
import time

import tabs
from scripts.commands import process_fit_data_from_csv

st.set_page_config(layout="wide")

if "file_bytes" not in st.session_state:
    st.session_state.file_bytes = None
if "file_timestamp" not in st.session_state:
    st.session_state.file_timestamp = ""
if "dl_button_disabled" not in st.session_state:
    st.session_state.dl_button_disabled = True
if "plot_list" not in st.session_state:
    st.session_state.plot_list = []


def fit_and_plot():
    with tempfile.TemporaryDirectory() as tmpdir:
        outzip_path, plot_list = process_fit_data_from_csv(
            data_dict, fit_dict, plot_dict, table_style, tmpdir
        )

        st.session_state.plot_list = plot_list

        with open(outzip_path, "rb") as f:
            st.session_state.file_bytes = f.read()

    st.session_state.dl_button_disabled = False
    st.session_state.file_timestamp = time.strftime("%Y%m%d_%H%M%S")
    st.toast("Plots complete! Ready for download.")


data_dict = {}
fit_dict = {}
plot_dict = {}

st.title("Analyze from csv file")

buttons_left, buttons_right = st.columns([0.15, 0.85])

plot_button = buttons_left.button("Fit and plot", on_click=fit_and_plot, type="primary")

dl_button = buttons_left.download_button(
    label="Download plots",
    data=st.session_state.file_bytes if st.session_state.file_bytes else b"",
    file_name=f"plots_{st.session_state.file_timestamp}.zip",
    mime="application/zip",
    type="primary",
    disabled=st.session_state.dl_button_disabled,
)

data_tab, fit_tab, plot_tab, style_tab, view_tab = st.tabs(
    ["Data", "Fit options", "Plot options", "Style options", "Plot view"]
)

data_dict = tabs.data_tab_table_csv(data_tab, data_dict)

fit_dict = tabs.fit_options_tab(fit_tab, fit_dict)

plot_dict = tabs.plot_options_tab(plot_tab, plot_dict, len(data_dict["sample names"]))

table_style = tabs.style_options_tab(
    style_tab,
    data_dict["sample table"]["Sample label"],
    data_dict["sample table"]["unique name"],
    plot_dict["number of plots"],
)

tabs.plot_view_tab(view_tab, st.session_state.plot_list)
