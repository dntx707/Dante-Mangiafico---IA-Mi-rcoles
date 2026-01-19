import streamlit as st
from groq import Groq
from datetime import datetime
import base64

# -------------------- CONFIG PÁGINA --------------------
st.set_page_config(
    page_title="MangiAI",
    page_icon="🤖",
    layout="centered"
)

# -------------------- LOGO FIXED --------------------
def cargar_logo_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = cargar_logo_base64("logomangi.png")

st.markdown(
    f"""
    <style>
    .logo-fixed {{
        position: fixed;
        top: 16px;
        right: 16px;
        width: 130px;
        opacity: 0.95;
        z-index: 999;
        pointer-events: none;
        filter: drop-shadow(0 6px 18px rgba(0,0,0,0.35));
    }}

    @media (max-width: 768px) {{
        .logo-fixed {{
            width: 95px;
            top: 12px;
            right: 12px;
        }}
    }}

    /* -------- BOTONES ESTILO RESPUESTA -------- */
    div[data-testid="stSidebar"] button {{
        background: transparent;
        border: 1px solid rgba(0, 255, 170, 0.25);
        color: #eaeaea;
        border-radius: 10px;
        padding: 10px 12px;
        margin-bottom: 8px;
        transition: all 0.15s ease;
        text-align: left;
    }}

    div[data-testid="stSidebar"] button:hover {{
        background: rgba(0, 255, 170, 0.15);
        color: #ffffff;
        transform: translateY(-1px);
    }}

    div[data-testid="stSidebar"] button:focus {{
        background: #00ffaa;
        color: #002b24;
        font-weight: 600;
    }}
    </style>

    <img src="data:image/png;base64,{logo_base64}" class="logo-fixed">
    """,
    unsafe_allow_html=True
)

# -------------------- HEADER --------------------
st.title("🤖 ¡Bienvenido a MangiAI!")
st.caption("Tu asistente, a otro nivel. Siempre.")

# -------------------- MODELOS --------------------
MODELOS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b"
]

# -------------------- ESTILOS RESPUESTA --------------------
ESTILOS = {
    "⚡ Directo": "Respondé de forma breve, clara y sin rodeos.",
    "📖 Explicativo": "Respondé paso a paso, con contexto y ejemplos claros.",
    "🎯 Estratégico": "Respondé analizando opciones, pros y contras, y recomendando.",
    "🧑‍💼 Formal": "Respondé con tono profesional, estructurado y neutral."
}

AVATARES = {
    "⚡ Directo": "⚡",
    "📖 Explicativo": "📖",
    "🎯 Estratégico": "🎯",
    "🧑‍💼 Formal": "🧑‍💼"
}

# -------------------- CONTEXTO --------------------
def obtener_contexto_actual():
    ahora = datetime.now()
    return (
        f"Fecha actual: {ahora.strftime('%d/%m/%Y')}. "
        f"Hora actual: {ahora.strftime('%H:%M')}."
    )

def construir_system_prompt():
    estilo = st.session_state.get("estilo_respuesta", "⚡ Directo")
    return (
        "MangiAI, una IA moderna, clara y profesional. "
        "Recordás el contexto de la conversación. "
        f"{ESTILOS[estilo]} "
        + obtener_contexto_actual()
    )

# -------------------- SIDEBAR --------------------
def configurar_pagina():
    st.sidebar.title("⚙️ Configuración")

    modelo = st.sidebar.selectbox("Elige un modelo:", MODELOS)

    st.sidebar.markdown("### 🎛️ Estilo de respuesta")

    if "estilo_respuesta" not in st.session_state:
        st.session_state.estilo_respuesta = "⚡ Directo"

    for estilo in ESTILOS.keys():
        if st.sidebar.button(estilo, use_container_width=True):
            st.session_state.estilo_respuesta = estilo

    if st.sidebar.button("🧹 Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()

    return modelo

# -------------------- GROQ CLIENT --------------------
def crear_cliente_groq():
    return Groq(api_key=st.secrets["CLAVE_API"])

# -------------------- ESTADO --------------------
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

# -------------------- RESPUESTA IA --------------------
def generar_respuesta(cliente, modelo):
    system_prompt = {
        "role": "system",
        "content": construir_system_prompt()
    }

    mensajes = [system_prompt] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.mensajes
    ]

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes
    )

    return respuesta.choices[0].message.content

# -------------------- APP --------------------
inicializar_estado()
cliente = crear_cliente_groq()
modelo = configurar_pagina()

mostrar_historial()

mensaje_usuario = st.chat_input("Escribe tu mensaje...")

if mensaje_usuario:
    actualizar_historial("user", mensaje_usuario, "🤔")

    with st.spinner("Analizando..."):
        respuesta = generar_respuesta(cliente, modelo)

    avatar = AVATARES.get(st.session_state.estilo_respuesta, "🤖")
    actualizar_historial("assistant", respuesta, avatar)

    st.rerun()

