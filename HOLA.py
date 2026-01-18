import streamlit as st
from groq import Groq
from datetime import datetime

st.set_page_config(page_title="MangiAI", page_icon="🤖")

st.markdown(
    """
    <style>
    .logo-fixed {
        position: fixed;
        top: 18px;
        right: 18px;
        width: 90px;
        opacity: 0.9;
        z-index: 1000;
    }
    </style>

    <img src="logomangi.png" class="logo-fixed">
    """,
    unsafe_allow_html=True
)

st.title("🤖 ¡Bienvenido a MangiAI!")
st.caption("Tu asistente, a otro nivel. Siempre.")

MODELOS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b"
]

def obtener_contexto_actual():
    ahora = datetime.now()
    fecha = ahora.strftime("%d/%m/%Y")
    hora = ahora.strftime("%H:%M")

    return (
        f"Fecha actual: {fecha}. "
        f"Hora actual: {hora}. "
        "Respondé teniendo en cuenta que esta información es actual."
    )

SYSTEM_PROMPT_BASE = (
    "Sos MangiAI, una IA moderna, clara y profesional. "
    "Recordás todo el contexto de la conversación. "
    "Respondés de forma ordenada y útil. "
    "Si el usuario pide código, explicás paso a paso. "
    "Si pide ideas, sos creativo pero realista."
)

def configurar_pagina():
    st.sidebar.title("⚙️ Configuración")
    modelo = st.sidebar.selectbox("Elegí un modelo:", MODELOS)

    if st.sidebar.button("🧹 Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()

    return modelo

def crear_cliente_groq():
    return Groq(api_key=st.secrets["CLAVE_API"])

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({
        "role": rol,
        "content": contenido,
        "avatar": avatar
    })

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def generar_respuesta(cliente, modelo):
    contexto_actual = obtener_contexto_actual()

    system_prompt = {
        "role": "system",
        "content": SYSTEM_PROMPT_BASE + " " + contexto_actual
    }

    mensajes = [system_prompt] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.mensajes
    ]

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream=False
    )

    return respuesta.choices[0].message.content

inicializar_estado()
cliente = crear_cliente_groq()
modelo = configurar_pagina()

mostrar_historial()

mensaje_usuario = st.chat_input("Escribe tu mensaje...")

if mensaje_usuario:
    actualizar_historial("user", mensaje_usuario, "🤔")

    with st.spinner("MangiAI está pensando..."):
        respuesta = generar_respuesta(cliente, modelo)

    actualizar_historial("assistant", respuesta, "logomangi.png")
    st.rerun()


