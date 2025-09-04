import streamlit as st
from st_pages import add_page_title, get_nav_from_toml
from utils.paths import abspath

st.set_page_config(layout="wide")
nav = get_nav_from_toml(abspath(".streamlit/pages.toml"))

pg = st.navigation(nav)

add_page_title(pg)
pg.run()
