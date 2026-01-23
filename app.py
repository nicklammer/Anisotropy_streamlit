import streamlit as st
import pandas as pd
import tempfile
import time

import tabs
from scripts import commands

st.set_page_config(layout="wide")

data_dict = {}
fit_dict = {}
plot_dict = {}

st.title("Analyze Fluorescence Anisotropy")
# st.header("Self fill")

buttons_left, buttons_right = st.columns([0.15, 0.85])
plot_button = buttons_left.button("Fit and plot", type="primary")
save_button = buttons_right.button("Save parameters")

data_tab, fit_tab, plot_tab, style_tab = st.tabs(
    ["Data", "Fit options", "Plot options", "Style options"]
)

data_dict = tabs.data_tab_selffill(data_tab, data_dict)

fit_dict = tabs.fit_options_tab(fit_tab, fit_dict)

plot_dict = tabs.plot_options_tab(plot_tab,
                                  plot_dict,
                                  len(data_dict["sample names"]))

table_style = tabs.style_options_tab(style_tab,
                       data_dict["sample table"]["Sample label"],
                       data_dict["sample table"]["unique name"],
                       plot_dict["number of plots"])

with tempfile.TemporaryDirectory() as tmpdir:
    if plot_button:
        outzip = commands.process_anisotropy(data_dict, fit_dict, plot_dict, table_style, tmpdir)
#         with st.spinner("Processing data...", show_time=True):
            # for file in encr_logs:
            #     encrypted_filenames.append(file.name)
            #     with open(f"{tmpdir}/{file.name}", "wb") as tmp_file:
            #         tmp_file.write(file.getvalue())
            # outzip = crypto_main.decrypt_parse_logs(encrypted_filenames, tmpdir,
            #                                    log_samples, parse_check,
            #                                    compile_check, segment_logs_check,
            #                                    keep_logs_check)
        #     st.success("Done!")
        with open(outzip, "rb") as file:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            st.download_button("Download logs", data=file, on_click='ignore',
                               file_name=f'plots_{timestamp}.zip')