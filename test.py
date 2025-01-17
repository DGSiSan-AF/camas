#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import chardet
import getpass
import oracledb
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv
import streamlit as st
# import pandasql as ps
import duckdb as dk
# from st_aggrid import AgGrid
# from st_aggrid.grid_options_builder import GridOptionsBuilder

load_dotenv("access_credentials.env")


# In[2]:


def table2df (query):
    #global df
    connection = oracledb.connect(
    user= os.getenv("usuario"),
    password= os.getenv("pw"),
    host = os.getenv("hosting"),
    port = os.getenv("puerto"),
    service_name = os.getenv("servicio"))
    print("Successfully connected to Oracle Database")

    engine = create_engine('oracle+oracledb://', creator=lambda: connection)
    # Get the data into a DataFrame
    
    df = pd.read_sql(query, engine)
    connection.close()
    return df
    


# In[3]:


def agregar_elemento(h,c):
    return h


# In[ ]:


# q1 = "select * from USUARIO_MF.LUGAR_ESTABLECIMIENTO_SANITARI"
# df_efector = table2df(q1)


# In[ ]:


# q2 = "select * from USUARIO_MF.LUGAR_EDIFICIO"
# df_edificio = table2df(q2)


# In[ ]:


# q3 = "select * from USUARIO_MF.LUGAR_PLANTA"
# df_planta = table2df(q3)


# In[ ]:


# q4 = "select * from USUARIO_MF.LUGAR_LOCAL"
# df_local = table2df(q4)


# In[ ]:


# q5 = "select * from USUARIO_MF.LUGAR_SECTOR"
# df_sector = table2df(q5)


# In[ ]:


# q6 = "select * from USUARIO_MF.LUGAR_SUBLOCAL"
# df_sublocal = table2df(q6)


# In[ ]:


# q7 = "select * from USUARIO_MF.LUGAR_ELEMENTO"
# df_elemento = table2df(q7)


# In[ ]:


# q8 = "select * from USUARIO_MF.LUGAR_TIPO_ELEMENTO"
# df_t_elemento = table2df(q8)


# In[60]:


if "df_loaded" not in st.session_state:
    st.session_state["df_efector"] = table2df("select * from USUARIO_MF.LUGAR_ESTABLECIMIENTO_SANITARI")
    st.session_state["df_edificio"] = table2df("select * from USUARIO_MF.LUGAR_EDIFICIO")
    st.session_state["df_planta"] = table2df("select * from USUARIO_MF.LUGAR_PLANTA")
    st.session_state["df_local"] = table2df("select * from USUARIO_MF.LUGAR_LOCAL")
    st.session_state["df_sector"] = table2df("select * from USUARIO_MF.LUGAR_SECTOR")
    st.session_state["df_sublocal"] = table2df("select * from USUARIO_MF.LUGAR_SUBLOCAL")
    st.session_state["df_elemento"] = table2df("select * from USUARIO_MF.LUGAR_ELEMENTO")
    st.session_state["df_t_elemento"] = table2df("select * from USUARIO_MF.LUGAR_TIPO_ELEMENTO")
    st.session_state["df_loaded"] = True
df_efector = st.session_state["df_efector"]
df_edificio = st.session_state["df_edificio"]
df_planta = st.session_state["df_planta"]
df_local = st.session_state["df_local"]
df_sector = st.session_state["df_sector"]
df_sublocal = st.session_state["df_sublocal"]
df_elemento = st.session_state["df_elemento"]
df_t_elemento = st.session_state["df_t_elemento"]



# In[ ]:





# In[47]:


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
    left_on='id_lugar', right_on='id_establecimiento', 
    suffixes=('','_efector')
)


# In[58]:


# result.info()


# In[52]:


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
    'tipo_sector'
]]


# In[54]:


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
    'tipo_sector'
]

# Resultado final
# print(final_result)


# In[55]:


# final_result.info()


# In[84]:


df_sublocal.info()


# In[75]:


