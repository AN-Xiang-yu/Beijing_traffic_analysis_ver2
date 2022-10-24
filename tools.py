# tools.py

from zipfile import ZipFile
import pandas as pd
import streamlit as st

# Declaration of constants
# Line spacing between different figures
LINE_SPACE_FIGURE = 3


def add_line_feed(n_line):
    """ jump over a specified number of lines

    Args:
        n_line (int): the number of lines to jump
    """
    for i in range(0, n_line):
        st.markdown(
            """<br>""", unsafe_allow_html=True)


def dataset_table(data, page_name):
    """ show the table of the dataset

    Args:
        path (str): the path of the zip file
        page_name (str) : the name of the page

    Returns:
        pandas.DataFrame: the data gotten from the path
    """
    # subtitle of the dataset part
    st.markdown(
        f"""<h3 style='text-align: center;'>This is a data visualisation of my {page_name} dataset</h3>""", unsafe_allow_html=True)
    # show the dataset
    if st.button('Show dataset'):
        # show the table of the dataset
        st.dataframe(data)
    add_line_feed(LINE_SPACE_FIGURE)
