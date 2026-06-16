 # Tamil AI Learning Assistant

## Live Demo
[Paste your Streamlit Cloud URL here]

## Overview
Tamil AI Learning Assistant is an AI-powered platform that helps users learn Tamil through translation, dialogue generation, grammar assistance, and interactive AI conversations.

## Technologies Used
- Python
- Streamlit
- Google Gemini API

## Run Locally

1. Install requirements:
pip install -r requirements.txt

2. Create .streamlit/secrets.toml

3. Add:
GEMINI_API_KEY = "YOUR_API_KEY"

4. Run:
streamlit run app.py
[10:48 am, 16/06/2026] Rohini: # 🪔 Tamil AI — Learning Assistant

An AI-powered Tamil language learning web application built with Streamlit and Google Gemini AI. Designed to help students and learners master the Tamil language through six intelligent tools.

---

## 🌐 Live Demo

🔗 [Click here to try the app](https://tamil-ai-hackathon.streamlit.app)

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 📝 Sentence Generator | Enter any word and get 5 authentic Tamil sentences |
| 💬 Dialogue Generator | Describe a situation and get a natural Tamil conversation |
| 🔤 Grammar Builder | Build Tamil sentences in any tense from a root word |
| 📄 Essay Generator | Get a full 300-word Tamil essay with intro, body and conclusion |
| 🤖 Tamil Chatbot | Ask grammar doubts, word meanings or practice Tamil conversation |
| 🔍 Grammar Explanation | Paste any Tamil sentence and get a full English grammar breakdown |

---

## 🛠️ Tech Stack

- *Frontend* — Streamlit (Python)
- *AI Model* — Google Gemini 2.5 Flash API
- *Text to Speech* — Web Speech API (Tamil voice ta-IN)
- *Deployment* — Streamlit Cloud

---

## 📱 Device Support

- ✅ Laptop / Desktop
- ✅ Mobile (responsive UI)
- ✅ Tablet

---

## 🚀 How to Run Locally

### 1. Clone the repository
bash
git clone https://github.com/rohinisenthilkumar1278/tamil-ai-hackathon.git
cd tamil-ai-hackathon


### 2. Install dependencies
bash
pip install -r requirements.txt


### 3. Add your Gemini API key

Create a file at .streamlit/secrets.toml:
toml
GEMINI_KEY_1 = "your_gemini_api_key_here"
GEMINI_KEY_2 = "your_gemini_api_key_here"
GEMINI_KEY_3 = "your_gemini_api_key_here"


Get your free API key at [aistudio.google.com](https://aistudio.google.com)

### 4. Run the app
bash
streamlit run app.py


Open your browser at http://localhost:8501

---

## 📦 Requirements


streamlit
google-generativeai


---

## 📁 Project Structure


tamil-ai-hackathon/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .streamlit/
    └── secrets.toml    # API keys (not pushed to GitHub)


---

## 🔑 API Key Setup

This app uses *Google Gemini API* (free tier).
- Free tier: 500 requests/day per key
- App uses 3 API keys with rotation for higher availability
- Get your free key at [aistudio.google.com](https://aistudio.google.com)

---

## 🎯 Hackathon

- *Event* — DTEC Hackathon 2026
- *Category* — Learning
- *Team* — Rohini S

---

## 👩‍💻 Developer

*Rohini S*
B.Tech Information Technology
Chettinad College of Engineering and Technology, Karur