#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import numpy as np
# import chardet
# import getpass
# import oracledb
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
    st.session_state["df_local"] = pd.read_csv(".//db//locales.csv")
    st.session_state["df_sector"] = pd.read_csv(".//db//sectores.csv")
    st.session_state["df_sublocal"] = pd.read_csv(".//db//sublocales.csv")
    st.session_state["df_elemento"] = pd.read_csv(".//db//elementos.csv")
    st.session_state["df_t_elemento"] = pd.read_csv(".//db//t_elementos.csv")
    st.session_state["df_t_sector"] = pd.read_csv(".//db//tipo_sector.csv", sep=";")
    st.session_state["creaSector"] = False
    st.session_state["creaSublocal"] = False
    st.session_state["creaElemento"] = False
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
        how='left',
        left_on='id_tipo_elemento', right_on='id_tipo_elemento', 
        suffixes=('','_elemento')
    )

    result = pd.merge(
        result, df_sublocal,
        how='left',
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
        how='left',
        left_on='id_sector_local', right_on='cod_sector', 
        suffixes=('','_sector')
    )

    result = pd.merge(
        result, df_t_sector,
        how='left',
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
        'cod_sector_sector', 'descripcion_sector',       # 'descripcion_y' de lugar_sector
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

    
def crear_elemento():
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
        # st.session_state["df_sector"].to_csv(".//db//sectores.csv",index=False)
        st.session_state["df_elemento"].to_csv(".//db//elementos.csv",index=False)
        # df_sublocal.to_csv(".//db//sublocales.csv",index=False)

def crear_sector():
    
    # if st.session_state["creaSector"]:
            
    st.write("### Crear Sector")


    # if st.button("Agregar Sector"):
    with st.form("Agregar Sector",clear_on_submit=True):

        sector_nombre = st.text_input("Nombre del nuevo Sector")

        locales_f = df_local[
            (df_local["id_planta"] == planta_seleccionada) & 
            # (df_merged["id_edificio"] == edificio_seleccionado) &
            # (df_merged["id_planta"] == planta_seleccionada) &
            (df_local["id_sector"].isnull()) #revisar df_local
            ]
        # st.table(locales_f)
        # st.table(locales_f)
        sector_locales = st.multiselect(
            "Selecciona los Locales:",
            options=locales_f["id_local"].tolist(),
            format_func=lambda x: locales_f[locales_f["id_local"] == x]["descripcion"].values[0]
            )
        
        t_sector_seleccionado = st.selectbox("Sector asignado:",
                                    options=df_t_sector["id_tipo_sector"].tolist(),
                                    format_func=lambda x: df_t_sector[df_t_sector["id_tipo_sector"] == x]["descripcion"].values[0]
                                    )

        

        # Crear un nuevo DataFrame con los datos del sector
        nuevo_id_sector = float(1.0 if df_sector.empty else df_sector["cod_sector"].max() + 1.0)
        nuevo_sector = pd.DataFrame({
            "cod_sector": nuevo_id_sector,
            "descripcion": sector_nombre,
            "estado": "A",
            "fecha_alta": datetime.now(),
            "fecha_baja": None,
            "fecha_ultima_modificacion": datetime.now(),
            "cod_dominio": None,
            "id_usuario": 1,
            "id_lugar": int(hospital_seleccionado),
            "id_area": None,
            "tipo_sector": int(t_sector_seleccionado)
        }, index=[1])


        if st.form_submit_button("Agregar Sector"):
            submit = st.form_submit_button("Agregar Sector")
            if submit:
        # if st.button("Agregar Sector"):
                if not sector_nombre:
                    return st.error("Debe ingresar un nombre para el sector.")
                elif not planta_seleccionada:
                    return st.error("Debe seleccionar al menos un local.")
                
                else:
        # Agregar al DataFrame en sesión
                    st.session_state.df_sector = pd.concat([st.session_state.df_sector, nuevo_sector], ignore_index=True)
                    st.session_state.df_local.loc[
                        st.session_state.df_local['id_local'].isin(sector_locales), 
                        'id_sector'] = nuevo_id_sector
                    # st.session_state.df_local['id_sector'] = st.session_state.df_local['id_sector'].astype('int64')
                    st.session_state["df_sector"].to_csv(".//db//sectores.csv",index=False)
                    st.session_state["df_local"].to_csv(".//db//locales.csv",index=False)                
                    st.session_state["creaSector"] = False
                    return st.success(f"Sector '{sector_nombre}' guardado correctamente.")
                    # st.experimental_rerun()
                    



def crear_sublocal():
    st.write("### Agregar nuevo Sublocal")

    with st.form("Agregar Sublocal"):
        st.markdown("#### Agregar Sublocal 🏢")
        st.markdown("En esta sección podrá agregar un sublocal al local seleccionado.")
        dotacion_map = {"Si": "S", "No": "N"}  # Diccionario para mapear valores
        nuevo_id_sublocal = 1 if df_sublocal.empty else df_sublocal["id_sublocal"].max() + 1
        nuevo_nombre_sublocal = st.text_input("Nombre del Sublocal", help="Ingrese el nombre del nuevo sublocal.")
        dotacion_val =  st.selectbox("Selecciona dotación:",
                        options=list(dotacion_map.keys())  # Mostramos "Si" y "No"
                        )
        
        if st.form_submit_button("Agregar Sublocal"):
            # df_sublocal = pd.concat([df_sublocal, nuevo_sublocal],axis=0)           # st.session_state["df_elemento"].append(nueva_fila, ignore_index=True)
            nuevo_sublocal = pd.DataFrame([{
            "id_sublocal": nuevo_id_sublocal,
            "descripcion": nuevo_nombre_sublocal,
            "descripcion_numerica" : 1,
            "estado" : 'A',
            "fecha_alta" : datetime.now(),
            "fecha_baja" : None,
            "fecha_ultima_modificacion" : datetime.now(),
            "id_local": local_seleccionado,
            "cod_dominio" : None,
            "id_usuario": 1,
            "dotacion" : dotacion_val,
            "id_sector" : sector_seleccionado
            
            # "id_establecimiento": hospital_seleccionado
            }])
            st.session_state.df_sublocal = pd.concat([st.session_state.df_sublocal, nuevo_sublocal], axis=0, ignore_index=True)
            st.success("Fila agregada exitosamente.")
            st.table(st.session_state.df_sublocal)
            st.session_state.df_sublocal.to_csv(".\\db\\sublocales.csv",index=False)
            st.experimental_rerun()
            st.success("Fila agregada exitosamente.")



# In[61]:


df_merged = df_joins()


# In[ ]:


# Interfaz de la app
st.title("Gestión de Sectores Sublocales y Camas")
st.write("### Selecciona un Efector")


# Selector de hospital

hospitales = df_efector[["id_establecimiento", "descripcion"]].drop_duplicates()
hospitales["id_establecimiento"] = hospitales["id_establecimiento"].fillna(0)
hospital_seleccionado = st.selectbox(
    "Selecciona un Efector:", 
    options=hospitales["id_establecimiento"].tolist(), 
    format_func=lambda x: hospitales[hospitales["id_establecimiento"] == x]["descripcion"].values[0]
)
# # st.write(hospital_seleccionado)

st.write("El efector cuenta con las siguientes dependencias")

st.write("### Selecciona un Edificio")
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

st.write("### Selecciona una Planta")
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

st.write("### Selecciona Sector")
sectores = df_merged[
    (df_merged["id_establecimiento"] == int(hospital_seleccionado)) &
    (df_merged["id_edificio"] == int(edificio_seleccionado)) &
    (df_merged["id_planta"] == int(planta_seleccionada))
    # (df_merged["cod_sector"] is not null)
        ][["cod_sector", "sector_det"]].drop_duplicates()
if sectores["cod_sector"].isnull().all():
    st.warning("No hay sectores disponibles para esta planta.")
    sector_seleccionado = None    
else: 
    sectores = sectores[~sectores["cod_sector"].isnull()].drop_duplicates()
    # st.table(sectores)
    sector_seleccionado = st.selectbox(
                "Selecciona un Sector:",
                options=sectores["cod_sector"].tolist(),
                format_func=lambda x: sectores[sectores["cod_sector"] == x]["sector_det"].values[0]
                )

# if st.button("Crear un nuevo Sector"):
#     # st.write("Sector seleccionado: ", sector_seleccionado)
#     st.write("Aqui deberíamos agregar otro sector")
#     st.session_state["creaSector"] = True
crear_sector()
    # st.session_state["creaSector"] = False
    # st.experimental_rerun()

st.write("### Selecciona Locales")
if sector_seleccionado is None:
    st.warning("Debe seleccionar un Sector primero.")
    local_seleccionado = None
else:
    locales = df_merged[
        (df_merged["id_establecimiento"] == hospital_seleccionado) & 
        (df_merged["id_edificio"] == edificio_seleccionado) &
        (df_merged["id_planta"] == planta_seleccionada) &
        (df_merged["cod_sector"] == sector_seleccionado)
    ][["id_local", "local_det"]].drop_duplicates()

    if locales["id_local"].isnull().all():
        st.warning("No hay locales disponibles para esta planta.")
        local_seleccionado = None
        st.write(locales)
    else:
        locales = locales.dropna(subset=["id_local"])
        #multiselect
        local_seleccionado = st.selectbox(
            "Selecciona los Locales:",
            options=locales["id_local"].tolist(),
            format_func=lambda x: locales[locales["id_local"] == x]["local_det"].values[0]
        )


st.write("### Selecciona Sublocal")

if st.session_state.df_sublocal["id_sublocal"].isnull().all():
    st.warning("No hay sublocales disponibles para este local.")
    sublocal_seleccionado = None

else:
    if local_seleccionado is None:
        st.warning("Debe seleccionar un Local primero.")
        sublocales = None
    else:
        sublocales = df_sublocal[
        (df_sublocal["id_sector"] == sector_seleccionado) &
        (df_sublocal["id_local"] == local_seleccionado)

        ][["id_sublocal", "descripcion"]].drop_duplicates()
        sublocales["id_sublocal"] = sublocales["id_sublocal"].fillna(0)

    # Manejar el caso de sectores vacíos
        if sublocales["id_sublocal"].isnull().all():
            st.warning("No hay sublocales disponibles para este local.")
            sublocal_seleccionado = None
        else:
            # if sublocales["id_sublocal"]:
            sublocal_seleccionado = st.selectbox(
                "Selecciona un Sublocal:",
                options=sublocales["id_sublocal"].tolist(),
                format_func=lambda x: sublocales[sublocales["id_sublocal"] == x]["descripcion"].values[0]
            )
            # if st.button("Crear un nuevo sublocal"):                
                # sublocal_det_carga = st.text_input("Nombre del Sublocal")

crear_sublocal()

    # Filtrar datos por hospital seleccionado

if (sublocales is None):
    st.warning("Debe seleccionar un sublocal.")
else:
    if (sublocales["id_sublocal"].isnull().all()):
        st.warning("Debe seleccionar un local primero.")
        elemento = None
    else:    
        datos_filtrados = df_merged[
            # [df_merged["id_establecimiento"] == hospital_seleccionado,
            # df_merged["cod_sector"] == sector_seleccionado]
                    (df_merged["id_establecimiento"] == hospital_seleccionado) &
                    (df_merged["cod_sector"] == sector_seleccionado) &
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

    crear_elemento()
css="""
<style>
    [data-testid="stForm"] {
        background: LightBlue;
    }
</style>
"""
st.write(css, unsafe_allow_html=True)
