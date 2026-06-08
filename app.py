import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import time

st.set_page_config(
    page_title="Tamil AI — Learning Assistant",
    page_icon="🪔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── GLOBAL AUDIO STOP ────────────────────────────────────────────────────────
components.html("""
<script>
    if (window.parent && window.parent.speechSynthesis) {
        window.parent.speechSynthesis.cancel();
    }
</script>
""", height=0)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    font-family: 'Outfit', sans-serif !important;
    background-color: #F5EFE8 !important;
    color: #2A1A0E !important;
}

#MainMenu, footer, header { visibility: hidden; }

/* Hide sidebar completely */
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] { display: none !important; }

/* ── Main block ── */
.block-container {
    padding: 1rem 1.5rem 3rem !important;
    max-width: 900px !important;
}

/* ── Hero ── */
.hero-wrap {
    position: relative;
    padding: 3rem 1.5rem 2.5rem;
    margin-bottom: 0.5rem;
    border-radius: 24px;
    overflow: hidden;
    background: radial-gradient(ellipse at 50% 0%, #3D1A05 0%, #1A0800 60%, #0D0400 100%);
    border: 1px solid #3D1F0A;
    text-align: center;
}
.hero-grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(232,99,10,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(232,99,10,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
}
.hero-glow {
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 300px;
    background: radial-gradient(ellipse, rgba(180,80,10,0.25) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(232,99,10,0.10);
    border: 1px solid rgba(232,99,10,0.30);
    color: #E8630A;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 6vw, 3.2rem);
    font-weight: 800;
    color: #F0E0CC;
    line-height: 1.05;
    margin-bottom: 0.6rem;
    letter-spacing: -1px;
}
.hero-title .orange { color: #E8630A; }
.hero-title .dim    { color: #5A2E10; }
.hero-sub {
    font-size: clamp(0.8rem, 2vw, 0.95rem);
    color: #7A4A25;
    font-weight: 300;
    margin-bottom: 0;
}

/* ── Stat row ── */
.stat-row {
    display: flex;
    gap: 0.75rem;
    margin: 1rem 0;
    flex-wrap: wrap;
}
.stat-box {
    flex: 1;
    min-width: 80px;
    background: rgba(232,99,10,0.06);
    border: 1px solid rgba(232,99,10,0.15);
    border-radius: 12px;
    padding: 0.8rem 0.5rem;
    text-align: center;
}
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #E8630A;
}
.stat-lbl {
    font-size: 0.6rem;
    color: #5A2E10;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 0.2rem;
}

/* ── Nav pills container ── */
.nav-pills-wrap {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    padding: 0.5rem 0 0.8rem;
    margin-bottom: 1rem;
}
.nav-pills-wrap::-webkit-scrollbar { display: none; }
.nav-pills-inner {
    display: flex;
    gap: 0.5rem;
    width: max-content;
    padding: 0 0.2rem;
}
.nav-pill {
    background: rgba(232,99,10,0.06);
    border: 1px solid rgba(232,99,10,0.20);
    color: #A06030;
    font-size: 0.8rem;
    padding: 0.45rem 1.1rem;
    border-radius: 100px;
    font-weight: 500;
    letter-spacing: 0.3px;
    white-space: nowrap;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Outfit', sans-serif;
}
.nav-pill:hover {
    background: rgba(232,99,10,0.15);
    color: #E8630A;
    border-color: rgba(232,99,10,0.40);
}
.nav-pill.active {
    background: #E8630A;
    color: #fff;
    border-color: #E8630A;
    box-shadow: 0 4px 14px rgba(232,99,10,0.35);
}

/* ── Feature card ── */
.feature-card {
    background: radial-gradient(ellipse at 50% 0%, #2E1205 0%, #160700 100%);
    border: 1px solid #3D1F0A;
    border-radius: 18px;
    padding: 1.8rem 1.8rem 1.4rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #E8630A, transparent);
    opacity: 0.5;
}
.feature-eyebrow {
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #E8630A;
    font-weight: 600;
    margin-bottom: 0.3rem;
    opacity: 0.7;
}
.feature-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(1.2rem, 4vw, 1.6rem);
    font-weight: 700;
    color: #E8630A;
    margin-bottom: 0.3rem;
}
.feature-desc {
    font-size: 0.82rem;
    color: #7A4A25;
    font-weight: 300;
}

/* ── Labels ── */
label, .stTextInput label, .stSelectbox label {
    color: #4A2A10 !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

/* ── Inputs ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #160800 !important;
    border: 1px solid #3D1F0A !important;
    border-radius: 12px !important;
    color: #D4A880 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #E8630A !important;
    box-shadow: 0 0 0 3px rgba(232,99,10,0.10) !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: #5A3A1A !important;
}

/* ── Selectbox ── */
div[data-testid="stSelectbox"] > div > div {
    background: #160800 !important;
    border: 1px solid #3D1F0A !important;
    border-radius: 12px !important;
    color: #D4A880 !important;
}

/* ── Buttons ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #C04A05, #E8630A) !important;
    color: #FFF5EE !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px !important;
    padding: 0.55rem 1.6rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(232,99,10,0.30) !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(232,99,10,0.45) !important;
}
div[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ── Output card ── */
.output-card {
    background: #0D0400;
    border: 1px solid #3D1F0A;
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    margin-top: 1rem;
    line-height: 1.9;
    font-size: 0.95rem;
    color: #C8906A;
    white-space: pre-wrap;
    word-break: break-word;
}
.output-label {
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #E8630A;
    font-weight: 600;
    opacity: 0.6;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.output-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #3D1F0A, transparent);
}

/* ── Tense badge ── */
.tense-badge {
    display: inline-block;
    background: rgba(232,99,10,0.10);
    border: 1px solid rgba(232,99,10,0.30);
    color: #E8630A;
    font-size: 0.68rem;
    padding: 0.2rem 0.8rem;
    border-radius: 100px;
    font-weight: 600;
    letter-spacing: 1px;
    margin: 0.5rem 0;
}

/* ── Chat bubbles ── */
.chat-user {
    background: #1A0A03;
    border: 1px solid #3D1F0A;
    border-radius: 16px 16px 4px 16px;
    padding: 0.9rem 1.2rem;
    margin: 0.6rem 0 0.6rem 2rem;
    color: #E8A070;
    font-size: 0.9rem;
}
.chat-ai {
    background: #0D0400;
    border: 1px solid #3D1F0A;
    border-radius: 16px 16px 16px 4px;
    padding: 0.9rem 1.2rem;
    margin: 0.6rem 2rem 0.6rem 0;
    color: #C8906A;
    font-size: 0.9rem;
    line-height: 1.75;
    white-space: pre-wrap;
}
.chat-label {
    font-size: 0.58rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.chat-label.u { color: #E8630A; }
.chat-label.a { color: #7A3A15; }

/* ── Spinner ── */
div[data-testid="stSpinner"] p { color: #E8630A !important; }

/* ── Error box ── */
.err-box {
    background: rgba(200,50,10,0.08);
    border: 1px solid rgba(200,50,10,0.25);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #D4603A;
    font-size: 0.88rem;
    margin-top: 1rem;
}

/* ── Mobile tweaks ── */
@media (max-width: 640px) {
    .block-container { padding: 0.8rem 0.8rem 3rem !important; }
    .hero-wrap { padding: 2rem 1rem 2rem; border-radius: 16px; }
    .feature-card { padding: 1.4rem 1.2rem 1.2rem; border-radius: 14px; }
    .chat-user { margin-left: 0.5rem; }
    .chat-ai  { margin-right: 0.5rem; }
    .stat-row { gap: 0.5rem; }
    .stat-box { padding: 0.6rem 0.4rem; }
    .stat-num { font-size: 1.1rem; }
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
defaults = {
    "menu": "Sentence Generator",
    "result_sentence": "",
    "result_dialogue": "",
    "result_grammar": "",
    "result_grammar_tense": "",
    "result_essay": "",
    "result_chat": "",
    "chat_user_input": "",
    "result_grammar_exp": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── API ───────────────────────────────────────────────────────────────────────
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# ─── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-grid"></div>
    <div class="hero-glow"></div>
    <div class="hero-badge">✦ AI Powered · Tamil Language</div>
    <div class="hero-title">
        Master Tamil<br>
        <span class="orange">Faster.</span> <span class="dim">Smarter.</span>
    </div>
    <p class="hero-sub">Six AI tools to read, write, speak and understand Tamil — all in one place.</p>
</div>
<div class="stat-row">
    <div class="stat-box"><div class="stat-num">6</div><div class="stat-lbl">AI Tools</div></div>
    <div class="stat-box"><div class="stat-num">∞</div><div class="stat-lbl">Generations</div></div>
    <div class="stat-box"><div class="stat-num">🔊</div><div class="stat-lbl">Voice</div></div>
</div>
""", unsafe_allow_html=True)

# ─── NAV PILLS ─────────────────────────────────────────────────────────────────
pages = [
    "Sentence Generator",
    "Dialogue Generator",
    "Grammar Builder",
    "Essay Generator",
    "Chatbot",
    "Grammar Explanation",
]

# Render pill buttons using Streamlit columns
pill_cols = st.columns(len(pages))
for i, page in enumerate(pages):
    with pill_cols[i]:
        label = page.replace(" Generator", "").replace(" Builder", "").replace(" Explanation", " Analysis")
        is_active = st.session_state.menu == page
        btn_style = "primary" if is_active else "secondary"
        if st.button(label, key=f"nav_{i}", type=btn_style if is_active else "secondary",
                     use_container_width=True):
            st.session_state.menu = page
            # clear stop speech
            components.html("""
            <script>
                if (window.parent && window.parent.speechSynthesis) {
                    window.parent.speechSynthesis.cancel();
                }
            </script>""", height=0)
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

col_stop, _ = st.columns([1,5])

with col_stop:
    if st.button("🛑 Stop Voice"):
        components.html("""
        <script>
            if (window.parent && window.parent.speechSynthesis) {
                window.parent.speechSynthesis.cancel();
            }

            if (window.speechSynthesis) {
                window.speechSynthesis.cancel();
            }
        </script>
        """, height=0)

menu = st.session_state.menu

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def render_output(text, label="Output"):
    st.markdown(f"""
    <div class="output-card">
        <div class="output-label">{label}</div>
        {text}
    </div>""", unsafe_allow_html=True)

def speak_text(text):
    clean = text.replace("'", "\\'").replace("\n", " ").replace('"', '\\"')

    components.html(f"""
    <script>
        if (window.parent && window.parent.speechSynthesis) {{

            // Stop previous speech first
            window.parent.speechSynthesis.cancel();

            var msg = new SpeechSynthesisUtterance('{clean}');
            msg.lang = 'ta-IN';
            msg.rate = 0.9;

            window.parent.speechSynthesis.speak(msg);
        }}
    </script>
    """, height=0)

def safe_generate(prompt):
    try:
        time.sleep(0.5)
        r = model.generate_content(prompt)
        return r.text
    except Exception:
        return "⚠️ API limit reached. Please wait a minute and try again."

def sentence_gen(word):
    return safe_generate(f"Convert the word into Tamil if needed and generate 5 Tamil sentences.\nInput: {word}\nOutput ONLY Tamil sentences.")

def dialogue_gen(situation):
    return safe_generate(f"Create a natural Tamil dialogue.\nSituation: {situation}\nOutput ONLY Tamil dialogue.")

def grammar_gen(word, grammar):
    return safe_generate(f"Generate Tamil sentences using {word} in {grammar} tense.\nOutput ONLY Tamil sentences.")

def essay_gen(topic):
    return safe_generate(f"Write a detailed Tamil essay on:\nTopic: {topic}\nRules:\n- Output only Tamil\n- Around 300 words\n- Include introduction, body and conclusion\n- Suitable for students")

def chatbot(user_input):
    return safe_generate(f"You are an AI Tamil Learning Assistant.\nRules:\n- Reply in Tamil\n- Help with Tamil learning\n- Answer grammar questions\n- Explain meanings\n- Be friendly\nUser: {user_input}")

def grammar_explanation(sentence):
    return safe_generate(f"Analyze the following Tamil sentence.\nSentence: {sentence}\nExplain in simple format:\n1. Subject\n2. Verb\n3. Tense\n4. Meaning in English\n5. Grammar Explanation\nKeep explanation simple for students.\nOutput in English.")

# ─── PAGES ────────────────────────────────────────────────────────────────────

# ── Sentence Generator ────────────────────────────────────────────────────────
if menu == "Sentence Generator":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-eyebrow">Tool 01</div>
        <div class="feature-title">Sentence Generator</div>
        <div class="feature-desc">Enter any word — get 5 authentic Tamil sentences crafted around it.</div>
    </div>""", unsafe_allow_html=True)

    word = st.text_input("Enter a word (English or Tamil)", placeholder="e.g. friendship / நட்பு")
    col1, _ = st.columns([1, 4])
    with col1:
        generate = st.button("Generate →", key="sg_gen")

    if generate and word:
        with st.spinner("Generating…"):
            st.session_state.result_sentence = sentence_gen(word)

    if st.session_state.result_sentence:
        render_output(st.session_state.result_sentence, "Generated Sentences")
        if st.button("🔊 Speak", key="sg_speak"):
            speak_text(st.session_state.result_sentence)

# ── Dialogue Generator ────────────────────────────────────────────────────────
elif menu == "Dialogue Generator":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-eyebrow">Tool 02</div>
        <div class="feature-title">Dialogue Generator</div>
        <div class="feature-desc">Describe a situation — get a natural Tamil conversation.</div>
    </div>""", unsafe_allow_html=True)

    situation = st.text_input("Describe the situation", placeholder="e.g. Two friends meeting after a long time")
    col1, _ = st.columns([1, 4])
    with col1:
        generate = st.button("Generate →", key="dg_gen")

    if generate and situation:
        with st.spinner("Writing dialogue…"):
            st.session_state.result_dialogue = dialogue_gen(situation)

    if st.session_state.result_dialogue:
        render_output(st.session_state.result_dialogue, "Tamil Dialogue")
        if st.button("🔊 Speak", key="dg_speak"):
            speak_text(st.session_state.result_dialogue)

# ── Grammar Builder ───────────────────────────────────────────────────────────
elif menu == "Grammar Builder":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-eyebrow">Tool 03</div>
        <div class="feature-title">Grammar Builder</div>
        <div class="feature-desc">Build Tamil sentences in any tense from a root word.</div>
    </div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        word = st.text_input("Root Word", placeholder="e.g. eat / சாப்பிடு")
    with col_b:
        grammar = st.selectbox("Tense / Form", ["Present", "Past", "Future", "Question", "Negative"])

    col1, _ = st.columns([1, 4])
    with col1:
        generate = st.button("Build →", key="gb_gen")

    if generate and word:
        with st.spinner("Building sentences…"):
            st.session_state.result_grammar = grammar_gen(word, grammar)
            st.session_state.result_grammar_tense = grammar

    if st.session_state.result_grammar:
        st.markdown(f'<div class="tense-badge">{st.session_state.result_grammar_tense} Tense</div>', unsafe_allow_html=True)
        render_output(st.session_state.result_grammar, "Grammar Output")
        if st.button("🔊 Speak", key="gb_speak"):
            speak_text(st.session_state.result_grammar)

# ── Essay Generator ───────────────────────────────────────────────────────────
elif menu == "Essay Generator":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-eyebrow">Tool 04</div>
        <div class="feature-title">Essay Generator</div>
        <div class="feature-desc">Get a full 300-word Tamil essay with intro, body, and conclusion.</div>
    </div>""", unsafe_allow_html=True)

    topic = st.text_input("Essay Topic", placeholder="e.g. The importance of water conservation")
    col1, _ = st.columns([1.2, 4])
    with col1:
        generate = st.button("Generate Essay →", key="eg_gen")

    if generate and topic:
        with st.spinner("Writing your Tamil essay…"):
            st.session_state.result_essay = essay_gen(topic)

    if st.session_state.result_essay:
        render_output(st.session_state.result_essay, "Tamil Essay")
        if st.button("🔊 Speak", key="eg_speak"):
            speak_text(st.session_state.result_essay)

# ── Chatbot ───────────────────────────────────────────────────────────────────
elif menu == "Chatbot":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-eyebrow">Tool 05</div>
        <div class="feature-title">Tamil Chatbot</div>
        <div class="feature-desc">Ask anything — grammar doubts, word meanings, or Tamil conversation practice.</div>
    </div>""", unsafe_allow_html=True)

    user_input = st.text_input("Your message", placeholder="Type in English or Tamil…")
    col1, _ = st.columns([1, 4])
    with col1:
        send = st.button("Send →", key="cb_send")

    if send and user_input:
        with st.spinner("Thinking…"):
            st.session_state.result_chat = chatbot(user_input)
            st.session_state.chat_user_input = user_input

    if st.session_state.result_chat:
        st.markdown(f"""
        <div class="chat-user">
            <div class="chat-label u">You</div>
            {st.session_state.chat_user_input}
        </div>
        <div class="chat-ai">
            <div class="chat-label a">Tamil AI</div>
            {st.session_state.result_chat}
        </div>""", unsafe_allow_html=True)
        if st.button("🔊 Speak Reply", key="cb_speak"):
            speak_text(st.session_state.result_chat)

# ── Grammar Explanation ───────────────────────────────────────────────────────
elif menu == "Grammar Explanation":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-eyebrow">Tool 06</div>
        <div class="feature-title">Grammar Explanation</div>
        <div class="feature-desc">Paste any Tamil sentence — get a full English breakdown of its grammar.</div>
    </div>""", unsafe_allow_html=True)

    sentence = st.text_input("Tamil Sentence", placeholder="e.g. அவன் பள்ளிக்கு போகிறான்")
    col1, _ = st.columns([1.3, 4])
    with col1:
        analyze = st.button("Analyze →", key="ge_btn")

    if analyze and sentence:
        with st.spinner("Analyzing grammar…"):
            st.session_state.result_grammar_exp = grammar_explanation(sentence)

    if st.session_state.result_grammar_exp:
        render_output(st.session_state.result_grammar_exp, "Grammar Analysis")