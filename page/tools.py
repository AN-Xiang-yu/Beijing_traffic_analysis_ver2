# tools.py

import streamlit as st
import base64
from pathlib import Path

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


def img_to_bytes(img_path):
    """transferer the image to bytes

    Args:
        img_path (str): path of the image

    Returns:
        str: the bytes of the image
    """
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    """transferer the bytes of image to html

    Args:
        img_path (str): the bytes of the image

    Returns:
        str: the html of the image
    """
    img_html = "<img style='width: 30px;' src='data:image/png;base64,{}' alt={}>".format(
        img_to_bytes(img_path), img_path
    )
    return img_html
