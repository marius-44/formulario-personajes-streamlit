import streamlit as st
import pandas as pd
import datetime
import os
from functools import reduce

FILE_PATH = "datos_personajes.xlsx"

# --- Inicializar Excel con hojas ---
def initialize_excel():
    if not os.path.exists(FILE_PATH):
        with pd.ExcelWriter(FILE_PATH) as writer:
            
            pd.DataFrame(columns=["ID", "Nombre", "Apodo", "Edad", "Sexo",
                "Altura", "Peso", "Color de cabello", "Color de ojos", "Complexión",
                "Ocupación", "Lugar de nacimiento", "Fecha de nacimiento", "Foto"]).to_excel(writer, sheet_name="Básico", index=False)
            
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

# --- Obtener el próximo ID ---
def get_next_id(df):
    if df.empty:
        return 1
    else:
        return int(df["ID"].max()) + 1

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
# CREAR NUEVO ID
# -------------------------------
st.header("Crear nuevo personaje")
if st.button("Generar nuevo ID"):
    new_id = get_next_id(datos_basico)
    new_row = {"ID": new_id, "Nombre": "", "Apodo": "", "Edad": "", "Sexo": "",
               "Altura": "", "Peso": "", "Color de cabello": "", "Color de ojos": "",
               "Complexión": "", "Ocupación": "", "Lugar de nacimiento": "",
               "Fecha de nacimiento": ""}
    datos_basico = pd.concat([datos_basico, pd.DataFrame([new_row])], ignore_index=True)
    all_sheets["Básico"] = datos_basico
    save_all_sheets(all_sheets)
    st.success(f"¡Nuevo personaje creado con ID {new_id}!")
    st.rerun()

# -------------------------------
# SECCIÓN 1: Datos Básicos
# -------------------------------
st.header("Sección 1: Datos Básicos")
with st.form("form1"):
    if not datos_basico.empty:
        selected_id = st.selectbox("Selecciona el ID", datos_basico["ID"].tolist())
    else:
        selected_id = None

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
    ocupacion = st.text_input("Ocupación").title()
    fecha_nac = st.date_input("Fecha de nacimiento", min_value=min_date, max_value=max_date)
    lugar_nac = st.text_input("Lugar de nacimiento").title()

    # Subir foto
    foto = st.file_uploader("Subir foto del personaje", type=["png", "jpg", "jpeg"])

    dia_nac = fecha_nac.day
    mes_nac = fecha_nac.month
    anio_nac = fecha_nac.year

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
             "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    fecha_text = (f"{dia_nac} de {meses[mes_nac-1]} del {anio_nac}")

    submitted1 = st.form_submit_button("Guardar sección 1")
    if submitted1 and selected_id:
        # Crear carpeta de imágenes si no existe
        if not os.path.exists("images"):
            os.makedirs("images")

        foto_path = None
        if foto is not None:
            ext = os.path.splitext(foto.name)[1]
            foto_path = (f"images/{selected_id}{ext}")
            with open(foto_path, "wb") as f:
                f.write(foto.getbuffer())

        # Guardar datos
        datos_basico.loc[datos_basico["ID"] == selected_id,
                         ["Nombre", "Apodo", "Edad", "Sexo", "Altura", "Peso",
                          "Color de cabello", "Color de ojos", "Complexión",
                          "Ocupación", "Lugar de nacimiento", "Fecha de nacimiento", "Foto"]] = \
        [nombre, apodo, edad, sexo, altura, peso, color_cabello, color_ojos,
         complexion, ocupacion, lugar_nac, fecha_text, foto_path]

        all_sheets["Básico"] = datos_basico
        save_all_sheets(all_sheets)
        st.success(f"Datos básicos guardados para ID {selected_id}")
        st.rerun()

# Mostrar imagen si ya existe
if selected_id:
    personaje = datos_basico[datos_basico["ID"] == selected_id]
    if not personaje["Foto"].isnull().values[0]:
        st.image(personaje["Foto"].values[0], caption="Foto del personaje", width=200)

