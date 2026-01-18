import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi chat de IA", page_icon="🤖")
st.title("¡Bienvenido a MangiAI!")

MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']

def configurar_pagina():
    st.sidebar.title("Configuración de la IA")
    elegirModelo = st.sidebar.selectbox("Elegí un modelo:", options=MODELOS, index=0)
    return elegirModelo

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=False
    )
    return respuesta.choices[0].message.content

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedor = st.container()
    with contenedor:
        mostrar_historial()

inicializar_estado()
clienteUsuario = crear_usuario_groq()
modelo = configurar_pagina()

mensaje = st.chat_input("Escribí tu mensaje:")

if mensaje:
    actualizar_historial("user", mensaje, "😁")
    respuesta = configurar_modelo(clienteUsuario, modelo, mensaje)
    actualizar_historial("assistant", respuesta, "🤖")
    st.rerun()


area_chat()