nuevo_elemento = pd.DataFrame([{
    "id_tipo_elemento": 3,
    "detalle": 'prueba',
    "cantidad" : 1,
    "estado" : 'A',
    "fecha_alta" : datetime.now(),
    "fecha_baja" : None,
    "fecha_ultima_modificacion" : datetime.now(),
    "id_local": None,
    "id_sublocal": 1,
    "id_mostrador" : None,
    "id_elemento" : df_elemento['id_elemento'].max()+1,
    "cod_dominio" : None
    # "id_establecimiento": hospital_seleccionado
    }])


# In[80]:


# type(nuevo_elemento['id_tipo_elemento'].values[0])


# In[ ]:


# df_merged = (
#     df_t_elemento
#     .merge(df_elemento, how='inner', left_on='id_tipo_elemento', right_on='id_tipo_elemento', suffixes=('','_elemento'))
#     .merge(df_sublocal, how='inner', left_on='id_sublocal', right_on='id_sublocal',suffixes=('','_sublocal'))
    # .merge(df_local, how='inner', left_on='id_local', right_on='id_local',suffixes=('','_local'))
    # .merge(df_sector, how='inner', left_on='id_sector', right_on='id_sector',suffixes=('','_sector'))
    # .merge(df_planta, how='inner', left_on='id_planta', right_on='id_planta',suffixes=('','_planta'))
    # .merge(df_edificio, how='inner', left_on='id_edificio', right_on='id_edificio',suffixes=('','_edificio'))
    # .merge(df_efector, how='inner', left_on='id_establecimiento', right_on='id_establecimiento',suffixes=('','_establecimiento'))
# )


# In[13]:


# query1 = """
# SELECT 
#     df_efector.id_establecimiento, df_efector.descripcion AS establ_det,
#     df_edificio.id_edificio, df_edificio.descripcion AS edificio_det,
#     df_planta.id_planta, df_planta.descripcion AS planta_det,
#     df_sector.tipo_sector,
#     df_sector.cod_sector , df_sector.descripcion AS sector_det,
#     df_local.id_local, df_local.descripcion AS local_det,
# 	df_sublocal.id_sublocal, df_sublocal.descripcion AS sublocal_det,    
#     df_t_elemento.id_tipo_elemento , df_t_elemento.descripcion,   
#     df_elemento.id_elemento, df_elemento.detalle AS elemento_det
    
# FROM
# 	df_t_elemento 
# RIGHT JOIN
#     df_elemento ON df_t_elemento.id_tipo_elemento = df_elemento.id_tipo_elemento 
#  RIGHT JOIN 
#     df_sublocal ON df_elemento.id_sublocal = df_sublocal.id_sublocal
# RIGHT JOIN 
#     df_local ON df_sublocal.id_local = df_local.id_local
# RIGHT JOIN
# 	df_sector ON df_local.id_sector = df_sector.cod_sector 
# RIGHT JOIN 
#     df_planta ON df_planta.id_planta = df_planta.id_planta
# RIGHT JOIN 
#     df_edificio ON df_planta.id_edificio = df_edificio.id_edificio
# RIGHT JOIN 
# 	df_efector ON df_edificio.id_establecimiento = df_efector.id_establecimiento
#     """


# In[21]:


# df_merged1 = ps.sqldf(query1, locals())
# df_merged = dk.query(query1).to_df()


# In[56]:


# final_result.to_excel("final_res_v1.xlsx")


# In[64]:


final_result.info()


# In[ ]:


df_merged = final_result


# In[20]:


# Interfaz de la app
st.title("Gestión de Hospitales y Camas")
st.write("Selecciona un hospital y agrega camas según sea necesario.")

# gb = GridOptionsBuilder.from_dataframe(df_merged)
# gb.configure_pagination(paginationAutoPageSize=True)
# gb.configure_side_bar()
# gb.configure_default_column(editable=True, groupable=True)
# grid_options = gb.build()

