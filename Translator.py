import streamlit as st
from deep_translator import GoogleTranslator
import pyperclip
from gtts import gTTS
import tempfile
import os


# Page configuration
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌐",
    layout="centered"
)


# Title
st.title("🌐 Language Translation Tool")
st.write("Enter text, select languages, and translate instantly.")


# Languages dictionary
languages = {
    "Auto Detect": "auto",
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Korean": "ko",
    "Arabic": "ar",
    "Russian": "ru",
    "Portuguese": "pt"
}


# User input
text = st.text_area(
    "Enter text to translate:",
    height=150,
    placeholder="Type your text here..."
)


# Language selection
col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "Source Language",
        list(languages.keys()),
        index=0
    )

with col2:
    target_language = st.selectbox(
        "Target Language",
        [lang for lang in languages.keys() if lang != "Auto Detect"],
        index=1
    )


# Translate button
if st.button("🌐 Translate", use_container_width=True):

    if text.strip() == "":
        st.warning("⚠️ Please enter some text to translate.")

    else:
        try:
            source_code = languages[source_language]
            target_code = languages[target_language]

            translator = GoogleTranslator(
                source=source_code,
                target=target_code
            )

            translated_text = translator.translate(text)

            # Store translated text
            st.session_state.translated_text = translated_text
            st.session_state.target_code = target_code

            st.success("✅ Translation completed!")

        except Exception as e:
            st.error(f"Translation Error: {e}")


# Display translated text
if "translated_text" in st.session_state:

    st.subheader("Translated Text")

    st.text_area(
        "Result:",
        value=st.session_state.translated_text,
        height=150
    )


    # Copy button
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📋 Copy Text", use_container_width=True):
            try:
                pyperclip.copy(st.session_state.translated_text)
                st.success("Copied to clipboard!")
            except Exception:
                st.error("Could not copy automatically.")


    # Text to Speech
    with col2:
        if st.button("🔊 Text to Speech", use_container_width=True):

            try:
                target_code = st.session_state.target_code

                tts = gTTS(
                    text=st.session_state.translated_text,
                    lang=target_code
                )

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".mp3"
                ) as temp_file:

                    audio_path = temp_file.name

                tts.save(audio_path)

                st.audio(audio_path)

            except Exception as e:
                st.error(f"Text-to-Speech Error: {e}")