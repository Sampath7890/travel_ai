import streamlit as st
from groq import Groq
import sqlite3, datetime, os, requests
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="TravelMind AI", page_icon="✈️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Background ── */
.stApp {
  background: #080E1D;
  background-image:
    radial-gradient(ellipse 90% 60% at 15% -5%, rgba(10,80,110,0.45) 0%, transparent 55%),
    radial-gradient(ellipse 70% 50% at 85% 105%, rgba(15,75,60,0.3) 0%, transparent 55%);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: rgba(8,14,29,0.97) !important;
  border-right: 1px solid rgba(255,255,255,0.07) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 1.8rem !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }

/* ── Hero ── */
.hero-wrap { padding: 2.2rem 0 1.4rem; }
.hero-eyebrow {
  font-size: 0.68rem; font-weight: 600;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: #4ECBA0; margin-bottom: 0.7rem;
}
.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.6rem; font-weight: 800;
  color: #EDE9E0; line-height: 1.08;
  margin-bottom: 0.55rem;
}
.hero-title span { color: #4ECBA0; }
.hero-sub {
  font-size: 0.92rem; color: rgba(237,233,224,0.42);
  line-height: 1.65; margin-bottom: 1.4rem;
}

/* ── Status pills ── */
.pill-row { display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 2rem; }
.pill {
  display: inline-flex; align-items: center; gap: 5px;
  background: rgba(255,255,255,0.05);
  border: 0.5px solid rgba(255,255,255,0.11);
  border-radius: 20px; padding: 3px 11px;
  font-size: 0.73rem; font-weight: 500;
  color: rgba(237,233,224,0.55);
}
.dot { width:6px; height:6px; border-radius:50%; background:#4ECBA0; display:inline-block; }
.dot.off { background:#E24B4A; }

/* ── Destination suggestion cards ── */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 2rem;
}
.dest-card {
  background: rgba(255,255,255,0.04);
  border: 0.5px solid rgba(255,255,255,0.09);
  border-radius: 14px;
  padding: 1rem 1rem 0.85rem;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}
.dest-card:hover {
  background: rgba(78,203,160,0.07);
  border-color: rgba(78,203,160,0.3);
}
.dest-card .dc-icon { font-size: 1.4rem; margin-bottom: 0.45rem; }
.dest-card .dc-title {
  font-size: 0.82rem; font-weight: 600;
  color: rgba(237,233,224,0.85); line-height: 1.35;
  margin-bottom: 0.2rem;
}
.dest-card .dc-tag {
  font-size: 0.7rem; color: #4ECBA0; font-weight: 500;
}

/* ── Weather widget ── */
.weather-card {
  background: rgba(78,203,160,0.07);
  border: 0.5px solid rgba(78,203,160,0.25);
  border-radius: 14px;
  padding: 1rem 1.2rem;
  margin-bottom: 1.2rem;
  display: flex; align-items: center; gap: 1rem;
}
.wc-temp {
  font-family: 'Playfair Display', serif;
  font-size: 2rem; font-weight: 700;
  color: #EDE9E0; flex-shrink: 0;
}
.wc-info { flex: 1; }
.wc-city { font-size: 0.85rem; font-weight: 600; color: #EDE9E0; margin-bottom: 2px; }
.wc-desc { font-size: 0.78rem; color: rgba(237,233,224,0.55); }
.wc-stats { display: flex; gap: 12px; margin-top: 4px; }
.wc-stat { font-size: 0.72rem; color: rgba(237,233,224,0.5); }
.wc-stat b { color: rgba(237,233,224,0.8); }

/* ── Chat messages (override Streamlit native) ── */
div[data-testid="stChatMessage"] {
  background: rgba(255,255,255,0.04) !important;
  border: 0.5px solid rgba(255,255,255,0.08) !important;
  border-radius: 16px !important;
  padding: 1rem 1.2rem !important;
  margin-bottom: 0.6rem !important;
}
div[data-testid="stChatMessage"][data-message-author-role="user"] {
  background: rgba(20,55,110,0.35) !important;
  border-color: rgba(78,203,160,0.15) !important;
}
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] span {
  color: rgba(237,233,224,0.88) !important;
  font-size: 0.93rem !important;
  line-height: 1.7 !important;
}
div[data-testid="stChatMessage"] strong { color: #EDE9E0 !important; font-weight: 600 !important; }
div[data-testid="stChatMessage"] h1,
div[data-testid="stChatMessage"] h2,
div[data-testid="stChatMessage"] h3 {
  color: #EDE9E0 !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  margin-top: 0.8rem !important;
}
div[data-testid="stChatMessage"] code {
  background: rgba(78,203,160,0.12) !important;
  color: #4ECBA0 !important;
  border-radius: 4px !important;
  padding: 1px 5px !important;
  font-size: 0.85rem !important;
}
div[data-testid="stChatMessage"] img { display: none; }

/* ── Chat input bar ── */
div[data-testid="stChatInput"] > div {
  background: rgba(255,255,255,0.05) !important;
  border: 0.5px solid rgba(255,255,255,0.15) !important;
  border-radius: 14px !important;
}
div[data-testid="stChatInput"] textarea {
  background: transparent !important;
  color: #EDE9E0 !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.93rem !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
  color: rgba(237,233,224,0.28) !important;
}
div[data-testid="stChatInput"] button {
  background: linear-gradient(135deg, #0A506E, #0F6E56) !important;
  border-radius: 10px !important;
  border: none !important;
}

/* ── Sidebar components ── */
.sb-logo {
  font-family: 'Playfair Display', serif;
  font-size: 1.2rem; font-weight: 800;
  color: #EDE9E0; padding: 0 0.3rem; margin-bottom: 2px;
}
.sb-sub {
  font-size: 0.73rem; color: rgba(237,233,224,0.3);
  padding: 0 0.3rem; margin-bottom: 1.1rem;
}
.sb-section {
  font-size: 0.65rem; font-weight: 600;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: rgba(237,233,224,0.3);
  padding: 0 0.2rem; margin-bottom: 0.5rem; margin-top: 0.2rem;
}
.sb-prompt {
  background: rgba(255,255,255,0.04);
  border: 0.5px solid rgba(255,255,255,0.08);
  border-radius: 9px;
  padding: 0.55rem 0.75rem;
  margin-bottom: 0.35rem;
  font-size: 0.8rem;
  color: rgba(237,233,224,0.65);
  cursor: pointer;
  transition: border-color 0.15s;
}
.sb-prompt:hover { border-color: rgba(78,203,160,0.35); color: #EDE9E0; }
.history-item {
  background: rgba(255,255,255,0.03);
  border: 0.5px solid rgba(255,255,255,0.06);
  border-radius: 9px;
  padding: 0.5rem 0.7rem;
  margin-bottom: 0.35rem;
  font-size: 0.78rem;
  color: rgba(237,233,224,0.55);
  line-height: 1.4;
}
.history-ts { font-size: 0.67rem; color: #4ECBA0; font-weight: 500; margin-bottom: 2px; }

/* ── Buttons ── */
.stButton > button {
  background: rgba(255,255,255,0.05) !important;
  color: rgba(237,233,224,0.7) !important;
  border: 0.5px solid rgba(255,255,255,0.12) !important;
  border-radius: 9px !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  padding: 0.45rem 0.9rem !important;
  transition: all 0.15s !important;
}
.stButton > button:hover {
  background: rgba(78,203,160,0.1) !important;
  border-color: rgba(78,203,160,0.35) !important;
  color: #EDE9E0 !important;
}

/* ── API key input ── */
.stTextInput > div > div > input {
  background: rgba(255,255,255,0.05) !important;
  border: 0.5px solid rgba(255,255,255,0.12) !important;
  border-radius: 9px !important;
  color: #EDE9E0 !important;
  font-size: 0.85rem !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(237,233,224,0.25) !important; }

div[data-testid="stDivider"] hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Spinner ── */
div[data-testid="stSpinner"] p { color: rgba(237,233,224,0.5) !important; }
</style>
""", unsafe_allow_html=True)

# ── Database ─────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("travel.db")
    conn.execute("CREATE TABLE IF NOT EXISTS searches (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT, response TEXT, ts TEXT)")
    conn.commit(); conn.close()

def save_search(q, r):
    conn = sqlite3.connect("travel.db")
    conn.execute("INSERT INTO searches (query,response,ts) VALUES (?,?,?)",
                 (q, r[:400], datetime.datetime.now().strftime("%d %b, %H:%M")))
    conn.commit(); conn.close()

def get_history():
    conn = sqlite3.connect("travel.db")
    rows = conn.execute("SELECT query,ts FROM searches ORDER BY id DESC LIMIT 5").fetchall()
    conn.close(); return rows

def clear_db():
    conn = sqlite3.connect("travel.db")
    conn.execute("DELETE FROM searches"); conn.commit(); conn.close()

# ── Weather ───────────────────────────────────────────────────
CITIES = [
    "paris","london","tokyo","dubai","new york","singapore","bangkok","rome",
    "bali","sydney","istanbul","barcelona","mumbai","delhi","hyderabad","kolkata",
    "goa","jaipur","amsterdam","berlin","prague","vienna","lisbon","cairo",
    "kuala lumpur","hong kong","seoul","beijing","shanghai","maldives",
    "phuket","colombo","kathmandu","manali","shimla","darjeeling","ooty","munnar"
]

def get_weather(city):
    key = os.getenv("WEATHER_API_KEY", "")
    if not key:
        try: key = st.secrets.get("WEATHER_API_KEY", "")
        except Exception: key = ""
    if not key: return None
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric",
            timeout=5)
        if r.status_code == 200:
            d = r.json()
            return {
                "city": city.title(),
                "temp": round(d["main"]["temp"]),
                "feels": round(d["main"]["feels_like"]),
                "min": round(d["main"]["temp_min"]),
                "max": round(d["main"]["temp_max"]),
                "desc": d["weather"][0]["description"].capitalize(),
                "icon": d["weather"][0]["main"],
                "humidity": d["main"]["humidity"],
                "wind": round(d["wind"]["speed"]),
                "visibility": round(d.get("visibility", 10000) / 1000, 1),
            }
    except Exception: pass
    return None

def weather_icon(main):
    return {"Clear":"☀️","Clouds":"☁️","Rain":"🌧️","Drizzle":"🌦️",
            "Thunderstorm":"⛈️","Snow":"❄️","Mist":"🌫️","Haze":"🌫️"}.get(main, "🌤️")

def weather_to_prompt(w):
    if not w: return ""
    comfort = ("hot and humid" if w["temp"]>30 and w["humidity"]>70 else
               "hot" if w["temp"]>32 else "warm" if w["temp"]>24 else
               "mild" if w["temp"]>16 else "cool" if w["temp"]>10 else "cold")
    rain = " Rain/clouds likely — recommend umbrella." if any(x in w["desc"].lower() for x in ["rain","cloud","drizzle"]) else ""
    return f"""

=== LIVE WEATHER DATA FOR {w['city'].upper()} ===
Conditions : {w['desc']}, {w['temp']}°C (feels {w['feels']}°C)
Range today: {w['min']}°C – {w['max']}°C  |  Humidity: {w['humidity']}%  |  Wind: {w['wind']} km/h
Overall    : {comfort}{rain}

MANDATORY INSTRUCTIONS:
1. Start with "🌤 Current Weather in {w['city']}: {w['desc']}, {w['temp']}°C (feels {w['feels']}°C), H:{w['humidity']}%"
2. Adjust itinerary timings based on heat/rain (avoid outdoor at peak heat)
3. Packing list MUST match these exact conditions
4. Add weather warnings if relevant
=== END WEATHER ===
"""

def detect_city(query):
    q = query.lower()
    for city in CITIES:
        if city in q: return city
    return ""

# ── Groq ─────────────────────────────────────────────────────
SYSTEM = """You are TravelMind, an elite AI travel concierge.

ALWAYS structure trip plans with these exact sections:
🌤 Current Weather  (only if live data is given — show the exact numbers)
📋 Trip Overview    (destination, duration, total budget in ₹)
🗓 Day-by-Day       (Morning / Afternoon / Evening for each day — real place names, entry fees, timings)
🏨 Where to Stay    (3 specific options with price per night in ₹)
🍽 What to Eat      (5+ specific local dishes + restaurant names)
🎒 Packing List     (based on actual weather conditions)
💰 Budget Breakdown (transport + stay + food + activities = total in ₹)
⚠️ Tips & Warnings

Rules:
- Use REAL place names and REAL prices. Never vague — say "Calangute Beach (free, best 6–8am)" not "visit the beach".
- Indian destinations: prices in ₹. International: ₹ + local currency.
- Weather data provided → USE IT. Adjust timings and packing accordingly.
- Format responses with bold headers, bullet points, and clear structure."""

def get_client():
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        try: key = st.secrets.get("GROQ_API_KEY", "")
        except Exception: key = ""
    return Groq(api_key=key) if key else None

def ask_ai(client, query, history):
    if not client:
        return "⚠️ No Groq API key found. Paste your key (gsk_...) in the sidebar."
    city = detect_city(query)
    w = get_weather(city) if city else None
    full_query = query + weather_to_prompt(w)
    msgs = [{"role":"system","content":SYSTEM}]
    for t in history[-6:]:
        msgs.append({"role":t["role"],"content":t["content"]})
    msgs.append({"role":"user","content":full_query})
    try:
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=msgs, max_tokens=2048)
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {e}"

# ── Init ─────────────────────────────────────────────────────
init_db()
if "history" not in st.session_state: st.session_state.history = []
if "client"  not in st.session_state: st.session_state.client  = get_client()
if "weather" not in st.session_state: st.session_state.weather = None

DEST_CARDS = [
    ("🏖️", "3-day Goa trip",         "Beach · Budget",   "Plan a 3 day Goa trip under ₹8000"),
    ("🗼", "5-day Paris under ₹1L",   "Europe · Culture", "Plan a 5 day Paris trip under ₹1 lakh"),
    ("🌸", "Japan cherry blossoms",   "Asia · Nature",    "Best time and places for cherry blossoms in Japan"),
    ("🏜️", "Dubai from India",        "Visa · Guide",     "Dubai visa requirements and trip plan from India"),
    ("🎒", "Backpack SE Asia",         "Adventure · Tips", "Backpacking Southeast Asia starter guide under ₹60000"),
    ("🏔️", "Manali in summer",        "India · Hill",     "Plan a 4 day Manali trip in summer"),
]

PROMPTS = [
    "Best beaches from Hyderabad — budget",
    "Europe 3 weeks on ₹2 lakhs",
    "Bali trip from India — complete guide",
    "Shimla vs Manali — which to pick?",
    "Singapore 4 days itinerary",
    "Rajasthan road trip plan",
]

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-logo">✈ TravelMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">AI-powered travel concierge</div>', unsafe_allow_html=True)

    # API key
    st.markdown('<div class="sb-section">Groq API Key</div>', unsafe_allow_html=True)
    key_in = st.text_input("", type="password", placeholder="gsk_...", label_visibility="collapsed")
    if key_in:
        os.environ["GROQ_API_KEY"] = key_in
        st.session_state.client = get_client()
        st.success("Connected!", icon="✅")
    elif not st.session_state.client:
        st.session_state.client = get_client()

    st.divider()

    # Quick prompts
    st.markdown('<div class="sb-section">Quick Prompts</div>', unsafe_allow_html=True)
    for p in PROMPTS:
        if st.button(p, use_container_width=True, key=f"p_{p}"):
            st.session_state["prefill"] = p; st.rerun()

    st.divider()

    # History
    st.markdown('<div class="sb-section">Recent Searches</div>', unsafe_allow_html=True)
    rows = get_history()
    if rows:
        for q, ts in rows:
            st.markdown(f'<div class="history-item"><div class="history-ts">{ts}</div>{q[:58]}{"…" if len(q)>58 else ""}</div>',
                       unsafe_allow_html=True)
        if st.button("Clear history", use_container_width=True):
            clear_db(); st.rerun()
    else:
        st.markdown('<p style="font-size:.75rem;color:rgba(237,233,224,0.22);padding:0 .2rem">No searches yet.</p>',
                   unsafe_allow_html=True)

    st.divider()
    if st.button("New chat", use_container_width=True):
        st.session_state.history = []; st.session_state.weather = None; st.rerun()

# ── MAIN ─────────────────────────────────────────────────────
main = st.container()
with main:
    # Hero
    connected = st.session_state.client is not None
    st.markdown(f"""
    <div class="hero-wrap">
      <div class="hero-eyebrow">AI Travel Concierge</div>
      <div class="hero-title">Where are you<br>headed <span>next?</span></div>
      <div class="hero-sub">Itineraries · Visas · Budgets · Hidden gems — ask anything.</div>
      <div class="pill-row">
        <span class="pill"><span class="dot {'off' if not connected else ''}"></span>{'Groq connected' if connected else 'Add API key'}</span>
        <span class="pill">SQLite storage</span>
        <span class="pill">Live weather</span>
        <span class="pill">Llama 3.3 70B</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # Weather card (if last query had weather)
    w = st.session_state.get("weather")
    if w:
        icon = weather_icon(w["icon"])
        st.markdown(f"""
        <div class="weather-card">
          <div class="wc-temp">{icon} {w['temp']}°C</div>
          <div class="wc-info">
            <div class="wc-city">{w['city']}</div>
            <div class="wc-desc">{w['desc']} · Feels like {w['feels']}°C</div>
            <div class="wc-stats">
              <span class="wc-stat"><b>{w['min']}–{w['max']}°C</b> range</span>
              <span class="wc-stat"><b>{w['humidity']}%</b> humidity</span>
              <span class="wc-stat"><b>{w['wind']} km/h</b> wind</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    # Destination cards (show only when no chat yet)
    if not st.session_state.history:
        st.markdown('<div class="cards-grid">', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, (icon, title, tag, prompt) in enumerate(DEST_CARDS):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="dest-card">
                  <div class="dc-icon">{icon}</div>
                  <div class="dc-title">{title}</div>
                  <div class="dc-tag">{tag}</div>
                </div>""", unsafe_allow_html=True)
                if st.button("Plan this →", key=f"dc_{i}", use_container_width=True):
                    st.session_state["prefill"] = prompt; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat messages — uses st.chat_message so markdown renders properly
    for t in st.session_state.history:
        role = "user" if t["role"] == "user" else "assistant"
        with st.chat_message(role, avatar="🧭" if role == "assistant" else "👤"):
            st.markdown(t["content"])

    # Chat input — sticky at bottom, handles Enter key natively
    prefill = st.session_state.pop("prefill", "")
    prompt = st.chat_input(
        placeholder="Ask about destinations, itineraries, visas, budgets…",
    )
    # Handle prefill from sidebar/cards
    if prefill and not prompt:
        prompt = prefill

    if prompt:
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        city = detect_city(prompt)
        if city:
            w = get_weather(city)
            st.session_state.weather = w
        else:
            st.session_state.weather = None

        with st.chat_message("assistant", avatar="🧭"):
            with st.spinner("Planning your trip…"):
                ans = ask_ai(st.session_state.client, prompt, st.session_state.history[:-1])
            st.markdown(ans)

        st.session_state.history.append({"role": "assistant", "content": ans})
        save_search(prompt, ans)
        st.rerun()
