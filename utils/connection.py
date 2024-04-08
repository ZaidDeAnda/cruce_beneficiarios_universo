from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
from utils.config import Config

@st.cache_resource
def connect(secrets):
    DATABASE_CONNECTION = f'mssql://{secrets["USERNAME"]}:{secrets["PASSWORD"]}@{secrets["SERVER"]}/{secrets["DATABASE"]}?driver={secrets["DRIVER"]}'

    engine = create_engine(DATABASE_CONNECTION)
    connection = engine.connect()

    return connection


