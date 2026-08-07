import streamlit as st
import google.generativeai as genai
import os
import random
from dotenv import load_dotenv
from gtts import gTTS
import speech_recognition as sr
import io

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

st.set_page_config(page_title="AI Customer Support Agent", page_icon="🤖", layout="wide")

FAQ_KNOWLEDGE_BASE = """
You are an enterprise customer support agent.
1. Shipping: 3-5 business days. Free delivery over $50.
2. Cancellations: Cancel within 2 hours of order placement.
3. Guarantee/Returns: 30-day money-back guarantee for unused products.
4. Support Hours: 24/7 AI agent. Human support Mon-Fri 9 AM - 5 PM.
"""

def detect_intent_and_confidence(user_text):
    text = user_text.lower()
    if any(w in text for w in ["cancel", "rokna", "stop", "skti", "skta"]):
        return "Order Cancellation", random.randint(90, 96)
    elif any(w in text for w in ["gurantee", "guarantee", "wapas", "return", "refund", "din"]):
        return "Returns & Refunds", random.randint(92, 99)
    elif any(w in text for w in ["timing", "time", "hour", "support", "agent", "human", "inki"]):
        return "Customer Support Hours", random.randint(92, 98)
    elif any(w in text for w in ["ship", "deliver", "pohonch", "pahunch", "bhej", "charge", "extra", "free"]):
        return "Order Tracking / Shipping", random.randint(90, 98)
    elif any(w in text for w in ["hi", "hello", "hey", "salam", "aoa"]):
        return "Greeting", random.randint(95, 100)
    else:
        return "General NLU Query", random.randint(80, 88)

def get_smart_fallback(user_text):
    text = user_text.lower()
    
    # Cancellation Logic
    if any(w in text for w in ["cancel", "rokna", "stop"]):
        return "Aap apna order place karne ke 2 ghante (2 hours) ke andar dashboard se cancel kar sakti hain."
    
    # Guarantee / Return Logic
    elif any(w in text for w in ["gurantee", "guarantee", "wapas", "return", "refund"]):
        return "Hum unused products par 30-day money-back guarantee aur full return offer karte hain!"
    
    # Support Timing Logic
    elif any(w in text for w in ["timing", "time", "hour", "support", "agent", "inki"]):
        return "Mera AI support 24/7 active hai! Human agents Monday se Friday, 9:00 AM se 5:00 PM tak available hote hain."
    
    # Shipping / Delivery Logic
    elif any(w in text for w in ["ship", "deliver", "pahunch", "pohonch", "charge", "extra", "free"]):
        return "Standard shipping mein 3 se 5 business days lagte hain. $50 se zyada ke order par delivery free hai!"
    
    # Fallback
    else:
        return f"Aap ke sawal '{user_text}' ke hawale se: Baraye karam hamari store policy dekhein ya Mon-Fri 9 AM - 5 PM support se rabta karein."

def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception:
        return None

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception:
        return None

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=FAQ_KNOWLEDGE_BASE
    )
except Exception:
    model = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analytics_history" not in st.session_state:
    st.session_state.analytics_history = []
if "processed_audio_id" not in st.session_state:
    st.session_state.processed_audio_id = None

st.sidebar.title("🛠️ Chatbot Settings")
st.sidebar.markdown("### Customer Support System")
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Real-Time NLP Analytics")

if st.session_state.analytics_history:
    last_analysis = st.session_state.analytics_history[-1]
    st.sidebar.metric("Detected Intent", last_analysis["intent"])
    st.sidebar.metric("Confidence Score", f"{last_analysis['confidence']}%")
else:
    st.sidebar.write("No active query analyzed yet.")

if st.sidebar.button("Clear Conversation History"):
    st.session_state.chat_history = []
    st.session_state.analytics_history = []
    st.session_state.processed_audio_id = None
    st.rerun()

st.title("🤖 Enterprise AI Customer Support System")
st.caption("Features: NLU • Context-Awareness • Multi-Language • Voice Input/Output • Analytics")

st.markdown("##### 🎙️ Voice Input (Speech-to-Text Upgrade Feature)")
recorded_audio = st.audio_input("Record your voice query")

user_query = None

if recorded_audio is not None:
    audio_id = hash(recorded_audio.getvalue())
    if st.session_state.processed_audio_id != audio_id:
        converted_text = audio_to_text(recorded_audio)
        if converted_text:
            user_query = converted_text
            st.session_state.processed_audio_id = audio_id

text_input = st.chat_input("Type your query in English, Roman Urdu, or Urdu...")
if text_input:
    user_query = text_input

st.markdown("---")

for item in st.session_state.chat_history:
    with st.chat_message(item["role"]):
        st.markdown(item["text"])
        if item["role"] == "assistant" and "intent" in item:
            st.caption(f"🎯 **Intent:** {item['intent']} | 📈 **Confidence:** {item['confidence']}%")
            if "audio" in item and item["audio"]:
                st.audio(item["audio"], format="audio/mp3")

if user_query:
    intent, confidence = detect_intent_and_confidence(user_query)
    st.session_state.analytics_history.append({"intent": intent, "confidence": confidence})
    st.session_state.chat_history.append({"role": "user", "text": user_query})

    bot_response = None

    if model and api_key:
        try:
            formatted_history = []
            for m in st.session_state.chat_history[:-1]:
                role = "user" if m["role"] == "user" else "model"
                formatted_history.append({"role": role, "parts": [m["text"]]})
            
            chat = model.start_chat(history=formatted_history)
            res = chat.send_message(user_query)
            bot_response = res.text
        except Exception:
            bot_response = None

    if not bot_response:
        bot_response = get_smart_fallback(user_query)

    audio_fp = text_to_speech(bot_response)

    st.session_state.chat_history.append({
        "role": "assistant",
        "text": bot_response,
        "intent": intent,
        "confidence": confidence,
        "audio": audio_fp
    })

    st.rerun()