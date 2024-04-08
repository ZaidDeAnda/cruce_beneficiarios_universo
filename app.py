import streamlit as st
from io import StringIO

from utils.data import read_data_from_sql

st.set_page_config(page_title="Buscador de universos beneficiarios", page_icon="🔍")

st.header("Sistema de búsqueda para universos de beneficiarios")

st.subheader("Ingresa tu archivo txt aquí ⬇⬇⬇")


curp_file = st.file_uploader("Sube el archivo .txt con los CURPS en múltiples lineas", type=[".txt"])

st.warning("Nota: El archivo debe contener curps separados por un salto de línea. Es decir:")

st.code(
    '''
    CURPEJEMPLO1
    CURPEJEMPLO2
    CURPEJEMPLO3
    '''
        )

if curp_file:

    st.header("Resultados de la búsqueda:")

    stringio = StringIO(curp_file.getvalue().decode("utf-8"))
    curp_str = stringio.read()

    curp_list = curp_str.split('\n')

    try:
        df = read_data_from_sql('ps', curp_list)

        st.subheader("Beneficiarios directos:")

        df.loc[df['IDEstatusBeneficiario'] == "4"]

        st.subheader("Beneficiarios indirectos:")

        df.loc[df['IDEstatusBeneficiario'] != "4"]

        st.subheader('No beneficiarios')

        for element in list(set(curp_list) - set(df['CURP'])):

            st.write(f' * {element}')

    except(Exception) as e:
        print(e)
        st.warning("Los curps que introduciste están mal escritos. Asegúrate de que esten bien")

    