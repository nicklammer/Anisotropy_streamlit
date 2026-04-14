"""
Reusable base components for Streamlit pages.
Contains common session state initialization and UI helpers.
"""
import streamlit as st
import tempfile
import time
import pathlib


@st.dialog("Help", width="large")
def help_dialog(doc_path: str):
    try:
        content = pathlib.Path(doc_path).read_text()
        st.markdown(content, width="stretch")
    except FileNotFoundError:
        st.warning("Help documentation not found.")


def setup_page_header(title: str, doc_file: str):
    """
    Renders the page title with a Help button at the top right.
    Clicking opens a dialog with content loaded from docs/{doc_file}.

    Args:
        title: Page title text
        doc_file: Filename (e.g., "anisotropy.md") inside the docs/ folder
    """
    docs_path = pathlib.Path(__file__).parent.parent / "docs" / doc_file
    title_col, help_col = st.columns([0.95, 0.05], vertical_alignment="bottom")
    title_col.title(title)
    if help_col.button("Help", key="help_button"):
        help_dialog(str(docs_path))


def init_session_state():
    """Initialize common session state variables with their defaults."""
    defaults = {
        "file_bytes": None,
        "file_timestamp": "",
        "dl_button_disabled": True,
        "plot_list": [],
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


def setup_download_buttons(plot_and_plot_func):
    """
    Set up the fit/plot button and download button.

    Args:
        plot_and_plot_func: Function to be called when "Fit and plot" button is clicked
    """
    buttons_col, _ = st.columns([0.15, 0.85])
    buttons_col.button("Fit and plot", on_click=plot_and_plot_func, type="primary")
    buttons_col.download_button(
        label="Download plots",
        data=st.session_state.file_bytes or b"",
        file_name=f"plots_{st.session_state.file_timestamp}.zip",
        mime="application/zip",
        type="primary",
        disabled=st.session_state.dl_button_disabled,
    )


def get_timestamp():
    """Get formatted timestamp for file naming."""
    return time.strftime("%Y%m%d_%H%M%S")


def setup_temp_processing(plot_func):
    """
    Setup temporary directory processing and update session state.
    
    Args:
        plot_func: Function that takes a temporary directory path and returns (zip_path, plot_list)
    
    Returns:
        Callable that can be used as the plot_and_plot_func
    """
    def run_processing():
        with tempfile.TemporaryDirectory() as tmpdir:
            outzip_path, plot_list = plot_func(tmpdir)
            st.session_state.plot_list = plot_list
            with open(outzip_path, "rb") as f:
                st.session_state.file_bytes = f.read()
        st.session_state.dl_button_disabled = False
        st.session_state.file_timestamp = get_timestamp()
        st.toast("Plots complete! Ready for download.")

    return run_processing