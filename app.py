import streamlit as st
from emotion import get_top_emotions, analyze_emotion
from llm import generate_doors, generate_custom_door
from image_gen import generate_door_image, overlay_poem_on_image
from rag import get_context
from poem_card import create_poem_card
from door_sounds import generate_door_sound
import base64
import re
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="KNOCK — Which Door Are You Knocking On?",
    page_icon="🚪",
    layout="wide",
)

# ── PER-DOOR CONFIG ─────────────────────────────────────────────────────────────
DOOR_CONFIG = {
    "Billy":    {"color": "#c8a030", "bg": "#1f1600", "emoji": "🤠"},
    "Vietnam":  {"color": "#7a9a50", "bg": "#0d1508", "emoji": "🪖"},
    "Dylan":    {"color": "#d07020", "bg": "#1a0e00", "emoji": "🎸"},
    "Survivor": {"color": "#8090c0", "bg": "#080a14", "emoji": "🕯️"},
}

def get_door_config(door_title):
    for key, cfg in DOOR_CONFIG.items():
        if key.lower() in door_title.lower():
            return cfg
    return {"color": "#c8a96e", "bg": "#1a1510", "emoji": "🚪"}

def parse_door(door_text):
    door_title = ""
    reason_text = ""
    poem_lines = []
    in_poem = False
    for line in door_text.strip().split("\n"):
        if line.startswith("DOOR:"):
            door_title = line.replace("DOOR:", "").strip()
            in_poem = False
        elif line.startswith("REASON:"):
            reason_text = line.replace("REASON:", "").strip()
            in_poem = False
        elif line.startswith("POEM:"):
            in_poem = True
        elif in_poem and line.strip():
            poem_lines.append(line.strip())
    return door_title, reason_text, poem_lines[:6]

# ── CSS ─────────────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Special+Elite&display=swap');

