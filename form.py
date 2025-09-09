import streamlit as st
import pandas as pd
import datetime
import os
import uuid
from functools import reduce

FILE_PATH = "datos_personajes.xlsx"

# --- Inicializar Excel con hojas ---
def initialize_excel():
    if not os.path.exists(FILE_PATH):
        with pd.ExcelWriter(FILE_PATH) as writer:
            pd.DataFrame(columns=["ID", "Nombre", "Apodo", "Edad", "Sexo",
                "Altura", "Peso", "Color de cabello", "Color de ojos", "Complexión",
                "Ocupación", "Lugar de nacimiento", "Fecha de nacimiento"]).to_excel(writer, sheet_name="Básico", index=False)
            
            pd.DataFrame(columns=["ID", 
                "Frase", "Rasgo 1", "Rasgo 2", "Rasgo 3", "Rasgo 4"]).to_excel(writer, sheet_name="Personalidad", index=False)

            pd.DataFrame(columns=["ID", "Rol en historia", "Momento de la infancia",
                "¿Qué quiere?", "¿Qué necesita?"]).to_excel(writer, sheet_name="Rol", index=False)
            
            pd.DataFrame(columns=["ID", "Notas adicionales"]).to_excel(writer, sheet_name="Notas", index=False)

# --- Cargar todas las hojas ---
def load_all_sheets():
    xls = pd.ExcelFile(FILE_PATH)
    data = {sheet: pd.read_excel(FILE_PATH, sheet_name=sheet) for sheet in xls.sheet_names}
    return data

# --- Guardar todas las hojas ---
def save_all_sheets(dataframes: dict):
    with pd.ExcelWriter(FILE_PATH) as writer:
        for sheet, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet, index=False)

# --- App ---
st.title("Formulario para la creación de personajes")

# Inicializar archivo y cargar datos
initialize_excel()
all_sheets = load_all_sheets()

datos_basico = all_sheets["Básico"]
datos_personalidad = all_sheets["Personalidad"]
datos_rol = all_sheets["Rol"]
datos_notas = all_sheets["Notas"]

# -------------------------------
# FORMULARIO SECCIÓN 1: Datos Básicos
# -------------------------------
st.header("Sección 1: Datos Básicos")
with st.form("form1"):

    min_date = datetime.date(1900, 1, 1)
    max_date = datetime.date(2050, 12, 31)

    nombre = st.text_input("Nombre").title()
    apodo = st.text_input("Apodo").capitalize()
    edad = st.slider("Edad", min_value=0, max_value=120, value=25, step=1)
    sexo = st.selectbox("Sexo", ["Femenino", "Masculino"])
    altura = st.slider("Altura", min_value=1.20, max_value=2.20, value=1.70, step=0.01)
    peso = st.slider("Peso", min_value=30, max_value=150, value=60, step=1)
    color_cabello = st.selectbox("Color de cabello", ["Negro", "Castaño oscuro", "Castaño", "Castaño claro",
        "Rubio", "Plateado", "Pelirrojo", "Canoso", "Pintado/Decolorado"]).lower()
    color_ojos = st.selectbox("Color de ojos", ["Negro", "Café oscuro", "Café", "Amielado",
        "Avellana", "Verde", "Azul", "Gris", "Violeta"]).lower()
    complexion = st.text_input("Complexión").lower()
    ocupacion = st.text_input("Ocupación").capitalize()
    fecha_nac = st.date_input("Fecha de nacimiento", min_value=min_date, max_value=max_date)
    lugar_nac = st.text_input("Lugar de nacimiento").title()

    dia_nac = fecha_nac.day
    mes_nac = fecha_nac.month
    anio_nac = fecha_nac.year

    mes_texto = ""
    match mes_nac:
        case 1:
            mes_texto = "Enero"
        case 2:
            mes_texto = "Febrero"
        case 3:
            mes_texto = "Marzo"
        case 4:
            mes_texto = "Abril"
        case 5:
            mes_texto = "Mayo"
        case 6:
            mes_texto = "Junio"
        case 7:
            mes_texto = "Julio"
        case 8:
            mes_texto = "Agosto"
        case 9:
            mes_texto = "Septiembre"
        case 10:
            mes_texto = "Octubre"
        case 11:
            mes_texto = "Noviembre"
        case 12:
            mes_texto = "Diciembre"
    
    fecha_text = (f"{dia_nac} de {mes_texto} del {anio_nac}")

    submitted1 = st.form_submit_button("Guardar sección 1")
    if submitted1:
        new_id = str(uuid.uuid4())
        new_row = {"ID": new_id, "Nombre": nombre, "Apodo":apodo, "Edad": edad, "Sexo":sexo,
                   "Altura":altura, "Peso":peso, "Color de cabello":color_cabello, "Color de ojos":color_ojos, "Complexión":complexion,
                   "Ocupación":ocupacion, "Lugar de nacimiento":lugar_nac,
                   # "Fecha de nacimiento":fecha_nac}
                   "Fecha de nacimiento":fecha_text}
        datos_basico = pd.concat([datos_basico, pd.DataFrame([new_row])], ignore_index=True)
        all_sheets["Básico"] = datos_basico
        save_all_sheets(all_sheets)
        st.success(f"Datos básicos guardados con ID {new_id}")
        st.rerun()

