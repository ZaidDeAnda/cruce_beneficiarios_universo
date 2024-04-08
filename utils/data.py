import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import base64

from utils.config import Config
from utils.connection import connect

def read_data_from_sql(table, curp_list):
    config = Config()

    secrets = config.get_config()[table]

    conn = connect(secrets)

    curp_str = '(\'' + '\',\''.join(map(str, curp_list)) + '\')'

    query = f'''WITH viviendas_beneficiadas AS (
                SELECT
                    DV.IDVivienda
                FROM 
                    DatosBeneficiario as DB
                INNER JOIN 
                    BeneficiarioControl as BC
                ON 
                    DB.IDBeneficiario=BC.IDBeneficiario 
                INNER JOIN
                    DatosVivienda as DV
                ON 
                    DB.IDVivienda=DV.IDVivienda
                WHERE 
                    IDEstatusBeneficiario=4
            )
            SELECT 
                DB.CURP, 
                DB.IDVivienda, 
                DB.Nombre, 
                DB.Paterno, 
                DB.Materno, 
                DB.Celular,
                DV.Municipio,
                DV.Colonia,
                DV.Localidad,
                DV.CodigoPostal,
                DV.TelPart,
                DV.TelMovil,
                DV.TelRecado,
                DV.FechaAgrega as FechaAgregaVivienda,
                DV.Observaciones,
                BC.IDEstatusBeneficiario,
                BC.FechaAgrega as FechaAgregaBeneficiario,
                BC.FechaActualiza,
                BC.IDPrograma,
                BC.FechaAutorizacion,
                BC.FechaCancelacion
            FROM
                DatosBeneficiario as DB
            INNER JOIN
                BeneficiarioControl as BC
            ON
                DB.IDBeneficiario=BC.IDBeneficiario 
             INNER JOIN
                DatosVivienda as DV
            ON 
                DB.IDVivienda=DV.IDVivienda
            WHERE
                DB.IDVivienda IN (
                    SELECT IDVivienda from viviendas_beneficiadas
                    )
            AND DB.CURP IN {curp_str}
        '''
        
    data = pd.read_sql_query(query, conn)

    data.dropna(subset=["CURP"], inplace=True)

    return data

def download_button(object_to_download, download_filename):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    """

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    dl_link = f"""
    <html>
    <head>
    <title>Start Auto Download file</title>
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
    $('<a href="data:text/csv;base64,{b64}" download="{download_filename}">')[0].click()
    </script>
    </head>
    </html>
    """
    return dl_link


def download_df(table):
    df = read_data(table)
    csv = df.to_csv().encode('utf-8')
    components.html(
        download_button(csv, f"beneficiarios_{table}.csv"),
        height=0,)
