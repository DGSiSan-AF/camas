#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import numpy as np
# import chardet
# import getpass
import oracledb
# from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv("access_credentials.env")


# In[2]:


# def table2df (query):
#     #global df
#     connection = oracledb.connect(
#     user= os.getenv("usuario"),
#     password= os.getenv("pw"),
#     host = os.getenv("hosting"),
#     port = os.getenv("puerto"),
#     service_name = os.getenv("servicio"))
#     print("Successfully connected to Oracle Database")

#     engine = create_engine('oracle+oracledb://', creator=lambda: connection)
#     # Get the data into a DataFrame
    
#     df = pd.read_sql(query, engine)
#     connection.close()
#     return df
    


# Streamlit

# In[ ]:


if "df_loaded" not in st.session_state:
    #--------------------------------------------------------------------------------version db
    # st.session_state["df_efector"] = table2df("select * from USUARIO_MF.LUGAR_ESTABLECIMIENTO_SANITARI")
    # st.session_state["df_edificio"] = table2df("select * from USUARIO_MF.LUGAR_EDIFICIO")
    # st.session_state["df_planta"] = table2df("select * from USUARIO_MF.LUGAR_PLANTA")
    # st.session_state["df_local"] = table2df("select * from USUARIO_MF.LUGAR_LOCAL")
    # st.session_state["df_sector"] = table2df("select * from USUARIO_MF.LUGAR_SECTOR")
    # st.session_state["df_sublocal"] = table2df("select * from USUARIO_MF.LUGAR_SUBLOCAL")
    # st.session_state["df_elemento"] = table2df("select * from USUARIO_MF.LUGAR_ELEMENTO")
    # st.session_state["df_t_elemento"] = table2df("select * from USUARIO_MF.LUGAR_TIPO_ELEMENTO")
    # st.session_state["df_loaded"] = True
    #-----------------------------------------------------------------------------------version csv
    st.session_state["df_efector"] = pd.read_csv(".//db//efectores.csv")
    st.session_state["df_edificio"] = pd.read_csv(".//db//edificios.csv")
    st.session_state["df_planta"] = pd.read_csv(".//db//plantas.csv")
    st.session_state["df_local"] = pd.read_csv(".//db//locales.csv", sep=";")
    st.session_state["df_sector"] = pd.read_csv(".//db//sectores.csv")
    st.session_state["df_sublocal"] = pd.read_csv(".//db//sublocales.csv")
    st.session_state["df_elemento"] = pd.read_csv(".//db//elementos.csv")
    st.session_state["df_t_elemento"] = pd.read_csv(".//db//t_elementos.csv")
    st.session_state["df_t_sector"] = pd.read_csv(".//db//tipo_sector.csv", sep=";")
    st.session_state["df_loaded"] = True    
df_efector = st.session_state["df_efector"] 
df_edificio = st.session_state["df_edificio"]
df_planta = st.session_state["df_planta"]
df_local = st.session_state["df_local"]
df_sector = st.session_state["df_sector"]
df_t_sector = st.session_state["df_t_sector"]
df_sublocal = st.session_state["df_sublocal"]
df_elemento = st.session_state["df_elemento"]
df_t_elemento = st.session_state["df_t_elemento"]


# Jupiter Notebbok

# In[3]:


# df_efector = table2df("select * from USUARIO_MF.LUGAR_ESTABLECIMIENTO_SANITARI")
# df_edificio = table2df("select * from USUARIO_MF.LUGAR_EDIFICIO")
# df_planta = table2df("select * from USUARIO_MF.LUGAR_PLANTA")
# df_local = table2df("select * from USUARIO_MF.LUGAR_LOCAL")
# df_sector = table2df("select * from USUARIO_MF.LUGAR_SECTOR")
# df_sublocal = table2df("select * from USUARIO_MF.LUGAR_SUBLOCAL")
# df_elemento = table2df("select * from USUARIO_MF.LUGAR_ELEMENTO")
# df_t_elemento = table2df("select * from USUARIO_MF.LUGAR_TIPO_ELEMENTO")


# In[71]:


# df_efector.to_csv(".//db//efectores.csv",index=False)
# df_edificio.to_csv(".//db//edificios.csv",index=False)
# df_planta.to_csv(".//db//plantas.csv",index=False)
# df_local.to_csv(".//db//locales.csv",index=False)
# df_sublocal.to_csv(".//db//sublocales.csv",index=False)
# df_sector.to_csv(".//db//sectores.csv",index=False)
# df_elemento.to_csv(".//db//elementos.csv",index=False)
# df_t_elemento.to_csv(".//db//t_elementos.csv",index=False)


# In[74]:


# df_efector = pd.read_csv(".//db//efectores.csv")
# df_edificio = pd.read_csv(".//db//edificios.csv")
# df_planta = pd.read_csv(".//db//plantas.csv")
# df_local = pd.read_csv(".//db//locales.csv", sep=";")
# df_sector = pd.read_csv(".//db//sectores.csv", sep=";")
# df_t_sector = pd.read_csv(".//db//tipo_sector.csv", sep=";")
# df_sublocal = pd.read_csv(".//db//sublocales.csv")
# df_elemento = pd.read_csv(".//db//elementos.csv")
# df_t_elemento = pd.read_csv(".//db//t_elementos.csv")


# In[60]:


def df_joins ():
    result = pd.merge(
        df_t_elemento, df_elemento,
        how='right',
        left_on='id_tipo_elemento', right_on='id_tipo_elemento', 
        suffixes=('','_elemento')
    )

    result = pd.merge(
        result, df_sublocal,
        how='right',
        left_on='id_sublocal', right_on='id_sublocal', 
        suffixes=('','_sublocal')
    )

    result = pd.merge(
        result, df_local,
        how='right',
        left_on='id_local_sublocal', right_on='id_local', 
        suffixes=('','_local')
    )

    result = pd.merge(
        result, df_sector,
        how='right',
        left_on='id_sector_local', right_on='cod_sector', 
        suffixes=('','_sector')
    )

    result = pd.merge(
        result, df_t_sector,
        how='right',
        left_on='tipo_sector', right_on='id_tipo_sector', 
        suffixes=('','_t_sector')
    )

    result = pd.merge(
        result, df_planta,
        how='right',
        left_on='id_planta', right_on='id_planta', 
        suffixes=('','_planta')
    )

    result = pd.merge(
        result, df_edificio,
        how='right',
        left_on='id_edificio', right_on='id_edificio', 
        suffixes=('','_edificio')
    )

    result = pd.merge(
        result, df_efector,
        how='right',
        left_on='id_establecimiento', right_on='id_establecimiento', 
        suffixes=('','_efector')
    )



    # Seleccionamos las columnas deseadas y las renombramos si es necesario
    final_result = result[[
        'id_tipo_elemento', 'descripcion',  # 'descripcion_x' de lugar_tipo_elemento
        'id_elemento', 'detalle',            # 'detalle' de lugar_elemento
        'id_sublocal', 'descripcion_sublocal',      # 'descripcion_y' de lugar_sublocal
        'id_local_local', 'descripcion_local',         # 'descripcion_x' de lugar_local
        'cod_sector', 'descripcion_sector',       # 'descripcion_y' de lugar_sector
        'id_planta', 'descripcion_planta',        # 'descripcion_x' de lugar_planta
        'id_edificio', 'descripcion_edificio',      # 'descripcion_y' de lugar_edificio
        'id_establecimiento', 'descripcion_efector',  # 'descripcion_x' de lugar_establecimiento_sanitari
        'tipo_sector', 'descripcion_t_sector'
    ]]

    # Renombramos las columnas finales para que tengan nombres consistentes
    final_result.columns = [
        'id_tipo_elemento', 'tipo_elemento_det',
        'id_elemento', 'elemento_det',
        'id_sublocal', 'sublocal_det',
        'id_local', 'local_det',
        'cod_sector', 'sector_det',
        'id_planta', 'planta_det',
        'id_edificio', 'edificio_det',
        'id_establecimiento', 'establ_det',
        'tipo_sector' ,'tipo_sector_det'
    ]
    return final_result

    


# In[61]:


df_merged = df_joins()


# In[ ]:


# Interfaz de la app
st.title("Gestión de Hospitales y Camas")
st.write("Selecciona un Efector")