.stApp { background-color: #0d0b07 !important; }
.block-container {
    background-color: #0d0b07 !important;
    max-width: 860px;
    padding-top: 1.5rem;
}
body, p, li, div { color: #d4b483; font-family: 'Playfair Display', serif; }
h1, h2, h3, h4, h5 { font-family: 'Special Elite', cursive !important; color: #c8a96e !important; }
.stMarkdown p { color: #d4b483; }

.knock-title {
    text-align: center;
    font-family: 'Special Elite', cursive !important;
    font-size: 4rem;
    color: #c8a96e;
    letter-spacing: 14px;
    text-shadow: 0 0 50px rgba(200,169,110,0.2);
    margin-bottom: 0.2rem;
}
.knock-subtitle {
    text-align: center;
    font-family: 'Playfair Display', serif;
    font-style: italic;
    color: #6a5535;
    font-size: 0.95rem;
    margin-top: 0;
    margin-bottom: 2rem;
    letter-spacing: 1px;
}
hr { border-color: #2a2010 !important; }

.stTextArea textarea {
    background-color: #141008 !important;
    border: 1px solid #3a2a15 !important;
    border-radius: 3px !important;
    color: #d4b483 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 1rem !important;
}
.stTextArea label { color: #6a5535 !important; font-style: italic; }

.stTextInput input {
    background-color: #141008 !important;
    border: 1px solid #3a2a15 !important;
    color: #d4b483 !important;
    font-family: 'Playfair Display', serif !important;
}

.stButton > button {
    background-color: transparent !important;
    border: 1px solid #7a6030 !important;
    color: #c8a96e !important;
    font-family: 'Special Elite', cursive !important;
    letter-spacing: 3px;
    font-size: 0.85rem;
    padding: 0.5rem 1.2rem;
    transition: all 0.3s ease;
    border-radius: 2px;
}
.stButton > button:hover {
    background-color: rgba(200,169,110,0.08) !important;
    border-color: #c8a96e !important;
    color: #e8c980 !important;
}
[data-testid="stDownloadButton"] > button {
    border-color: #4a3820 !important;
    color: #8a6840 !important;
    font-size: 0.78rem;
    letter-spacing: 1px;
    padding: 0.3rem 0.8rem;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: #7a6030 !important;
    color: #c8a96e !important;
}
[data-testid="stMetric"] {
    background-color: #141008;
    border: 1px solid #2a2010;
    border-radius: 3px;
    padding: 12px;
}
[data-testid="stMetricLabel"] { color: #6a5535 !important; font-style: italic; }
[data-testid="stMetricValue"] { color: #c8a96e !important; font-family: 'Special Elite', cursive !important; }

.door-card {
    border-radius: 3px;
    padding: 22px 26px;
    margin: 4px 0 8px 0;
    border-left: 3px solid;
    opacity: 0;
    animation: doorReveal 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
@keyframes doorReveal {
    from { opacity: 0; transform: translateX(-14px); }
    to   { opacity: 1; transform: translateX(0); }
}
.door-card-0 { animation-delay: 0.15s; }
.door-card-1 { animation-delay: 0.45s; }
.door-card-2 { animation-delay: 0.75s; }
.door-card-3 { animation-delay: 1.05s; }
.door-card h3 {
    font-family: 'Special Elite', cursive !important;
    font-size: 1.15rem;
    margin-bottom: 10px;
    letter-spacing: 1px;
}
.door-card .reason-text {
    font-style: italic;
    color: #a08850;
    margin-bottom: 14px;
    line-height: 1.75;
    font-size: 0.97rem;
}
.door-card .poem-block {
    border-left: 2px solid;
    padding-left: 16px;
    margin: 14px 0 4px 0;
    line-height: 2.1;
    font-style: italic;
    font-size: 1rem;
}

.historical-echo {
    background-color: #0e0c08;
    border: 1px solid #2a2010;
    border-left: 3px solid #5a4020;
    border-radius: 3px;
    padding: 16px 22px;
    margin: 18px 0;
}
.echo-label {
    font-family: 'Special Elite', cursive;
    color: #5a4020;
    font-size: 0.75rem;
    letter-spacing: 3px;
    margin-bottom: 10px;
}
.echo-text {
    font-style: italic;
    color: #7a6040;
    line-height: 1.8;
    font-size: 0.95rem;
}

.fifth-door-header {
    background-color: #100d08;
    border: 1px dashed #3a2a18;
    border-radius: 3px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.fifth-door-header h3 { color: #9060c0 !important; }
.fifth-door-header p { color: #6a5040; font-style: italic; font-size: 0.93rem; }

/* ses player'ını gizle */
[data-testid="stAudio"] { display: none !important; }

.selected-door-label {
    font-family: 'Special Elite', cursive;
    font-size: 1.2rem;
    color: #c8a96e;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

@keyframes swingLeft {
    0%   { transform: perspective(1400px) rotateY(0deg);   opacity: 1; }
    78%  { transform: perspective(1400px) rotateY(-87deg); opacity: 1; }
    100% { transform: perspective(1400px) rotateY(-90deg); opacity: 0; }
}
@keyframes swingRight {
    0%   { transform: perspective(1400px) rotateY(0deg);  opacity: 1; }
    78%  { transform: perspective(1400px) rotateY(87deg); opacity: 1; }
    100% { transform: perspective(1400px) rotateY(90deg); opacity: 0; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── DOOR ANIMATION HTML ──────────────────────────────────────────────────────────
DOOR_ANIM_HTML = """
<div id="knock-door-overlay" style="
    position:fixed; top:0; left:0;
    width:100vw; height:100vh;
    display:flex; z-index:9999;
    pointer-events:none;
">
  <div style="
    width:50%; height:100%;
    background: linear-gradient(to left, #2a1c00, #0d0b07);
    transform-origin: left center;
    animation: swingLeft 1.9s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  "></div>
  <div style="
    width:50%; height:100%;
    background: linear-gradient(to right, #2a1c00, #0d0b07);
    transform-origin: right center;
    animation: swingRight 1.9s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  "></div>
</div>
"""

def inject_door_sound(door_title, key=0):
    sound_bytes, mime = generate_door_sound(door_title)
    b64 = base64.b64encode(sound_bytes).decode()
    st.markdown(
        f'<audio id="door-snd-{key}" autoplay style="display:none">'
        f'<source src="data:{mime};base64,{b64}" type="{mime}">'
        f'</audio>',
        unsafe_allow_html=True,
    )

# ── HEADER ───────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="knock-title">K N O C K</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="knock-subtitle">'
    '"Mama, take this badge off of me, I can\'t use it anymore"'
    ' &nbsp;—&nbsp; Bob Dylan, 1973'
    '</p>',
    unsafe_allow_html=True,
)
st.divider()

# ── INPUT ─────────────────────────────────────────────────────────────────────────
user_text = st.text_area(
    "Tell me about a threshold moment in your life...",
    placeholder="e.g. I am leaving my country to start a new life abroad. I feel like I am losing everything I know.",
    height=130,
)

if st.button("⟡  Find My Door", type="primary"):
    if not user_text.strip():
        st.warning("Please write something first.")
    else:
        with st.spinner("Analyzing your emotions..."):
            emotions = get_top_emotions(user_text, top_n=3)
            all_emotions = analyze_emotion(user_text)
            st.session_state.emotions = emotions
            st.session_state.all_emotions = all_emotions
            st.session_state.user_text = user_text

        with st.spinner("Searching the archive of 1973..."):
            rag_echo = get_context(user_text, k=1)
            st.session_state.rag_echo = rag_echo

        with st.spinner("Consulting the spirit of the threshold..."):
            raw_output = generate_doors(user_text, emotions)
            st.session_state.raw_output = raw_output
            st.session_state.selected_door = None
            st.session_state.selected_poem = []
            st.session_state.door_image = None
            st.session_state.custom_door_output = None
            st.session_state.show_door_anim = False
            st.session_state.play_door_sound = None

# ── EMOTION RESULTS ───────────────────────────────────────────────────────────────
if "all_emotions" in st.session_state:
    st.subheader("🎭 Emotions detected")

    cols = st.columns(3)
    top3 = sorted(st.session_state.all_emotions.items(), key=lambda x: x[1], reverse=True)[:3]
    top3_total = sum(s for _, s in top3) or 1
    for i, (emotion, score) in enumerate(top3):
        cols[i].metric(emotion.capitalize(), f"{score / top3_total * 100:.0f}%")

    MEANINGFUL_EMOTIONS = {
        "sadness", "joy", "anger", "fear", "love", "surprise",
        "disappointment", "grief", "nervousness", "remorse",
        "optimism", "desire", "relief", "excitement", "annoyance",
    }
    sorted_emotions = sorted(
        [(e, s) for e, s in st.session_state.all_emotions.items() if e in MEANINGFUL_EMOTIONS],
        key=lambda x: x[1],
        reverse=True,
    )
    df = pd.DataFrame(sorted_emotions, columns=["Emotion", "Score"])
    df["Score"] = (df["Score"] * 100).round(1)
    st.bar_chart(df.set_index("Emotion")["Score"], color="#c8a96e")

    # ── RAG HISTORICAL ECHO ───────────────────────────────────────────────────────
    if st.session_state.get("rag_echo"):
        echo_text = st.session_state.rag_echo
        st.markdown(
            f'<div class="historical-echo">'
            f'<div class="echo-label">📜 &nbsp; T H E &nbsp; A R C H I V E &nbsp; S P E A K S</div>'
            f'<div class="echo-text">{echo_text}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.subheader("🚪 Your Four Doors")

    # ── DOOR CARDS ────────────────────────────────────────────────────────────────
    doors = re.split(r"---+", st.session_state.raw_output)
    doors = [d.strip() for d in doors if d.strip()]

    # Animasyon slot'u: for loop'tan once tanimla, buton click'inde direkt doldurulacak
    anim_slot = st.empty()

    for i, door_text in enumerate(doors):
        door_title, reason_text, poem_lines = parse_door(door_text)
        cfg = get_door_config(door_title)
        poem_html = "<br>".join(poem_lines)
        color = cfg["color"]
        bg = cfg["bg"]
        emoji = cfg["emoji"]

        st.markdown(
            f'<div class="door-card door-card-{i}" style="border-left-color:{color};background-color:{bg};">'
            f'<h3 style="color:{color}">{emoji}&nbsp; {door_title}</h3>'
            f'<p class="reason-text">{reason_text}</p>'
            f'<div class="poem-block" style="border-left-color:{color}55;color:{color};">{poem_html}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        col_gap, col_card, col_choose = st.columns([3, 1, 1])
        with col_card:
            if poem_lines:
                card_img = create_poem_card(door_title, poem_lines)
                buf = BytesIO()
                card_img.save(buf, format="PNG")
                buf.seek(0)
                st.download_button(
                    label="🎨 Poem card",
                    data=buf,
                    file_name=f"{door_title.replace(' ', '_')}_poem.png",
                    mime="image/png",
                    key=f"download_{i}",
                )
        with col_choose:
            if st.button("🚪 Choose", key=f"door_{i}"):
                st.session_state.selected_door = door_title
                st.session_state.selected_poem = poem_lines
                st.session_state.door_image = None
                st.session_state.custom_door_output = None
                new_key = st.session_state.get("door_anim_key", 0) + 1
                st.session_state.door_anim_key = new_key
                _snd_bytes, _snd_mime = generate_door_sound(door_title)
                st.session_state.door_sound_bytes = _snd_bytes
                st.session_state.door_sound_mime  = _snd_mime
                # Animasyon + ses + scroll — image generation'dan once tetikle
                _anim = DOOR_ANIM_HTML.replace(
                    'id="knock-door-overlay"',
                    f'id="knock-door-overlay-{new_key}"'
                )
                _b64snd = base64.b64encode(_snd_bytes).decode()
                _audio = (
                    f'<audio id="ks-{new_key}" autoplay style="display:none">'
                    f'<source src="data:{_snd_mime};base64,{_b64snd}" type="{_snd_mime}">'
                    '</audio>'
                )
                _scroll = (
                    '<img src="x" onerror="setTimeout(function(){'
                    'var p=window.parent;'
                    'p.scrollTo({top:99999,behavior:\'smooth\'});'
                    'var els=[\'[data-testid=\\u0022stAppViewContainer\\u0022]\','
                    '\'[data-testid=\\u0022stMain\\u0022]\',\'.main\'];'
                    'for(var i=0;i<els.length;i++){'
                    'var el=p.document.querySelector(els[i]);'
                    'if(el){el.scrollTo({top:99999,behavior:\'smooth\'});break;}'
                    '}},2200)">'
                )
                anim_slot.markdown(_anim + _audio + _scroll, unsafe_allow_html=True)
                st.session_state.show_door_anim = False

# ── SELECTED DOOR — ANİMASYON + SES + GÖRSEL ─────────────────────────────────────
if st.session_state.get("selected_door"):
    st.divider()

    label = st.session_state.selected_door
    st.markdown(
        f'<div class="selected-door-label">✦ &nbsp; {label}</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.get("door_image") is None:
        with st.spinner("Generating your door's vision..."):
            img = generate_door_image(st.session_state.selected_door)
            if img:
                img = overlay_poem_on_image(img, st.session_state.get("selected_poem", []))
            st.session_state.door_image = img

    if st.session_state.door_image:
        col_img, col_spacer = st.columns([2, 1])
        with col_img:
            st.image(st.session_state.door_image, use_container_width=True)
            buf = BytesIO()
            st.session_state.door_image.save(buf, format="PNG")
            buf.seek(0)
            fname = st.session_state.selected_door.replace(" ", "_") + "_vision.png"
            st.download_button(
                "⬇  Download Vision",
                data=buf,
                file_name=fname,
                mime="image/png",
                key="download_vision",
            )



# ── 5TH DOOR ─────────────────────────────────────────────────────────────────────
if "emotions" in st.session_state:
    st.divider()
    st.markdown(
        '<div class="fifth-door-header">'
        '<h3>✦ &nbsp; The Fifth Door: Yours to Name</h3>'
        '<p>None of the four doors feel quite like yours? '
        'Describe the threshold you are actually standing at — in your own words. '
        'The system will name your door and write its poem.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    custom_concept = st.text_input(
        "Your door",
        placeholder="e.g. The door of becoming a parent for the first time...",
        key="custom_door_input",
        label_visibility="collapsed",
    )

    if st.button("✦  Create My Own Door", key="custom_door_btn"):
        if custom_concept.strip():
            with st.spinner("Crafting your door..."):
                result = generate_custom_door(
                    st.session_state.user_text,
                    st.session_state.emotions,
                    custom_concept,
                )
                st.session_state.custom_door_output = result
        else:
            st.warning("Describe your door first.")

    if st.session_state.get("custom_door_output"):
        door_title, reason_text, poem_lines = parse_door(st.session_state.custom_door_output)
        poem_html = "<br>".join(poem_lines)
        st.markdown(
            '<div class="door-card" style="border-left-color:#9060c0;background-color:#100a18;animation-delay:0s;">'
            f'<h3 style="color:#9060c0">✦ &nbsp; {door_title}</h3>'
            f'<div class="poem-block" style="border-left-color:rgba(144,96,192,0.35);color:#b080c0;">{poem_html}</div>'
            '</div>',
            unsafe_allow_html=True,
        )