# df_merged_p = df_merged.groupby(
#     ["id_establecimiento", "detalle_establecimiento"], as_index=False
# ).sum()

# Selector de hospital

hospitales = df_merged[["id_establecimiento", "establ_det"]].drop_duplicates()
hospitales["id_establecimiento"] = hospitales["id_establecimiento"].fillna(0)
hospital_seleccionado = st.selectbox(
    "Selecciona un hospital:", 
    options=hospitales["id_establecimiento"].tolist(), 
    format_func=lambda x: hospitales[hospitales["id_establecimiento"] == x]["establ_det"].values[0]
)


# st.write(hospital_seleccionado)
locales = df_merged[df_merged["id_establecimiento"] == int(hospital_seleccionado)][["id_local", "local_det"]].drop_duplicates()
locales["id_local"] = locales["id_local"].fillna(0)
# st.dataframe(sectores)
# Manejar el caso de sectores vacíos
if locales.empty:
    st.warning("No hay sectores disponibles para este hospital.")
    local_seleccionado = None
else:
    local_seleccionado = st.selectbox(
        "Selecciona un Local:",
        options=locales["id_local"].tolist(),
        format_func=lambda x: locales[locales["id_local"] == x]["local_det"].values[0]
    )

# st.write(hospital_seleccionado)
sublocales = df_merged[df_merged["id_establecimiento"] == int(hospital_seleccionado)][["id_sublocal", "sublocal_det"]].drop_duplicates()
sublocales["id_sublocal"] = sublocales["id_sublocal"].fillna(0)
# st.dataframe(sectores)
# Manejar el caso de sectores vacíos
if sublocales.empty:
    st.warning("No hay sectores disponibles para este hospital.")
    sublocal_seleccionado = None
else:
    sublocal_seleccionado = st.selectbox(
        "Selecciona un Sublocal:",
        options=sublocales["id_sublocal"].tolist(),
        format_func=lambda x: sublocales[sublocales["id_sublocal"] == x]["sublocal_det"].values[0]
    )

# st.write(hospital_seleccionado)
sectores = df_merged[df_merged["id_establecimiento"] == int(hospital_seleccionado)][["cod_sector", "sector_det"]].drop_duplicates()
sectores["cod_sector"] = sectores["cod_sector"].fillna(0)
# st.dataframe(sectores)
# Manejar el caso de sectores vacíos
if sectores.empty:
    st.warning("No hay sectores disponibles para este hospital.")
    sector_seleccionado = None
else:
    sector_seleccionado = st.selectbox(
        "Selecciona un sector:",
        options=sectores["cod_sector"].tolist(),
        format_func=lambda x: sectores[sectores["cod_sector"] == x]["sector_det"].values[0]
    )

# Filtrar datos por hospital seleccionado
datos_filtrados = df_merged[
    # [df_merged["id_establecimiento"] == hospital_seleccionado,
    # df_merged["cod_sector"] == sector_seleccionado]
            (df_merged["id_establecimiento"] == hospital_seleccionado) &
            (df_merged["cod_sector"] == sector_seleccionado) &
            (df_merged["id_local"] == local_seleccionado) &
            (df_merged["id_sublocal"] == sublocal_seleccionado)
    ]



# Mostrar datos filtrados
st.subheader("Tabla de Elementos en el sublocal")
if datos_filtrados.empty:
    st.write("No hay datos para mostrar.")
else:
    st.dataframe(datos_filtrados)

# Visualización con ag-Grid
    st.title("Visualización de Datos con ag-Grid")


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
with st.form("Agregar fila"):
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

    if st.form_submit_button("Agregar"):
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
        "local_det" : df_local.loc[(df_local['id_local']==local_seleccionado,'descripcion')].values[0],
        "id_sublocal": sublocal_seleccionado,
        "sublocal_det" :df_sublocal.loc[(df_sublocal['id_sublocal']==nuevo_elemento['id_sublocal'].values[0],'descripcion')].values[0],
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
        # st.dataframe(df_elemento)
        datos_filtrados = pd.concat([datos_filtrados, nuevo_merge], axis=0)
        st.dataframe(datos_filtrados)