# gb = GridOptionsBuilder.from_dataframe(df_merged)
# gb.configure_pagination(paginationAutoPageSize=True)
# gb.configure_side_bar()
# gb.configure_default_column(editable=True, groupable=True)
# grid_options = gb.build()

# df_merged_p = df_merged.groupby(
#     ["id_establecimiento", "detalle_establecimiento"], as_index=False
# ).sum()

# Selector de hospital

hospitales = df_efector[["id_establecimiento", "descripcion"]].drop_duplicates()
hospitales["id_establecimiento"] = hospitales["id_establecimiento"].fillna(0)
hospital_seleccionado = st.selectbox(
    "Selecciona un hospital:", 
    options=hospitales["id_establecimiento"].tolist(), 
    format_func=lambda x: hospitales[hospitales["id_establecimiento"] == x]["descripcion"].values[0]
)
# # st.write(hospital_seleccionado)

st.write("El efector cuenta con las siguientes dependencias")

st.write("Edificio")
# st.write(hospital_seleccionado)
edificios = df_merged[df_merged["id_establecimiento"] == int(hospital_seleccionado)][["id_edificio", "edificio_det"]].drop_duplicates()
edificios["id_edificio"] = edificios["id_edificio"].fillna(0)
# st.dataframe(sectores)
# Manejar el caso de sectores vacíos
if edificios.empty:
    st.warning("No hay Edificios disponibles para este hospital.")
    edificio_seleccionado = None
else:
    edificio_seleccionado = st.selectbox(
        "Selecciona un Edificio:",
        options=edificios["id_edificio"].tolist(),
        format_func=lambda x: edificios[edificios["id_edificio"] == x]["edificio_det"].values[0]
    )

st.write("Plantas")
# st.write(hospital_seleccionado)
plantas = df_merged[
    (df_merged["id_establecimiento"] == int(hospital_seleccionado)) &
    (df_merged["id_edificio"] == int(edificio_seleccionado))
    ][["id_planta", "planta_det"]].drop_duplicates()
plantas["id_planta"] = plantas["id_planta"].fillna(0)
# st.dataframe(sectores)
# Manejar el caso de sectores vacíos
if plantas.empty:
    st.warning("No hay plantas disponibles para este hospital.")
    planta_seleccionada = None
else:
    planta_seleccionada = st.selectbox(
        "Selecciona una Planta:",
        options=plantas["id_planta"].tolist(),
        format_func=lambda x: plantas[plantas["id_planta"] == x]["planta_det"].values[0]
    )

st.write("Locales")
# st.write(hospital_seleccionado)
locales = df_merged[
    (df_merged["id_establecimiento"] == int(hospital_seleccionado)) & 
    (df_merged["id_planta"] == int(planta_seleccionada))
    ][["id_local", "local_det"]].drop_duplicates()
locales["id_local"] = locales["id_local"].fillna(0)
# st.dataframe(sectores)
# Manejar el caso de sectores vacíos
if locales.empty:
    st.warning("No hay locales disponibles para este hospital.")
    local_seleccionado = None
else:
    local_seleccionado = st.selectbox(
        "Selecciona un Local:",
        options=locales["id_local"].tolist(),
        format_func=lambda x: locales[locales["id_local"] == x]["local_det"].values[0]
    )

st.write("Tipo de Sector")

t_sectores = df_merged[
    (df_merged["id_establecimiento"] == int(hospital_seleccionado)) &
    (df_merged["id_local"] == int(local_seleccionado))
    ][["tipo_sector", "tipo_sector_det"]].drop_duplicates()
t_sectores["tipo_sector"] = t_sectores["tipo_sector"].dropna()
# st.dataframe(sectores)
# Manejar el caso de sectores vacíos
if t_sectores.empty:
    st.warning("No hay tipos de sectores disponibles para este hospital.")
    t_sector_seleccionado = None
else:
    t_sector_seleccionado = st.selectbox(
        "Tipo sector:",
        options=t_sectores["tipo_sector"].tolist(),
        format_func=lambda x: t_sectores[t_sectores["tipo_sector"] == x]["tipo_sector_det"].values[0]
    )

sectores = df_merged[
    (df_merged["id_establecimiento"] == int(hospital_seleccionado)) &
    (df_merged["id_local"] == int(local_seleccionado))
    ][["cod_sector", "sector_det"]].drop_duplicates()
