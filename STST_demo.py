'''import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile
import base64
from PIL import Image
import numpy as np
import plotly.express as px
import pandas as pd
import io

# Set up Streamlit page configuration
st.set_page_config(
    page_title="VoiceTranslate",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS styles
def local_css():
    st.markdown("""
    <style>
        .main { background-color: #f5f7f9; }
        .stButton button {
            background-color: #007bff; color: white; border-radius: 8px;
            padding: 0.5em 1em; font-weight: 600; border: none;
            transition: all 0.3s;
        }
        .stButton button:hover {
            background-color: #0056b3; box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        .status-box {
            padding: 10px; border-radius: 8px; margin-bottom: 10px;
        }
        .success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .warning { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
        .info { background-color: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .title-container {
            display: flex; align-items: center; margin-bottom: 20px;
        }
        .logo { width: 60px; margin-right: 20px; }
        .title { font-size: 2.5rem; color: #007bff; font-weight: 700; }
        .subtitle { font-size: 1.2rem; color: #6c757d; }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Initialize session state variables
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar settings
with st.sidebar:
    st.markdown("## Settings ⚙️")
    with st.expander("Voice Settings", expanded=True):
        voice_speed = st.slider("Speech Rate", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

    with st.expander("Usage Statistics", expanded=False):
        if st.session_state.history:
            lang_counts = pd.DataFrame(st.session_state.history, columns=['to_lang']).value_counts().reset_index()
            lang_counts.columns = ['Language', 'Count']
            fig = px.pie(lang_counts, values='Count', names='Language', title='Translation Distribution')
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("## About VoiceTranslate 🌐")
    st.markdown("**Break language barriers with real-time speech translation.**")

# Main UI
st.markdown('<div class="title-container"><h1 class="title">VoiceTranslate</h1><p class="subtitle">Speak, Translate, Listen</p></div>', unsafe_allow_html=True)

# Language selection
col1, col2 = st.columns(2)
LANGUAGE_OPTIONS = {'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de', 'Hindi': 'hi', 'Chinese': 'zh-CN'}
from_lang = col1.selectbox("Select Input Language", options=list(LANGUAGE_OPTIONS.keys()), index=0)
to_lang = col2.selectbox("Select Output Language", options=list(LANGUAGE_OPTIONS.keys()), index=1)

# Speech-to-Text function
def recognize_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for background noise
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language=LANGUAGE_OPTIONS[from_lang])
            return text
    except sr.UnknownValueError:
        st.warning("Speech not understood, please try again.")
        return None
    except sr.RequestError as e:
        st.error(f"API unavailable: {e}")
        return None
    except Exception as e:
        st.error(f"Error during speech recognition: {e}")
        return None

# Translate function using deep_translator
def translate_text(text, target_language):
    try:
        translated = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translated
    except Exception as e:
        st.error(f"Translation error: {e}")
        return None

# Text-to-Speech function
def text_to_speech(text, lang_code, speed):
    try:
        tts = gTTS(text=text, lang=lang_code, slow=(speed < 1.0))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            return temp_audio.name
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None

# UI for speech recognition
st.markdown("### 🎤 Speak & Translate")
if st.button("Start Listening 🎙️"):
    original_text = recognize_speech()
    if original_text:
        st.success(f"Recognized Text: {original_text}")

        # Translation
        translated_text = translate_text(original_text, LANGUAGE_OPTIONS[to_lang])
        if translated_text:
            st.info(f"Translated: {translated_text}")

            # Store history
            st.session_state.history.append({'from_lang': from_lang, 'to_lang': to_lang, 'text': original_text, 'translated': translated_text})

            # Text-to-Speech
            audio_file = text_to_speech(translated_text, LANGUAGE_OPTIONS[to_lang], voice_speed)
            if audio_file:
                st.audio(audio_file, format="audio/mp3")
        else:
            st.error("Translation failed. Please try again.")
    else:
        st.warning("No speech detected or recognition failed. Please try again.")

# Display Translation History
st.markdown("### 📜 Translation History")
if st.session_state.history:
    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"""
        **From {item['from_lang']} to {item['to_lang']}**  
        🎙️ *{item['text']}*  
        🔄 **{item['translated']}**  
        """, unsafe_allow_html=True)
else:
    st.info("No history yet. Speak something!")

# Footer
st.markdown("---")
st.markdown('<div class="footer">Made with ❤️ by AI Josh Team</div>', unsafe_allow_html=True)
'''
import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile
import base64
from PIL import Image
import numpy as np
import plotly.express as px
import pandas as pd
import io
import time
import threading