# In[ ]:


# import pandas as pd
# import os
# import streamlit as st
# from st_aggrid import AgGrid
# from st_aggrid.grid_options_builder import GridOptionsBuilder
# from sqlalchemy import create_engine
# from dotenv import load_dotenv
# import oracledb

# # Cargar credenciales
# load_dotenv("access_credentials.env")

# # Función para cargar datos desde Oracle
# def table2df(query):
#     connection = oracledb.connect(
#         user=os.getenv("usuario"),
#         password=os.getenv("pw"),
#         host=os.getenv("hosting"),
#         port=os.getenv("puerto"),
#         service_name=os.getenv("servicio")
#     )
#     engine = create_engine('oracle+oracledb://', creator=lambda: connection)
#     df = pd.read_sql(query, engine)
#     connection.close()
#     return df

# # Carga inicial de datos en session_state
# if "df_loaded" not in st.session_state:
#     st.session_state["df_efector"] = table2df("select * from USUARIO_MF.LUGAR_ESTABLECIMIENTO_SANITARI")
#     st.session_state["df_edificio"] = table2df("select * from USUARIO_MF.LUGAR_EDIFICIO")
#     st.session_state["df_planta"] = table2df("select * from USUARIO_MF.LUGAR_PLANTA")
#     st.session_state["df_local"] = table2df("select * from USUARIO_MF.LUGAR_LOCAL")
#     st.session_state["df_sector"] = table2df("select * from USUARIO_MF.LUGAR_SECTOR")
#     st.session_state["df_sublocal"] = table2df("select * from USUARIO_MF.LUGAR_SUBLOCAL")
#     st.session_state["df_elemento"] = table2df("select * from USUARIO_MF.LUGAR_ELEMENTO")
#     st.session_state["df_t_elemento"] = table2df("select * from USUARIO_MF.LUGAR_TIPO_ELEMENTO")
#     st.session_state["df_loaded"] = True

# # Acceso a los DataFrames desde session_state
# df_efector = st.session_state["df_efector"]
# df_elemento = st.session_state["df_elemento"]

# # Interfaz de la app
# st.title("Gestión de Hospitales y Camas")

# # Filtros de hospital
# hospitales = df_efector[["id_establecimiento", "descripcion"]].drop_duplicates()
# hospital_seleccionado = st.selectbox(
#     "Selecciona un hospital:",
#     options=hospitales["id_establecimiento"].tolist(),
#     format_func=lambda x: hospitales[hospitales["id_establecimiento"] == x]["descripcion"].values[0]
# )

# # Filtros de sectores
# sectores = df_elemento[df_elemento["id_establecimiento"] == hospital_seleccionado][["cod_sector", "sector_det"]].drop_duplicates()
# sector_seleccionado = st.selectbox(
#     "Selecciona un sector:",
#     options=sectores["cod_sector"].tolist(),
#     format_func=lambda x: sectores[sectores["cod_sector"] == x]["sector_det"].values[0]
# )

# # Botón para resetear filtros
# if st.button("Resetear filtros"):
#     st.experimental_rerun()

# # Filtrar datos
# datos_filtrados = df_elemento[df_elemento["id_establecimiento"] == hospital_seleccionado]
# st.subheader("Datos filtrados")
# AgGrid(datos_filtrados)

# # Agregar nueva fila
# with st.form("Agregar fila"):
#     nueva_fila = {
#         "id_elemento": st.text_input("ID Elemento"),
#         "detalle": st.text_input("Detalle"),
#         "id_establecimiento": hospital_seleccionado
#     }
#     if st.form_submit_button("Agregar"):
#         st.session_state["df_elemento"] = st.session_state["df_elemento"].append(nueva_fila, ignore_index=True)
#         st.success("Fila agregada exitosamente.")

