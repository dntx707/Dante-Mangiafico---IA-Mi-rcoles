import streamlit as st
from groq import Groq
from datetime import datetime
import base64
import uuid
import html

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
    <!-- GOOGLE FONT : EXO 2 -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
    /* -------- FONT GLOBAL -------- */
    html, body, [class*="st-"], div, span, p, h1, h2, h3, h4, h5, h6,
    button, input, textarea {{
        font-family: 'Exo 2', -apple-system, BlinkMacSystemFont,
                     'Segoe UI', sans-serif !important;
    }}

    /* -------- SIDEBAR COLLAPSE BUTTON FIX -------- */
    [data-testid="collapsedControl"] {{
        position: fixed !important;
        top: 0.5rem !important;
        left: 0.5rem !important;
        z-index: 999999 !important;
        background: rgba(0, 255, 170, 0.15) !important;
        border: 1px solid rgba(0, 255, 170, 0.4) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        transition: all 0.2s ease !important;
    }}

    [data-testid="collapsedControl"]:hover {{
        background: rgba(0, 255, 170, 0.3) !important;
        transform: scale(1.08) !important;
        border-color: rgba(0, 255, 170, 0.6) !important;
    }}

    [data-testid="collapsedControl"] svg {{
        color: #00ffaa !important;
        width: 1.2rem !important;
        height: 1.2rem !important;
    }}

    /* -------- LOGO -------- */
    .logo-fixed {{
        position: fixed;
        top: 16px;
        right: 16px;
        width: 130px;
        opacity: 0.95;
        z-index: 998;
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

    /* -------- SIDEBAR STYLING -------- */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, 
            rgba(0, 30, 30, 0.95) 0%, 
            rgba(0, 20, 20, 0.98) 100%);
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {{
        color: #00ffaa;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }}

    /* -------- SIDEBAR BUTTONS -------- */
    div[data-testid="stSidebar"] button {{
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(0,255,170,0.3) !important;
        color: #eaeaea !important;
        border-radius: 14px !important;
        padding: 11px 16px !important;
        margin-bottom: 8px !important;
        transition: all 0.15s ease !important;
        text-align: left !important;
        font-weight: 500 !important;
        width: 100% !important;
    }}

    div[data-testid="stSidebar"] button:hover {{
        background: rgba(0,255,170,0.18) !important;
        transform: translateY(-1px) !important;
        border-color: rgba(0,255,170,0.5) !important;
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
        letter-spacing: -0.01em;
        margin-bottom: 0.3rem;
        background: linear-gradient(135deg, #00ffaa 0%, #00cc88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .empty-subtitle {{
        font-size: 1.05rem;
        font-weight: 400;
        opacity: 0.75;
        color: #b0b0b0;
    }}

    /* -------- CHAT -------- */
    .chat-wrapper {{
        position: relative;
        padding: 16px;
        padding-top: 42px;
        border-radius: 14px;
        margin-bottom: 14px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(0,255,170,0.1);
        transition: all 0.2s ease;
    }}

    .chat-wrapper:hover {{
        background: rgba(255,255,255,0.04);
        border-color: rgba(0,255,170,0.2);
    }}

    .chat-header {{
        position: absolute;
        top: 8px;
        left: 12px;
        right: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .style-badge {{
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.95rem;
        font-weight: 600;
        opacity: 0.9;
        color: #00ffaa;
    }}

    .copy-btn {{
        font-size: 0.75rem;
        background: rgba(255,255,255,0.08);
        border: none;
        border-radius: 6px;
        padding: 4px 8px;
        cursor: pointer;
        opacity: 0.7;
        transition: all 0.2s ease;
    }}

    .copy-btn:hover {{
        opacity: 1;
        background: rgba(0,255,170,0.25);
    }}

    .chat-message {{
        max-width: 100%;
        white-space: pre-wrap;
        word-wrap: break-word;
        overflow-wrap: break-word;
        line-height: 1.7;
        font-size: 1.02rem;
        font-weight: 400;
        color: #e0e0e0;
    }}

    /* -------- CHAT INPUT -------- */
    .stChatInput {{
        border-color: rgba(0,255,170,0.3) !important;
    }}

    .stChatInput:focus-within {{
        border-color: rgba(0,255,170,0.6) !important;
        box-shadow: 0 0 0 1px rgba(0,255,170,0.3) !important;
    }}
    </style>

    <img src="data:image/png;base64,{logo_base64}" class="logo-fixed">
    """,
    unsafe_allow_html=True
)

# -------------------- HEADER --------------------
st.title("🤖 MangiAI")
st.caption("Tu asistente inteligente, elevado al siguiente nivel.")

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
    return f"Fecha y hora actual: {ahora.strftime('%d/%m/%Y %H:%M')}"

def construir_system_prompt():
    estilo = st.session_state.get("estilo_respuesta", "⚡ Directo")
    return (
        "Sos MangiAI, una IA moderna y profesional creada por Dante Mangiafico. "
        f"{ESTILOS[estilo]} "
        f"{obtener_contexto_actual()}"
    )

# -------------------- SIDEBAR --------------------
def configurar_pagina():
    st.sidebar.title("⚙️ Configuración")
    modelo = st.sidebar.selectbox("Modelo:", MODELOS, key="modelo_selector")

    st.sidebar.markdown("### 💬 Estilo de respuesta")

    if "estilo_respuesta" not in st.session_state:
        st.session_state.estilo_respuesta = "⚡ Directo"

    for estilo in ESTILOS:
        if st.sidebar.button(estilo, key=f"estilo_{estilo}", use_container_width=True):
            st.session_state.estilo_respuesta = estilo

    st.sidebar.markdown("---")
    
    if st.sidebar.button("🧹 Limpiar conversación", use_container_width=True):
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
            emoji, nombre = AVATARES.get(mensaje["estilo"], ("🤖", "MangiAI"))
            texto_seguro = html.escape(mensaje["content"])

            st.markdown(f"""
            <div class="chat-wrapper">
                <div class="chat-header">
                    <div class="style-badge">{emoji} {nombre}</div>
                    <button class="copy-btn" 
                        onclick="navigator.clipboard.writeText(decodeURIComponent('{html.escape(mensaje['content']).replace("'", "\\'")}'))">
                        📋 Copiar
                    </button>
                </div>
                <div class="chat-message">{texto_seguro}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.chat_message("user", avatar=mensaje["avatar"]):
                st.markdown(mensaje["content"])

# -------------------- RESPUESTA IA --------------------
def generar_respuesta(cliente, modelo):
    mensajes = [{"role": "system", "content": construir_system_prompt()}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.mensajes
    ]

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        temperature=0.7,
        max_tokens=2048
    )

    return respuesta.choices[0].message.content

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
else:
    mostrar_historial()

mensaje_usuario = st.chat_input("Escribí tu mensaje...")

if mensaje_usuario:
    actualizar_historial("user", mensaje_usuario, "🤔")

    with st.spinner("✨ Analizando..."):
        respuesta = generar_respuesta(cliente, modelo)

    estilo_actual = st.session_state.estilo_respuesta
    avatar = AVATARES.get(estilo_actual, ("🤖", ""))[0]

    actualizar_historial(
        "assistant",
        respuesta,
        avatar,
        estilo=estilo_actual
    )

    st.rerun()
