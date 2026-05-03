import streamlit as st
from emotion import get_top_emotions, analyze_emotion
from llm import generate_doors
from image_gen import generate_door_image
import re

st.set_page_config(page_title="Which Door Are You Knocking On?", page_icon="🚪", layout="wide")

st.title("🚪 Which Door Are You Knocking On?")
st.markdown("*Inspired by Bob Dylan's 'Knockin' on Heaven's Door' (1973)*")
st.divider()

user_text = st.text_area(
    "Tell me about a threshold moment in your life...",
    placeholder="e.g. I am leaving my country to start a new life abroad...",
    height=120
)

if st.button("Find My Door", type="primary"):
    if not user_text.strip():
        st.warning("Please write something first.")
    else:
        with st.spinner("Analyzing your emotions..."):
            emotions = get_top_emotions(user_text, top_n=3)
            all_emotions = analyze_emotion(user_text)
            st.session_state.emotions = emotions
            st.session_state.all_emotions = all_emotions

        with st.spinner("Consulting the spirit of 1973..."):
            raw_output = generate_doors(user_text, emotions)
            st.session_state.raw_output = raw_output
            st.session_state.selected_door = None
            st.session_state.door_image = None

if "all_emotions" in st.session_state:
    st.subheader("🎭 Emotions detected:")

    # Metric kutucukları
    cols = st.columns(3)
    for i, (emotion, score) in enumerate(
            sorted(st.session_state.all_emotions.items(), key=lambda x: x[1], reverse=True)[:3]
    ):
        cols[i].metric(emotion.capitalize(), f"{score * 100:.0f}%")

    # Bar chart
    import pandas as pd

    emotion_colors = {
        "sadness": "#6B8CAE",
        "joy": "#F4C542",
        "anger": "#E05C5C",
        "fear": "#9B72CF",
        "love": "#E87EA1",
        "surprise": "#5CB85C"
    }

    sorted_emotions = sorted(
        st.session_state.all_emotions.items(),
        key=lambda x: x[1],
        reverse=True
    )

    MEANINGFUL_EMOTIONS = {
        "sadness", "joy", "anger", "fear", "love", "surprise",
        "disappointment", "grief", "nervousness", "remorse",
        "optimism", "desire", "relief", "excitement", "annoyance"
    }
    sorted_emotions = [(e, s) for e, s in sorted_emotions if e in MEANINGFUL_EMOTIONS]
    df = pd.DataFrame(sorted_emotions, columns=["Emotion", "Score"])
    df["Score"] = (df["Score"] * 100).round(1)
    df["Color"] = df["Emotion"].map(emotion_colors).fillna("#888888")

    st.bar_chart(df.set_index("Emotion")["Score"], color="#6B8CAE")

    st.divider()
    st.subheader("🚪 Your Four Doors:")

    doors = re.split(r"---+", st.session_state.raw_output)
    doors = [d.strip() for d in doors if d.strip()]

    for i, door_text in enumerate(doors):
        door_title = ""
        for line in door_text.strip().split("\n"):
            if line.startswith("DOOR:"):
                door_title = line.replace("DOOR:", "").strip()
                break

        with st.expander(f"Door {i+1}: {door_title}", expanded=True):
            st.markdown(door_text.replace("DOOR:", "**DOOR:**").replace("REASON:", "**REASON:**").replace("POEM:", "**POEM:**"))
            if st.button(f"🚪 Choose this door", key=f"door_{i}"):
                st.session_state.selected_door = door_title
                # Şiiri çıkar ve indir butonu ekle
                poem_lines = []
                in_poem = False
                for line in door_text.strip().split("\n"):
                    if line.startswith("POEM:"):
                        in_poem = True
                        continue
                    if in_poem and line.strip():
                        poem_lines.append(line.strip())

                if poem_lines:
                    from poem_card import create_poem_card
                    from io import BytesIO

                    card = create_poem_card(door_title, poem_lines)
                    buf = BytesIO()
                    card.save(buf, format="PNG")
                    buf.seek(0)

                    st.download_button(
                        label="🎨 Download Poem Card",
                        data=buf,
                        file_name=f"{door_title.replace(' ', '_')}_poem.png",
                        mime="image/png",
                        key=f"download_{i}"
                    )

if st.session_state.get("selected_door"):
    st.divider()
    st.subheader(f"✨ You chose: {st.session_state.selected_door}")
    if st.session_state.get("door_image") is None:
        with st.spinner("Generating your door's vision..."):
            img = generate_door_image(st.session_state.selected_door)
            st.session_state.door_image = img
    st.image(st.session_state.door_image, width=400)