sectores["cod_sector"] = sectores["cod_sector"].fillna(0)
sectores["sector_det"] = sectores["sector_det"].fillna('Cargar Detalle')
# st.dataframe(sectores)
# Manejar el caso de sectores vacíos
if sectores.empty:
    st.warning("No hay sectores disponibles para este hospital.")
    sector_seleccionado = None
else:
    sector_seleccionado = st.selectbox(
        "Sector asignado:",
        options=sectores["cod_sector"].tolist(),
        format_func=lambda x: sectores[sectores["cod_sector"] == x]["sector_det"].values[0]
    )
    # st.write(sector_seleccionado)
    sector_det_carga = st.text_input("Nuevo detalle del sector")
    if st.button("Actualizar detalle del sector"):        
        # sector_det_carga = st.text_input("Detalle")
        st.session_state["df_sector"].loc[st.session_state["df_sector"]["cod_sector"] == sector_seleccionado,'descripcion'] = sector_det_carga
        st.success("Detalle actualizado correctamente.")

# st.write(hospital_seleccionado)
sublocales = df_merged[
    (df_merged["id_establecimiento"] == int(hospital_seleccionado)) &
    (df_merged["id_local"] == int(local_seleccionado))
    ][["id_sublocal", "sublocal_det"]].drop_duplicates()
sublocales["id_sublocal"] = sublocales["id_sublocal"].fillna(0)
sublocales["sublocal_det"] = sublocales["sublocal_det"].fillna('Debe cargar sublocal')
# st.dataframe(sectores)
# Manejar el caso de sectores vacíos
if sublocales.empty:
    st.warning("No hay sublocales disponibles para este local.")
    sublocal_seleccionado = None
else:
    sublocal_seleccionado = st.selectbox(
        "Selecciona un Sublocal:",
        options=sublocales["id_sublocal"].tolist(),
        format_func=lambda x: sublocales[sublocales["id_sublocal"] == x]["sublocal_det"].values[0]
    )
    # if st.button("Crear un nuevo sublocal"):                
        # sublocal_det_carga = st.text_input("Nombre del Sublocal")
    st.write("**Agregar nuevo sublocal**")
    with st.form("Agregar Sublocal"):
        dotacion_map = {"Si": "S", "No": "N"}  # Diccionario para mapear valores
        nuevo_id_sublocal = 1 if df_sublocal.empty else df_sublocal["id_sublocal"].max() + 1
        nuevo_sublocal = pd.DataFrame([{
        "id_sublocal": nuevo_id_sublocal,
        "descripcion": st.text_input("Nombre del Sublocal"),
        "descripcion_numerica" : 1,
        "estado" : 'A',
        "fecha_alta" : datetime.now(),
        "fecha_baja" : None,
        "fecha_ultima_modificacion" : datetime.now(),
        "id_local": local_seleccionado,
        "cod_dominio" : None,
        "id_usuario": 1,
        "dotacion" : st.selectbox("Selecciona dotación:",
                    options=list(dotacion_map.keys())  # Mostramos "Si" y "No"
                    ),
        "id_sector" : sector_seleccionado
        
        # "id_establecimiento": hospital_seleccionado
        }])
        if st.form_submit_button("Agregar Sublocal"):        
            # df_sublocal = pd.concat([df_sublocal, nuevo_sublocal],axis=0)           # st.session_state["df_elemento"].append(nueva_fila, ignore_index=True)
            st.session_state.df_sublocal = pd.concat([st.session_state.df_sublocal, nuevo_sublocal], axis=0, ignore_index=True)
            st.success("Fila agregada exitosamente.")
            st.table(st.session_state.df_sublocal)
            st.session_state.df_sublocal.to_csv(".\\db\\sublocales.csv",index=False)

# Filtrar datos por hospital seleccionado
datos_filtrados = df_merged[
    # [df_merged["id_establecimiento"] == hospital_seleccionado,
    # df_merged["cod_sector"] == sector_seleccionado]
            (df_merged["id_establecimiento"] == hospital_seleccionado) &
            # (df_merged["cod_sector"] == sector_seleccionado) &
            (df_merged["id_planta"] == planta_seleccionada) &
            (df_merged["id_local"] == local_seleccionado) &
            (df_merged["id_sublocal"] == sublocal_seleccionado)
    ]



