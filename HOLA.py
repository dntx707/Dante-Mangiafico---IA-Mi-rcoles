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

# -------------------- LOGO --------------------
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
    html, body, [class*="st-"], button, input, textarea {{
        font-family: 'Exo 2', -apple-system, BlinkMacSystemFont,
                     'Segoe UI', sans-serif !important;
    }}

    /* -------- LOGO FIXED -------- */
    .logo-fixed {{
        position: fixed;
        top: 14px;
        right: 14px;
        width: 130px;
        z-index: 999;
        opacity: 0.95;
        pointer-events: none;
        filter: drop-shadow(0 6px 18px rgba(0,0,0,0.35));
    }}

    @media (max-width: 768px) {{
        .logo-fixed {{
            width: 95px;
        }}
    }}

    /* -------- SIDEBAR BUTTONS -------- */
    div[data-testid="stSidebar"] button {{
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(0,255,170,0.3);
        color: #eaeaea;
        border-radius: 14px;
        padding: 11px 16px;
        margin-bottom: 8px;
        font-weight: 500;
        transition: all 0.15s ease;
        text-align: left;
    }}

    div[data-testid="stSidebar"] button:hover {{
        background: rgba(0,255,170,0.18);
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
    }}

    .empty-title {{
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }}

    .empty-subtitle {{
        font-size: 1.05rem;
        opacity: 0.75;
    }}

    /* -------- CHAT -------- */
    .chat-wrapper {{
        position: relative;
        padding: 18px;
        padding-top: 42px;
        border-radius: 14px;
        margin-bottom: 14px;
        background: rgba(255,255,255,0.025);
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
    }}

    .copy-btn {{
        font-size: 0.75rem;
        background: rgba(255,255,255,0.08);
        border: none;
        border-radius: 6px;
        padding: 4px 6px;
        cursor: pointer;
        opacity: 0.75;
    }}

    .copy-btn:hover {{
        background: rgba(0,255,170,0.25);
        opacity: 1;
    }}

    .chat-message {{
        line-height: 1.7;
        font-size: 1.02rem;
        white-space: pre-wrap;
        word-break: break-word;
    }}
    </style>

    <img src="data:image/png;base64,{logo_base64}" class="logo-fixed">
    """,
    unsafe_allow_html=True
)

# -------------------- HEADER --------------------
st.title("🤖 ¡Bienvenido a MangiAI!")
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
    "🎯 Estratégico": "Respondé analizando opciones y recomendando.",
    "🧑‍💼 Formal": "Respondé con tono profesional y estructurado.",
    "💻 Código": "Respondé como programador senior. Código limpio y sin explicación."
}

AVATARES = {k: (k.split()[0], k.split()[1]) for k in ESTILOS}

# -------------------- CONTEXTO --------------------
def construir_system_prompt():
    estilo = st.session_state.get("estilo_respuesta", "⚡ Directo")
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
    return f"Sos MangiAI, una IA premium creada por Dante Mangiafico. {ESTILOS[estilo]} {ahora}"

# -------------------- SIDEBAR --------------------
st.sidebar.title("⚙️ Configuración")
modelo = st.sidebar.selectbox("Modelo", MODELOS)

st.sidebar.markdown("### 💬 Estilo de respuesta")
st.session_state.setdefault("estilo_respuesta", "⚡ Directo")

for estilo in ESTILOS:
    if st.sidebar.button(estilo, use_container_width=True):
        st.session_state.estilo_respuesta = estilo

if st.sidebar.button("🧹 Limpiar conversación"):
    st.session_state.mensajes = []
    st.rerun()

# -------------------- GROQ --------------------
cliente = Groq(api_key=st.secrets["CLAVE_API"])
st.session_state.setdefault("mensajes", [])

# -------------------- HISTORIAL --------------------
def mostrar_historial():
    for m in st.session_state.mensajes:
        if m["role"] == "assistant":
            emoji, nombre = AVATARES[m["estilo"]]
            texto = html.escape(m["content"])
            st.markdown(f"""
            <div class="chat-wrapper">
                <div class="chat-header">
                    <div class="style-badge">{emoji} {nombre}</div>
                </div>
                <div class="chat-message">{texto}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.chat_message("user", avatar="🤔"):
                st.markdown(m["content"])

# -------------------- APP --------------------
if not st.session_state.mensajes:
    st.markdown("""
        <div class="empty-state">
            <div class="empty-title">¿En qué te ayudo hoy?</div>
            <div class="empty-subtitle">Elegí un estilo o escribí tu consulta</div>
        </div>
    """, unsafe_allow_html=True)
else:
    mostrar_historial()

mensaje = st.chat_input("Escribí tu mensaje...")

if mensaje:
    st.session_state.mensajes.append({"role": "user", "content": mensaje})

    with st.spinner("Analizando..."):
        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=[{"role": "system", "content": construir_system_prompt()}]
            + st.session_state.mensajes
        ).choices[0].message.content

    st.session_state.mensajes.append({
        "role": "assistant",
        "content": respuesta,
        "estilo": st.session_state.estilo_respuesta
    })

    st.rerun()
