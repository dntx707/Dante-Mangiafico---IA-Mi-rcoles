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

# -------------------- LOGOS --------------------
def cargar_logo_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_fijo_base64 = cargar_logo_base64("logomangi.png")
logo_definitivo_base64 = cargar_logo_base64("logodefinitivo2.png")

# -------------------- ESTILOS GLOBALES --------------------
st.markdown(
    f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
    html, body, [class*="st-"], div, span, p, h1, h2, h3, h4, h5, h6,
    button, input, textarea {{
        font-family: 'Exo 2', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }}

    h1 {{
        font-weight: 900;
        margin: 0;
    }}

    /* -------- LOGO FIJO -------- */
    .logo-fixed {{
        position: fixed;
        top: 16px;
        right: 16px;
        width: 150px;
        z-index: 999;
        opacity: 0.95;
        pointer-events: none;
        filter: drop-shadow(0 6px 18px rgba(0,0,0,0.35));
    }}

    /* -------- ANIMACIÓN LOGO PRINCIPAL -------- */
    @keyframes flotar {{
        0%, 100% {{
            transform: translateY(0px);
        }}
        50% {{
            transform: translateY(-12px);
        }}
    }}

    @keyframes brillo {{
        0%, 100% {{
            filter: drop-shadow(0 0 8px rgba(147, 51, 234, 0.3));
        }}
        50% {{
            filter: drop-shadow(0 0 20px rgba(147, 51, 234, 0.6));
        }}
    }}

    /* -------- HEADER -------- */
    .header-logo {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 14px;
        margin-top: 32px;
        margin-bottom: 42px;
        text-align: center;
    }}

    .header-logo img {{
        width: 118px;
        height: 118px;
        animation: flotar 3s ease-in-out infinite, brillo 3s ease-in-out infinite;
    }}

    .header-logo h1 {{
        font-size: 2.9rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        line-height: 1.15;
    }}

    .header-subtitle {{
        font-size: 1.05rem;
        opacity: 0.75;
        margin-top: -6px;
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

    <img src="data:image/png;base64,{logo_fijo_base64}" class="logo-fixed">
    """,
    unsafe_allow_html=True
)

# -------------------- HEADER --------------------
st.markdown(
    f"""
    <div class="header-logo">
        <img src="data:image/png;base64,{logo_definitivo_base64}">
        <h1>¡Bienvenido a MangiAI!</h1>
        <div class="header-subtitle">
            Tu asistente inteligente, elevado al siguiente nivel. Siempre.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------- CONFIGURACIÓN --------------------
MODELOS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b"
]

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

# -------------------- FUNCIONES --------------------
def construir_system_prompt():
    estilo = st.session_state.get("estilo_respuesta", "⚡ Directo")
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    return (
        f"MangiAI, una IA moderna y profesional creada por Dante Mangiafico. "
        f"{ESTILOS[estilo]} {timestamp}"
    )

def configurar_sidebar():
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
    for m in st.session_state.mensajes:
        if m["role"] == "assistant":
            emoji, nombre = AVATARES.get(m["estilo"], ("🤖", "MangiAI"))
            texto = html.escape(m["content"])
            st.markdown(f"**{emoji} {nombre}**\n\n{texto}")
        else:
            with st.chat_message("user", avatar=m["avatar"]):
                st.markdown(m["content"])

def generar_respuesta(cliente, modelo):
    mensajes = [{"role": "system", "content": construir_system_prompt()}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.mensajes
    ]

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes
    )

    return respuesta.choices[0].message.content

# -------------------- APP PRINCIPAL --------------------
inicializar_estado()
cliente = Groq(api_key=st.secrets["CLAVE_API"])
modelo = configurar_sidebar()

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

    with st.spinner("Analizando..."):
        respuesta = generar_respuesta(cliente, modelo)

    estilo_actual = st.session_state.estilo_respuesta
    avatar = AVATARES[estilo_actual][0]

    actualizar_historial("assistant", respuesta, avatar, estilo=estilo_actual)

    st.rerun()
