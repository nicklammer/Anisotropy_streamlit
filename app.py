import streamlit as st
import pandas as pd

import tabs

st.set_page_config(layout="wide")


def run_analysis():
    return NotImplementedError


parameters = {}

st.title("Analyze Fluorescence Anisotropy")
st.header("Self fill")

buttons_left, buttons_right = st.columns([0.15, 0.85])
plot_button = buttons_left.button("Fit and plot", type="primary")
save_button = buttons_right.button("Save parameters")

data_tab, fit_tab, plot_tab, style_tab = st.tabs(
    ["Data", "Fit options", "Plot options", "Style options"]
)

tabs.data_tab_selffill(data_tab, parameters)

tabs.fit_options_tab(fit_tab, parameters)

tabs.plot_options_tab(plot_tab, parameters)

tabs.style_options_tab(style_tab, parameters)