# Mostrar datos filtrados
st.subheader("Tabla de Elementos en el sublocal")
if datos_filtrados.empty:
    st.write("**No hay datos para mostrar.**")
else:
    st.dataframe(datos_filtrados)

# # Visualización con ag-Grid
#     st.title("Visualización de Datos con ag-Grid")


    # AgGrid(
    #     datos_filtrados,
    #     gridOptions=grid_options,
    #     height=600,
    #     width="100%",
    #     enable_enterprise_modules=True
    # )

# Formulario para agregar camas

# Botón para resetear filtros
if st.button("Resetear filtros"):
    st.experimental_rerun()

# st.subheader("Agregar Elementos al Sublocal")
# num_camas = st.number_input("Número de camas a agregar:", min_value=1, step=1)

# if st.button("Agregar elementos"):
#     st.success(f"Se han agregado {num_camas} camas al hospital seleccionado.")

# Agregar nueva fila
st.subheader("Agregar Elementos en el sublocal")
with st.form("Agregar Elemento"):
    nuevo_elemento = pd.DataFrame([{
        "id_tipo_elemento": st.selectbox(
                "Selecciona un elemento:", 
                options=df_t_elemento["id_tipo_elemento"].tolist(), 
                format_func=lambda x: df_t_elemento[df_t_elemento["id_tipo_elemento"] == x]["descripcion"].values[0]
            ),
        "detalle": st.text_input("Detalle"),
        "cantidad" : 1,
        "estado" : 'A',
        "fecha_alta" : datetime.now(),
        "fecha_baja" : None,
        "fecha_ultima_modificacion" : datetime.now(),
        "id_local": None,
        "id_sublocal": sublocal_seleccionado,
        "id_mostrador" : None,
        "id_elemento" : df_elemento['id_elemento'].max()+1,
        "cod_dominio" : None
        # "id_establecimiento": hospital_seleccionado
        }])

    if st.form_submit_button("Agregar Elemento"):
        # df_add_el = pd.DataFrame(nueva_fila)
        st.session_state["df_elemento"] = pd.concat([st.session_state["df_elemento"], nuevo_elemento], axis=0)
        # st.session_state["df_elemento"].append(nueva_fila, ignore_index=True)
        
        st.success("Fila agregada exitosamente.")
        nuevo_merge = pd.DataFrame([{
        "id_tipo_elemento": nuevo_elemento['id_tipo_elemento'].values[0],
        "tipo_elemento_det": df_t_elemento.loc[(df_t_elemento['id_tipo_elemento']==nuevo_elemento['id_tipo_elemento'].values[0],'descripcion')].values[0],
        "id_elemento" : nuevo_elemento['id_elemento'].values[0],
        "elemento_det" : nuevo_elemento['detalle'].values[0],
        # "fecha_alta" : datetime.now(),
        # "fecha_baja" : None,
        # "fecha_ultima_modificacion" : datetime.now(),
        "id_local": local_seleccionado,
        "local_det" : st.session_state["df_local"].loc[(st.session_state["df_local"]['id_local']==local_seleccionado,'descripcion')].values[0],
        "id_sublocal": sublocal_seleccionado,
        "sublocal_det" :st.session_state["df_sublocal"].loc[(st.session_state["df_sublocal"]['id_sublocal']==nuevo_elemento['id_sublocal'].values[0],'descripcion')].values[0],
        "cod_sector" : sector_seleccionado,
        "sector_det" : None,
        "id_planta" : None,
        "planta_det" : None,
        "id_edificio" : None,
        "edificio_det" : None,
        "id_establecimiento" : None,
        "establ_det" : None,
        "tipo_sector" : None
        # "id_establecimiento": hospital_seleccionado
    }])
        datos_filtrados = pd.concat([datos_filtrados, nuevo_merge], axis=0)        # st.dataframe(df_elemento)
        st.dataframe(datos_filtrados)
    st.session_state["df_sector"].to_csv(".//db//sectores.csv",index=False)
    st.session_state["df_elemento"].to_csv(".//db//elementos.csv",index=False)
    # df_sublocal.to_csv(".//db//sublocales.csv",index=False)

