import streamlit as st
import pandas as pd

from helpers import generate_empty_plate

st.set_page_config(layout="wide")

def run_analysis():
    return NotImplementedError

st.title("Analyze Fluorescence Anisotropy - Self fill")


st.write("Parallel fluorescence")
table_parallel = st.data_editor(generate_empty_plate(), key="parallel")

st.write("Perpendicular fluorescence")
table_perpendicular = st.data_editor(generate_empty_plate(), key="perpendicular")