# Set up Streamlit page configuration
st.set_page_config(
    page_title="VoiceTranslate Pro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS styles
def local_css():
    st.markdown("""
    <style>
        .main { background-color: #f5f7f9; }
        .stButton button {
            background-color: #007bff; color: white; border-radius: 8px;
            padding: 0.5em 1em; font-weight: 600; border: none;
            transition: all 0.3s;
        }
        .stButton button:hover {
            background-color: #0056b3; box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        .status-box {
            padding: 10px; border-radius: 8px; margin-bottom: 10px;
        }
        .success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .warning { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
        .info { background-color: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .title-container {
            display: flex; align-items: center; margin-bottom: 20px;
        }
        .logo { width: 60px; margin-right: 20px; }
        .title { font-size: 2.5rem; color: #007bff; font-weight: 700; }
        .subtitle { font-size: 1.2rem; color: #6c757d; }
        .progress-bar-container {
            width: 100%;
            background-color: #e9ecef;
            border-radius: 4px;
            height: 20px;
            margin-top: 10px;
            position: relative;
        }
        .progress-bar {
            height: 100%;
            border-radius: 4px;
            background-color: #4CAF50;
            transition: width 0.1s;
        }
        .progress-text {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            text-align: center;
            line-height: 20px;
            color: white;
            mix-blend-mode: difference;
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Initialize session state variables
if 'history' not in st.session_state:
    st.session_state.history = []
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'stop_recording' not in st.session_state:
    st.session_state.should_stop_recording = False

# Expanded language options
LANGUAGE_OPTIONS = {
    'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de',
    'Hindi': 'hi', 'Chinese': 'zh-CN', 'Tamil': 'ta', 'Arabic': 'ar',
    'Bengali': 'bn', 'Portuguese': 'pt', 'Russian': 'ru', 'Japanese': 'ja',
    'Korean': 'ko', 'Italian': 'it', 'Dutch': 'nl', 'Turkish': 'tr',
    'Polish': 'pl', 'Swedish': 'sv', 'Vietnamese': 'vi', 'Thai': 'th',
    'Indonesian': 'id', 'Greek': 'el', 'Czech': 'cs', 'Danish': 'da',
    'Finnish': 'fi', 'Romanian': 'ro', 'Hungarian': 'hu', 'Norwegian': 'no',
    'Ukrainian': 'uk', 'Hebrew': 'he', 'Croatian': 'hr', 'Bulgarian': 'bg',
    'Lithuanian': 'lt', 'Slovak': 'sk', 'Slovenian': 'sl', 'Estonian': 'et',
    'Latvian': 'lv', 'Serbian': 'sr', 'Malay': 'ms', 'Filipino': 'tl',
    'Urdu': 'ur'
}

# Sidebar settings
with st.sidebar:
    st.markdown("## Settings ⚙️")
    with st.expander("Voice Settings", expanded=True):
        voice_speed = st.slider("Speech Rate", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        max_recording_duration = st.slider("Max Recording Duration (seconds)", min_value=10, max_value=120, value=60, step=10)

    with st.expander("Usage Statistics", expanded=False):
        if st.session_state.history:
            lang_counts = pd.DataFrame(st.session_state.history, columns=['to_lang']).value_counts().reset_index()
            lang_counts.columns = ['Language', 'Count']
            fig = px.pie(lang_counts, values='Count', names='Language', title='Translation Distribution')
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("## About VoiceTranslate Pro 🌐")
    st.markdown("**Break language barriers with real-time speech translation.**")
    st.markdown("* Supports 40+ languages")
    st.markdown("* Extended recording up to 2 minutes")
    st.markdown("* Optimized translation engine")

# Main UI
st.markdown('<div class="title-container"><h1 class="title">VoiceTranslate Pro</h1><p class="subtitle">Speak, Translate, Listen</p></div>', unsafe_allow_html=True)

# Language selection
col1, col2 = st.columns(2)
from_lang = col1.selectbox("Select Input Language", options=list(LANGUAGE_OPTIONS.keys()), index=0)
to_lang = col2.selectbox("Select Output Language", options=list(LANGUAGE_OPTIONS.keys()), index=1)

# Progress display
def display_progress():
    progress_container = st.empty()
    while st.session_state.recording and not st.session_state.stop_recording:
        progress_html = f"""
        <div class="progress-bar-container">
            <div class="progress-bar" style="width: {min(st.session_state.progress, 100)}%"></div>
            <div class="progress-text">{st.session_state.progress:.0f}%</div>
        </div>
        """
        progress_container.markdown(progress_html, unsafe_allow_html=True)
        time.sleep(0.1)

# Speech-to-Text function with longer recording
def recognize_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.session_state.recording = True
            st.session_state.progress = 0
            st.session_state.stop_recording = False
            
            # Start progress bar in background thread
            progress_thread = threading.Thread(target=display_progress)
            progress_thread.start()
            
            st.info("Listening... Speak now! (Recording will automatically stop after the set duration)")
            
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Record for specified duration
            recognizer.pause_threshold = 2.0  # Longer pause threshold for continuous recording
            
            # Set up dynamic energy threshold for better background noise handling
            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 300  # Default energy threshold
            
            # Record audio
            start_time = time.time()
            audio_data = bytearray()
            
            # Keep recording until max_recording_duration is reached
            while (time.time() - start_time) < max_recording_duration and not st.session_state.stop_recording:
                try:
                    # Get audio in chunks
                    chunk = recognizer.listen(source, timeout=1.0, phrase_time_limit=5.0)
                    audio_data.extend(chunk.get_raw_data())
                    
                    # Update progress
                    elapsed = time.time() - start_time
                    st.session_state.progress = (elapsed / max_recording_duration) * 100
                except sr.WaitTimeoutError:
                    # No speech detected in this chunk, continue recording
                    continue
            
            st.session_state.recording = False
            
            # Convert accumulated audio_data to AudioData object
            audio = sr.AudioData(audio_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
            
            # Recognize accumulated speech
            text = recognizer.recognize_google(audio, language=LANGUAGE_OPTIONS[from_lang])
            return text
            
    except sr.UnknownValueError:
        st.warning("Speech not understood, please try again.")
    except sr.RequestError as e:
        st.error(f"API unavailable: {e}")
    except Exception as e:
        st.error(f"Error during speech recognition: {e}")
    finally:
        st.session_state.recording = False
        st.session_state.progress = 0
    return None

# Chunked translation for handling longer texts
def translate_text(text, target_language):
    try:
        if len(text) > 5000:  # If text is very long, chunk it
            chunks = [text[i:i+5000] for i in range(0, len(text), 5000)]
            translated_chunks = []
            
            for i, chunk in enumerate(chunks):
                st.text(f"Translating part {i+1} of {len(chunks)}...")
                translated_chunk = GoogleTranslator(source='auto', target=target_language).translate(chunk)
                translated_chunks.append(translated_chunk)
                
            return ' '.join(translated_chunks)
        else:
            return GoogleTranslator(source='auto', target=target_language).translate(text)
    except Exception as e:
        st.error(f"Translation error: {e}")
        return None

# Text-to-Speech function
def text_to_speech(text, lang_code, speed):
    try:
        tts = gTTS(text=text, lang=lang_code, slow=(speed < 1.0))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            return temp_audio.name
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None

# Stop recording button (visible during recording)
def stop_button():
    st.session_state.stop_button= True
    st.success("Recording stopped!")

# UI for speech recognition
st.markdown("### 🎤 Speak & Translate")
col1, col2 = st.columns([3, 1])
with col1:
    if st.button("Start Listening 🎙️", key="start_listening"):
        if st.session_state.recording:
            st.warning("Already recording! Please wait or stop the current recording.")
        else:
            # Show stop button when recording starts
            stop_placeholder = st.empty()
            with stop_placeholder.container():
                if st.button("Stop button🛑", key="stop_button"):
                    stop_button()
            
            original_text = recognize_speech()
            stop_placeholder.empty()  # Remove stop button
            
            if original_text:
                st.success(f"Recognized Text: {original_text}")

                # Translation
                with st.spinner("Translating..."):
                    translated_text = translate_text(original_text, LANGUAGE_OPTIONS[to_lang])
                
                if translated_text:
                    st.info(f"Translated: {translated_text}")

                    # Store history
                    st.session_state.history.append({
                        'from_lang': from_lang, 
                        'to_lang': to_lang, 
                        'text': original_text, 
                        'translated': translated_text
                    })

                    # Text-to-Speech
                    with st.spinner("Generating audio..."):
                        audio_file = text_to_speech(translated_text, LANGUAGE_OPTIONS[to_lang], voice_speed)
                    
                    if audio_file:
                        st.audio(audio_file, format="audio/mp3")
                else:
                    st.error("Translation failed. Please try again.")
            else:
                st.warning("No speech detected or recognition failed. Please try again.")

# Sidebar for showing stop button during recording
if st.session_state.recording:
    with st.sidebar:
        if st.button("Stop Recording Now 🛑", key="stop_recording_sidebar"):
            stop_button()

# Display Translation History
st.markdown("### 📜 Translation History")
if st.session_state.history:
    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"""
        **From {item['from_lang']} to {item['to_lang']}**  
        🎙️ *{item['text']}*  
        🔄 **{item['translated']}**  
        """, unsafe_allow_html=True)
else:
    st.info("No history yet. Speak something!")

# Footer
st.markdown("---")
st.markdown('<div class="footer">Made with ❤️ by AI Josh Team</div>', unsafe_allow_html=True)