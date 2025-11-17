import streamlit as st
import pandas as pd

from helpers import generate_empty_plate
import tabs

st.set_page_config(layout="wide")


def run_analysis():
    return NotImplementedError


parameters = {}

st.title("Analyze Fluorescence Anisotropy - Self fill")

data_tab, fit_tab, plot_tab, style_tab = st.tabs(["Data", "Fit options", "Plot options", "Style options"])

tabs.data_tab_selffill(data_tab, parameters)

tabs.
