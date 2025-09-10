import streamlit as st

def main():
    st.title("Curso de Streamlit (H1)")
    st.header("Esto es un encabezado (H2)")
    st.subheader("Esto es un sub-encabezado (H3)")
    st.text("Esto es un texto")
    nombre = "Motumbo"
    st.text(f"¡Hola {nombre}! Esto es otro texto")
    st.markdown("### Esto es un markdown H3")

    st.success("El programa se ejecutó correctamente")
    st.warning("Aviso: esto podría salir mal")
    st.info("Pare cerrar el puerto en terminal, ejecutar Ctrl + C")
    st.error("Error: no se ha podido ejecutar el programa")
    st.exception("Esto es una excepción") # type: ignore

if __name__=="__main__":
    main()
