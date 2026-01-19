import streamlit as st
from groq import Groq
from datetime import datetime
import base64
import uuid
import html   # 🔒 FIX DEFINITIVO

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

    /* -------- SIDEBAR BUTTONS -------- */
    div[data-testid="stSidebar"] button {{
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(0,255,170,0.25);
        color: #eaeaea;
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 8px;
        transition: all 0.15s ease;
        text-align: left;
    }}

    div[data-testid="stSidebar"] button:hover {{
        background: rgba(0,255,170,0.15);
        transform: translateY(-1px);
    }}

    /* -------- EMPTY STATE -------- */
    .empty-state {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 55vh;
        text-align: center;
        opacity: 0.9;
    }}

    .empty-title {{
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }}

    .empty-subtitle {{
        font-size: 1.05rem;
        opacity: 0.7;
    }}

    /* -------- CHAT -------- */
    .chat-wrapper {{
        position: relative;
        padding: 14px;
        padding-top: 38px;
        border-radius: 12px;
        margin-bottom: 12px;
    }}

    .chat-header {{
        position: absolute;
        top: 6px;
        left: 8px;
        right: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .style-badge {{
        font-size: 0.9rem;
        opacity: 0.85;
    }}

    .copy-btn {{
        font-size: 0.75rem;
        background: rgba(255,255,255,0.08);
        border: none;
        border-radius: 6px;
        padding: 4px 6px;
        cursor: pointer;
        opacity: 0.7;
    }}

    .copy-btn:hover {{
        opacity: 1;
        background: rgba(0,255,170,0.2);
    }}

    /* -------- FIX DEFINITIVO TEXTO -------- */
    .chat-message {{
        max-width: 100%;
        white-space: pre-wrap;
        word-wrap: break-word;
        overflow-wrap: break-word;
        line-height: 1.6;
        font-size: 1rem;
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
    "⚡ Directo": "⚡",
    "📖 Explicativo": "📖",
    "🎯 Estratégico": "🎯",
    "🧑‍💼 Formal": "🧑‍💼",
    "💻 Código": "💻"
}

# -------------------- CONTEXTO --------------------
def obtener_contexto_actual():
    ahora = datetime.now()
    return f"Fecha: {ahora.strftime('%d/%m/%Y')} | Hora: {ahora.strftime('%H:%M')}"

def construir_system_prompt():
    estilo = st.session_state.get("estilo_respuesta", "⚡ Directo")
    return (
        "Sos MangiAI, una IA moderna y profesional creada por Dante Mangiafico. "
        "Recordás el contexto de la conversación. "
        f"{ESTILOS[estilo]} "
        + obtener_contexto_actual()
    )

# -------------------- SIDEBAR --------------------
def configurar_pagina():
    st.sidebar.title("⚙️ Configuración")

    modelo = st.sidebar.selectbox("Elige un modelo:", MODELOS)

    st.sidebar.markdown("### 💬 Estilo de respuesta")

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

def actualizar_historial(rol, contenido, avatar, estilo=None):
    st.session_state.mensajes.append({
        "id": str(uuid.uuid4()),
        "role": rol,
        "content": contenido,
        "avatar": avatar,
        "estilo": estilo
    })

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        if mensaje["role"] == "assistant":
            emoji = AVATARES.get(mensaje["estilo"], "🤖")
            texto_seguro = html.escape(mensaje["content"])

            st.markdown(f"""
            <div class="chat-wrapper">
                <div class="chat-header">
                    <div class="style-badge">{emoji}</div>
                    <button class="copy-btn"
                        onclick="navigator.clipboard.writeText(this.dataset.text)">
                        📋
                    </button>
                </div>
                <div class="chat-message" data-text="{texto_seguro}">
                    {texto_seguro}
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            with st.chat_message("user", avatar=mensaje["avatar"]):
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

if len(st.session_state.mensajes) == 0:
    st.markdown("""
        <div class="empty-state">
            <div class="empty-title">¿En qué te ayudo hoy?</div>
            <div class="empty-subtitle">Elegí un estilo o escribí tu consulta</div>
        </div>
    """, unsafe_allow_html=True)
else:
    mostrar_historial()

mensaje_usuario = st.chat_input("Escribe tu mensaje...")

if mensaje_usuario:
    actualizar_historial("user", mensaje_usuario, "🤔")

    with st.spinner("Analizando..."):
        respuesta = generar_respuesta(cliente, modelo)

    estilo_actual = st.session_state.estilo_respuesta
    avatar = AVATARES.get(estilo_actual, "🤖")

    actualizar_historial(
        "assistant",
        respuesta,
        avatar,
        estilo=estilo_actual
    )

    st.rerun()
