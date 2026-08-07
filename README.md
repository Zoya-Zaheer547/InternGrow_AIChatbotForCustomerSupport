# Enterprise AI Chatbot for Customer Support 🤖

An intelligent, context-aware customer support chatbot built using Streamlit and Google Gemini LLM API. This project features NLU, multi-turn conversation handling, real-time analytics, and voice integration.

## 🌟 Features
* **Natural Language Understanding (NLU):** Handles queries in English, Urdu, and Roman Urdu.
* **Context-Aware Responses:** Remembers conversation history for natural follow-ups.
* **Real-Time Analytics:** Displays detected intent and confidence score dynamically in the sidebar.
* **Voice Capabilities:** Includes Speech-to-Text input and Text-to-Speech audio generation.
* **Smart Fallback Mechanism:** Ensures instant answers even if API calls encounter limits.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **AI Model:** Google Gemini API (gemini-1.5-flash)
* **Speech Processing:** gTTS (Text-to-Speech), SpeechRecognition (Speech-to-Text)
* **Language:** Python 3.10+

## 🚀 Setup Instructions

1. **Clone the Repository:**
   git clone https://github.com/Zoya-Zaheer547/InternGrow_AIChatbotForCustomerSupport.git
   cd InternGrow_AIChatbotForCustomerSupport

2. **Install Dependencies:**
   pip install -r requirements.txt

3. **Configure Environment Variables:**
   Create a .env file in the root directory and add your API key:
   GEMINI_API_KEY=your_actual_api_key_here

4. **Run the Application:**
   streamlit run app.py