# -------------------------------
# FORMULARIO SECCIÓN 2: Personalidad
# -------------------------------
st.header("Sección 2: Datos de Personalidad")
with st.form("form2"):
    selected_id = st.selectbox("Selecciona el ID para asociar", datos_basico["ID"].tolist())
    frase = st.text_area("Frase típica del personaje").lower()
    rasgo_1 = st.text_input("Rasgo 1").lower()
    rasgo_2 = st.text_input("Rasgo 2").lower()
    rasgo_3 = st.text_input("Rasgo 3").lower()
    rasgo_4 = st.text_input("Rasgo 4").lower()

    submitted2 = st.form_submit_button("Guardar sección 2")
    if submitted2:
        new_row = {"ID": selected_id, "Frase": frase, "Rasgo 1": rasgo_1, "Rasgo 2": rasgo_2, "Rasgo 3": rasgo_3, "Rasgo 4": rasgo_4}
        datos_personalidad = pd.concat([datos_personalidad, pd.DataFrame([new_row])], ignore_index=True)
        all_sheets["Personalidad"] = datos_personalidad
        save_all_sheets(all_sheets)
        st.success(f"Datos de personalidad guardados para ID {selected_id}")
        st.rerun()

# -------------------------------
# FORMULARIO SECCIÓN 3: Rol
# -------------------------------
st.header("Sección 3: Rol en la Historia")
with st.form("form3"):
    selected_id = st.selectbox("Selecciona el ID para asociar", datos_basico["ID"].tolist())
    rol = st.selectbox("Rol en la historia", ["Protagonista", "Ayudante de protagonista", "Escudero",
        "Deuteragonista", "Guardián", "Mentor", "Personaje de impacto",
        "Antagonista", "Ayudante de antagonista", "Escéptico", "Obstáculo", "Meta"])
    infancia = st.text_area("Momento clave en la infancia").lower()
    quiere = st.text_area("¿Qué es lo que quiere?").lower()
    necesita = st.text_area("¿Qué es lo que realmente necesita?").lower()

    submitted3 = st.form_submit_button("Guardar sección 3")
    if submitted3:
        new_row = {"ID": selected_id, "Rol en historia": rol,
                   "Momento de la infancia":infancia, "¿Qué quiere?":quiere, "¿Qué necesita?":necesita}
        datos_rol = pd.concat([datos_rol, pd.DataFrame([new_row])], ignore_index=True)
        all_sheets["Rol"] = datos_rol
        save_all_sheets(all_sheets)
        st.success(f"Datos del rol guardados para ID {selected_id}")
        st.rerun()

# -------------------------------
# FORMULARIO SECCIÓN 4: Notas
# -------------------------------
st.header("Sección 4: Notas adicionales")
with st.form("form4"):
    selected_id = st.selectbox("Selecciona el ID para asociar", datos_basico["ID"].tolist())
    notas = st.text_area("Notas adicionales sobre el personaje")

    submitted4 = st.form_submit_button("Guardar sección 4")
    if submitted4:
        new_row = {"ID":selected_id, "Notas adicionales":notas}
        datos_notas = pd.concat([datos_notas, pd.DataFrame([new_row])], ignore_index=True)
        all_sheets["Notas"] = datos_notas
        save_all_sheets(all_sheets)
        st.success(f"Notas guardadas para ID {selected_id}")
        st.rerun()

# -------------------------------
# ELIMINAR REGISTROS COMPLETOS
# -------------------------------
st.header("Eliminar un personaje")
if not datos_basico.empty:
    delete_id = st.selectbox("Selecciona el ID a eliminar", datos_basico["ID"].tolist())
    if st.button("Eliminar registro completo"):
        for sheet_name, df in all_sheets.items():
            all_sheets[sheet_name] = df[df["ID"] != delete_id]
        save_all_sheets(all_sheets)
        st.success(f"Registro con ID {delete_id} eliminado de todas las hojas")
        st.rerun()
else:
    st.info("No hay registros para eliminar.")

# -------------------------------
# MERGE DINÁMICO Y EDICIÓN GLOBAL
# -------------------------------
dfs = list(all_sheets.values())
if dfs and not dfs[0].empty:
    merged_df = reduce(lambda left, right: pd.merge(left, right, on="ID", how="left"), dfs)

    st.subheader("Vista global de TODOS los datos (editable)")
    edited_df = st.data_editor(
        merged_df,
        use_container_width=True,
        num_rows="dynamic",
        key="global_editor",
        disabled=["ID"]
    )

    if st.button("Guardar cambios globales"):
        edited_df["ID"] = edited_df["ID"].fillna("").apply(lambda x: str(uuid.uuid4()) if x == "" else x)

        new_data = {}
        for sheet_name, original_df in all_sheets.items():
            sheet_cols = original_df.columns.tolist()
            new_data[sheet_name] = edited_df[sheet_cols]

        save_all_sheets(new_data)
        st.success("¡Cambios guardados en todas las hojas!")
        st.rerun()
else:
    st.info("No hay datos aún para mostrar.")
