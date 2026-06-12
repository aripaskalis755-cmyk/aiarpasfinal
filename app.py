import streamlit as st
import streamlit.components.v1 as components
import requests
import xml.etree.ElementTree as ET
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="AI ARPAS - Sistem Informasi Meteorologi & Geofisika",
    page_icon="🌩️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- BACA SECRETS (API Key) ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- FUNGSI GROQ ---
def chat_with_groq(system_prompt, user_message):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Koneksi Groq terganggu: {str(e)}"

# --- STYLE TEMA TERANG (LIGHT MODE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,600;14..32,700;14..32,800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* GLOBAL LIGHT THEME */
    .stApp {
        background: linear-gradient(135deg, #f5f7fc 0%, #eef2f6 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* HIDE DEFAULT STREAMLIT DECORATIONS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* CUSTOM SCROLLBAR */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #e2e8f0; border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: #94a3b8; border-radius: 10px; }
    
    /* HEADER UTAMA - GLASS MORPHISM TERANG */
    .main-header {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(16px);
        border-radius: 40px;
        padding: 0.8rem 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 100, 150, 0.2);
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05), 0 8px 10px -6px rgba(0,0,0,0.02);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    
    /* JUDUL WARNA GELAP */
    .title-section h1 {
        font-family: 'Space Grotesk', monospace;
        font-size: 2.8rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        letter-spacing: -1px;
        text-shadow: none;
    }
    
    .bmkg-badge {
        background: linear-gradient(135deg, #0284c7, #0369a1);
        padding: 4px 14px;
        border-radius: 40px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1px;
        color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    .live-clock {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(8px);
        padding: 8px 18px;
        border-radius: 50px;
        border: 1px solid #cbd5e1;
        font-family: 'Space Grotesk', monospace;
        font-size: 1rem;
        font-weight: 500;
        color: #0f172a;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        letter-spacing: 0.5px;
    }
    
    /* KARTU INFO - PUTIH DENGAN BAYANGAN LEMBUT */
    .info-panel {
        background: white;
        border-radius: 24px;
        padding: 0.8rem 1.2rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.01);
        transition: all 0.2s ease;
    }
    .info-panel:hover {
        border-color: #38bdf8;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
        transform: translateY(-2px);
    }
    .info-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #475569;
        font-weight: 600;
    }
    .info-value {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0f172a;
    }
    .badge-danger {
        background: #fee2e2;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        border-left: 3px solid #ef4444;
        color: #991b1b;
    }
    
    /* CHAT AREA - GAYA MODERN TERANG */
    .stChatMessage {
        background: white !important;
        border-radius: 20px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
        padding: 12px 18px !important;
        margin-bottom: 16px !important;
    }
    .stChatMessage p, .stChatMessage div {
        color: #1e293b !important;
    }
    .stChatInput textarea {
        background: white !important;
        border-radius: 36px !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
        font-size: 0.9rem;
        padding: 12px 20px !important;
        box-shadow: none !important;
    }
    .stChatInput textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56,189,248,0.2) !important;
    }
    button[kind="primary"] {
        background: linear-gradient(90deg, #0284c7, #38bdf8) !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600;
        color: white !important;
    }
    
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #cbd5e1, #94a3b8, transparent);
        margin: 1.5rem 0;
    }
    
    .suggestion-chip {
        background: #f1f5f9;
        border-radius: 40px;
        padding: 6px 14px;
        font-size: 0.75rem;
        color: #0284c7;
        cursor: pointer;
        transition: 0.2s;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    .suggestion-chip:hover {
        background: #e0f2fe;
        color: #0369a1;
    }
    
    .caption-text, .stCaption {
        color: #64748b !important;
    }
    div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] li {
        color: #334155;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
    }
    .stMarkdown h3 {
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER (HTML + JS) ---
components.html("""
<div class="main-header">
    <div style="display: flex; align-items: center; gap: 1.5rem;">
        <div style="font-size: 2.8rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">🛰️</div>
        <div class="title-section">
            <h1>AI ARPAS</h1>
            <div style="display: flex; gap: 0.8rem; align-items: center; margin-top: 8px;">
                <span class="bmkg-badge">BMKG TERINTEGRASI</span>
                <span style="color: #475569; font-size: 0.75rem; font-weight: 500;">Sistem Meteorologi & Geofisika</span>
            </div>
        </div>
    </div>
    <div class="live-clock" id="live-clock">--:--:--</div>
</div>
<script>
    function updateTime() {
        var d = new Date();
        var days = ["MINGGU", "SENIN", "SELASA", "RABU", "KAMIS", "JUMAT", "SABTU"];
        var months = ["JAN", "FEB", "MAR", "APR", "MEI", "JUN", "JUL", "AGT", "SEP", "OKT", "NOV", "DES"];
        var dateStr = days[d.getDay()] + ", " + d.getDate() + " " + months[d.getMonth()] + " " + d.getFullYear();
        var timeStr = d.getHours().toString().padStart(2,'0') + ":" + d.getMinutes().toString().padStart(2,'0') + ":" + d.getSeconds().toString().padStart(2,'0');
        document.getElementById("live-clock").innerHTML = dateStr + " &nbsp; • &nbsp; " + timeStr + " WIB";
    }
    setInterval(updateTime, 1000);
    updateTime();
</script>
""", height=120)

# --- DATA FUNCTIONS (sama seperti sebelumnya) ---
@st.cache_data(ttl=300)
def get_gempa_terkini():
    try:
        res = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json", timeout=10).json()
        return res["Infogempa"]["gempa"]
    except:
        return None

@st.cache_data(ttl=600)
def get_weather_city(city="Jakarta"):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&lang=id"
    try:
        return requests.get(url, timeout=8).json()
    except:
        return None

@st.cache_data(ttl=600)
def get_bmkg_alert_summary():
    try:
        rss_url = "https://www.bmkg.go.id/alerts/nowcast/id/rss.xml"
        resp = requests.get(rss_url, timeout=10)
        root = ET.fromstring(resp.content)
        items = root.findall('.//item')
        alerts = []
        for item in items[:3]:
            title = item.find('title').text if item.find('title') is not None else ""
            if title:
                alerts.append(f"• {title[:60]}")
        return alerts if alerts else ["Tidak ada peringatan dini saat ini"]
    except:
        return ["Gagal mengambil data peringatan"]

# --- LAYOUT 2 KOLOM ---
left_col, right_col = st.columns([1.2, 2.8], gap="large")

with left_col:
    st.markdown("### 📡 PANTAUAN REAL-TIME")
    
    gempa = get_gempa_terkini()
    if gempa:
        mag = gempa['Magnitude']
        warna = "#dc2626" if float(mag) >= 5.0 else "#ea580c"
        st.markdown(f"""
        <div class="info-panel">
            <div class="info-label">⚠️ GEMPA TERKINI</div>
            <div class="info-value" style="font-size: 2rem; color: {warna};">{mag} <span style="font-size:0.9rem;">SR</span></div>
            <div style="font-size:0.8rem; color:#334155;">{gempa['Wilayah'][:70]}</div>
            <div style="font-size:0.7rem; color:#64748b;">{gempa['Tanggal']} {gempa['Jam']} WIB</div>
            <div class="badge-danger" style="display:inline-block; margin-top:8px;">{gempa['Potensi']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-panel">📡 Gagal memuat data gempa</div>', unsafe_allow_html=True)
    
    weather_jkt = get_weather_city("Jakarta")
    if weather_jkt and "current" in weather_jkt:
        curr = weather_jkt["current"]
        st.markdown(f"""
        <div class="info-panel">
            <div class="info-label">🌆 CUACA JAKARTA</div>
            <div class="info-value">{curr['temp_c']}°C • {curr['condition']['text']}</div>
            <div style="color:#475569;">💨 {curr['wind_kph']} km/j | 💧 {curr['humidity']}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    alerts = get_bmkg_alert_summary()
    st.markdown(f"""
    <div class="info-panel">
        <div class="info-label">🚨 PERINGATAN DINI CUACA</div>
        <div style="font-size:0.75rem; color:#334155;">
            {chr(10).join(alerts[:2])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("Sumber: BMKG & WeatherAPI • Diperbarui otomatis")

with right_col:
    st.markdown("### 💬 AI ARPAS · Asisten Meteorologi & Kebumian")
    
    def get_context_from_query(user_query):
        context = ""
        q_lower = user_query.lower()
        if any(k in q_lower for k in ["gempa terkini", "gempa terbaru", "info gempa", "gempa hari ini"]):
            g = get_gempa_terkini()
            if g:
                context = f"[DATA GEMPA TERKINI BMKG]\nWaktu: {g['Tanggal']} {g['Jam']}\nMagnitudo: {g['Magnitude']} SR\nLokasi: {g['Wilayah']}\nKedalaman: {g['Kedalaman']}\nPotensi: {g['Potensi']}\n"
        kota_match = re.search(r"(?:cuaca di|cuaca|prakiraan cuaca)\s+(\w+)", q_lower)
        if kota_match:
            kota = kota_match.group(1).capitalize()
            w = get_weather_city(kota)
            if w and "current" in w:
                curr = w["current"]
                context += f"\n[DATA CUACA UNTUK {kota}]\nSuhu: {curr['temp_c']}°C\nKelembaban: {curr['humidity']}%\nAngin: {curr['wind_kph']} km/j\nKondisi: {curr['condition']['text']}\n"
        return context
    
    def chat_with_arpas(prompt, context=""):
        system = (
            "Kamu adalah AI Arpas, asisten meteorologi & geofisika yang terintegrasi dengan data BMKG. "
            "Gunakan data real-time yang diberikan dalam [DATA ...] untuk menjawab gempa atau cuaca. "
            "Jawab dalam bahasa Indonesia yang jelas, berwibawa, dan utamakan keselamatan. "
            "Jika tidak ada data real-time, gunakan pengetahuan hingga 2026. "
            "Tolak pertanyaan di luar kebumian dengan sopan. "
            "Perkenalkan dirimu sebagai AI Arpas yang ditenagai Groq."
        )
        return chat_with_groq(system, f"Konteks: {context}\n\nPertanyaan: {prompt}")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Selamat datang di **AI ARPAS** – sistem informasi meteorologi dan geofisika terintegrasi. Saya siap membantu informasi gempa terkini, cuaca real-time, prakiraan iklim, dan fenomena kebumian lainnya. Silakan bertanya!"}
        ]
    
    chat_container = st.container(height=420)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    if user_input := st.chat_input("Tanyakan tentang gempa, cuaca, atau prediksi..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
            with st.spinner("🛰️ Menghubungkan ke sistem AI Groq & BMKG..."):
                konteks = get_context_from_query(user_input)
                response = chat_with_arpas(user_input, konteks)
                with st.chat_message("assistant"):
                    st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Tombol saran cepat
    st.markdown("#### 💡 Pertanyaan cepat")
    col_a, col_b, col_c = st.columns(3)
    if col_a.button("🌍 Gempa terkini", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Gempa terkini"})
        with chat_container:
            with st.chat_message("user"):
                st.markdown("Gempa terkini")
            with st.spinner("Mengakses data seismik..."):
                konteks = get_context_from_query("gempa terkini")
                response = chat_with_arpas("Gempa terkini", konteks)
                with st.chat_message("assistant"):
                    st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    if col_b.button("☁️ Cuaca Jakarta", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Cuaca di Jakarta"})
        with chat_container:
            with st.chat_message("user"):
                st.markdown("Cuaca di Jakarta")
            with st.spinner("Memproses data atmosfer..."):
                konteks = get_context_from_query("cuaca di Jakarta")
                response = chat_with_arpas("Cuaca di Jakarta", konteks)
                with st.chat_message("assistant"):
                    st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    if col_c.button("📅 Prakiraan musim hujan 2026", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Bagaimana prakiraan musim hujan 2026 di Indonesia?"})
        with chat_container:
            with st.chat_message("user"):
                st.markdown("Bagaimana prakiraan musim hujan 2026 di Indonesia?")
            with st.spinner("Menganalisis data klimatologi..."):
                response = chat_with_arpas("Prakiraan musim hujan 2026 di Indonesia", "")
                with st.chat_message("assistant"):
                    st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# --- FOOTER ---
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; font-size: 0.7rem; color: #64748b; padding-bottom: 20px;'>"
    "© 2026 AI ARPAS · Data gempa & peringatan oleh BMKG | Cuaca oleh WeatherAPI | AI dipercepat oleh Groq"
    "</div>",
    unsafe_allow_html=True
)
