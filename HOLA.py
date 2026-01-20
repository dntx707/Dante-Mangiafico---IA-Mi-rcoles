import streamlit as st
from groq import Groq
from datetime import datetime
import base64
import uuid
import html

# -------------------- CONFIG PÁGINA --------------------
st.set_page_config(
    page_title="MangiAI",
    page_icon="logopersonaje.png",
    layout="centered"
)

# -------------------- LOGOS --------------------
def cargar_logo_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = cargar_logo_base64("logomangi.png")
logo_personaje_base64 = cargar_logo_base64("logopersonaje.png")

st.markdown(
    f"""
    <!-- GOOGLE FONT : EXO 2 -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
    html, body, [class*="st-"], div, span, p, h1, h2, h3, h4, h5, h6,
    button, input, textarea {{
        font-family: 'Exo 2', -apple-system, BlinkMacSystemFont,
                     'Segoe UI', sans-serif !important;
    }}

    h1 {{
        font-weight: 900 !important;
        margin: 0;
    }}

    /* -------- SIDEBAR ARROW -------- */
    button[data-testid="collapsedControl"],
    button[data-testid="stSidebarCollapseButton"] {{
        position: fixed !important;
        top: 14px !important;
        left: 14px !important;
        z-index: 9999 !important;
        background: rgba(0, 255, 170, 0.15) !important;
        border-radius: 10px !important;
        padding: 8px 10px !important;
        border: 1px solid rgba(0, 255, 170, 0.4) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3) !important;
    }}

    button[data-testid="collapsedControl"] svg,
    button[data-testid="stSidebarCollapseButton"] svg {{
        color: #00ffaa !important;
        width: 1.2rem !important;
        height: 1.2rem !important;
    }}

    /* -------- LOGO FIXED (TOP RIGHT) -------- */
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

    /* -------- HEADER -------- */
    .header-logo {{
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 4px;
    }}

    .header-logo img {{
        width: 72px;
        height: 72px;
    }}

    .header-logo h1 {{
        font-size: 2.4rem;
        line-height: 1.1;
    }}

    /* -------- EMPTY STATE -------- */
    .empty-state {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 55vh;
        text-align: center;
        opacity: 0.95;
    }}

    .empty-title {{
        font-size: 2.35rem;
        font-weight: 800;
    }}

    .empty-subtitle {{
        font-size: 1.05rem;
        opacity: 0.75;
    }}
    </style>

    <img src="data:image/png;base64,{logo_base64}" class="logo-fixed">
    """,
    unsafe_allow_html=True
)

# -------------------- HEADER --------------------
st.markdown(
    f"""
    <div class="header-logo">
        <img src="data:image/png;base64,{logo_personaje_base64}">
        <h1>¡Bienvenido a MangiAI!</h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.caption("Tu asistente inteligente, elevado al siguiente nivel. Siempre.")

# -------------------- MODELOS --------------------
MODELOS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b"
]

# -------------------- ESTILOS --------------------
ESTILOS = {
    "⚡ Directo": "Respondé de forma breve, clara y sin rodeos.",
    "📖 Explicativo": "Respondé paso a paso, con contexto y ejemplos claros.",
    "🎯 Estratégico": "Respondé analizando opciones, pros y contras, y recomendando.",
    "🧑‍💼 Formal": "Respondé con tono profesional, estructurado y neutral.",
    "💻 Código": (
        "Respondé como un programador senior. "
        "Priorizá código limpio y optimizado. "
        "Usá bloques de código correctamente. "
        "No expliques salvo que el usuario lo pida."
    )
}

AVATARES = {
    "⚡ Directo": ("⚡", "Directo"),
    "📖 Explicativo": ("📖", "Explicativo"),
    "🎯 Estratégico": ("🎯", "Estratégico"),
    "🧑‍💼 Formal": ("🧑‍💼", "Formal"),
    "💻 Código": ("💻", "Código")
}

# -------------------- CONTEXTO --------------------
def obtener_contexto_actual():
    ahora = datetime.now()
    return f"{ahora.strftime('%d/%m/%Y %H:%M')}"

def construir_system_prompt():
    estilo = st.session_state.get("estilo_respuesta", "⚡ Directo")
    return (
        "MangiAI, una IA moderna y profesional creada por Dante Mangiafico. "
        f"{ESTILOS[estilo]} "
        + obtener_contexto_actual()
    )

# -------------------- SIDEBAR --------------------
def configurar_pagina():
    st.sidebar.title("⚙️ Configuración")
    modelo = st.sidebar.selectbox("Modelo:", MODELOS)

    st.sidebar.markdown("### 💬 Estilo de respuesta")

    if "estilo_respuesta" not in st.session_state:
        st.session_state.estilo_respuesta = "⚡ Directo"

    for estilo in ESTILOS:
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

def actualizar_historial(rol, contenido, avatar, estilo=None):
    st.session_state.mensajes.append({
        "id": str(uuid.uuid4()),
        "role": rol,
        "content": contenido,
        "avatar": avatar,
        "estilo": estilo
    })

# -------------------- APP --------------------
inicializar_estado()
cliente = crear_cliente_groq()
modelo = configurar_pagina()

if not st.session_state.mensajes:
    st.markdown("""
        <div class="empty-state">
            <div class="empty-title">¿En qué te ayudo hoy?</div>
            <div class="empty-subtitle">Elegí un estilo o escribí tu consulta</div>
        </div>
    """, unsafe_allow_html=True)

mensaje_usuario = st.chat_input("Escribí tu mensaje...")

if mensaje_usuario:
    actualizar_historial("user", mensaje_usuario, "🤔")
    with st.spinner("Analizando..."):
        respuesta = generar_respuesta(cliente, modelo)

    estilo_actual = st.session_state.estilo_respuesta
    avatar = AVATARES.get(estilo_actual, ("🤖", ""))[0]

    actualizar_historial("assistant", respuesta, avatar, estilo=estilo_actual)
    st.rerun()