# -------------------------------
# SECCIÓN 2: Personalidad
# -------------------------------
st.header("Sección 2: Personalidad")
with st.form("form2"):
    if not datos_basico.empty:
        selected_id = st.selectbox("Selecciona el ID", datos_basico["ID"].tolist(), key="perso_id")
    else:
        selected_id = None

    frase = st.text_area("Frase típica del personaje").lower()
    rasgo_1 = st.text_input("Rasgo 1").lower()
    rasgo_2 = st.text_input("Rasgo 2").lower()
    rasgo_3 = st.text_input("Rasgo 3").lower()
    rasgo_4 = st.text_input("Rasgo 4").lower()

    submitted2 = st.form_submit_button("Guardar sección 2")
    if submitted2 and selected_id:
        datos_personalidad = datos_personalidad[datos_personalidad["ID"] != selected_id]
        new_row = {"ID": selected_id, "Frase": frase, "Rasgo 1": rasgo_1, "Rasgo 2": rasgo_2, "Rasgo 3": rasgo_3, "Rasgo 4": rasgo_4}
        datos_personalidad = pd.concat([datos_personalidad, pd.DataFrame([new_row])], ignore_index=True)
        all_sheets["Personalidad"] = datos_personalidad
        save_all_sheets(all_sheets)
        st.success(f"Datos de personalidad guardados para ID {selected_id}")
        st.rerun()

# -------------------------------
# SECCIÓN 3: Rol
# -------------------------------
st.header("Sección 3: Rol en la Historia")
with st.form("form3"):
    if not datos_basico.empty:
        selected_id = st.selectbox("Selecciona el ID", datos_basico["ID"].tolist(), key="rol_id")
    else:
        selected_id = None

    rol = st.selectbox("Rol en la historia", ["", "Protagonista", "Ayudante de protagonista", "Escudero",
        "Deuteragonista", "Guardián", "Mentor", "Personaje de impacto",
        "Antagonista", "Ayudante de antagonista", "Escéptico", "Obstáculo", "Meta"])
    infancia = st.text_area("Momento clave en la infancia").lower()
    quiere = st.text_area("¿Qué es lo que quiere?").lower()
    necesita = st.text_area("¿Qué es lo que realmente necesita?").lower()

    submitted3 = st.form_submit_button("Guardar sección 3")
    if submitted3 and selected_id:
        datos_rol = datos_rol[datos_rol["ID"] != selected_id]
        new_row = {"ID": selected_id, "Rol en historia": rol,
                   "Momento de la infancia":infancia, "¿Qué quiere?":quiere, "¿Qué necesita?":necesita}
        datos_rol = pd.concat([datos_rol, pd.DataFrame([new_row])], ignore_index=True)
        all_sheets["Rol"] = datos_rol
        save_all_sheets(all_sheets)
        st.success(f"Rol guardado para ID {selected_id}")
        st.rerun()

# -------------------------------
# SECCIÓN 4: Notas
# -------------------------------
st.header("Sección 4: Notas adicionales")
with st.form("form4"):
    if not datos_basico.empty:
        selected_id = st.selectbox("Selecciona el ID", datos_basico["ID"].tolist(), key="notas_id")
    else:
        selected_id = None

    notas = st.text_area("Notas adicionales sobre el personaje")

    submitted4 = st.form_submit_button("Guardar sección 4")
    if submitted4 and selected_id:
        datos_notas = datos_notas[datos_notas["ID"] != selected_id]
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
# MERGE DINÁMICO Y EDICIÓN GLOBAL (SIN COLUMNA FOTO)
# -------------------------------
dfs = list(all_sheets.values())
if dfs and not dfs[0].empty:
    # Hacemos el merge de todas las hojas
    merged_df = reduce(lambda left, right: pd.merge(left, right, on="ID", how="left"), dfs)

    # Excluimos la columna Foto si existe
    if "Foto" in merged_df.columns:
        merged_df = merged_df.drop(columns=["Foto"])

    st.subheader("Vista global de TODOS los datos (editable)")
    edited_df = st.data_editor(
        merged_df,
        use_container_width=True,
        num_rows="dynamic",
        key="global_editor",
        disabled=["ID"]  # ID no editable
    )

    if st.button("Guardar cambios globales"):
        # Restauramos la columna Foto en el proceso de guardado (manteniendo valores originales)
        if "Foto" in all_sheets["Básico"].columns:
            merged_df = pd.merge(edited_df, all_sheets["Básico"][["ID", "Foto"]], on="ID", how="left")

        # Reconstruimos las hojas originales
        new_data = {}
        for sheet_name, original_df in all_sheets.items():
            sheet_cols = original_df.columns.tolist()
            new_data[sheet_name] = merged_df[sheet_cols] if all(col in merged_df.columns for col in sheet_cols) else original_df

        save_all_sheets(new_data)
        st.success("¡Cambios guardados en todas las hojas!")
        st.rerun()
else:
    st.info("No hay datos aún para mostrar.")
