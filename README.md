# ✈️ TravelMind AI — Intelligent Travel Concierge

A conversational AI travel assistant built with **Gemini 1.5 Flash**, **LangChain-style tool calling**, **SQLite**, and **Streamlit**.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_DEPLOYED_URL_HERE)

---

## 🎯 Features

| Feature | Details |
|---|---|
| 🤖 AI Agent | Gemini 1.5 Flash with travel-specialized system prompt |
| 🛠️ Tools | Live weather lookup (OpenWeatherMap API) |
| 💾 Database | SQLite — persists every search query |
| 💬 Multi-turn Chat | Full conversation history with context window |
| 🎨 UI | Streamlit with custom dark travel-theme CSS |
| 🚀 Deployment | Streamlit Cloud |

---

## 🗂️ Project Structure

```
travel_ai/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignored files
└── README.md            # This file
```

---

## 🏗️ Architecture

```
User Input (Streamlit UI)
        │
        ▼
  Context Builder
  (chat history + query)
        │
        ▼
  Weather Tool (if city detected)
  OpenWeatherMap API → real-time data
        │
        ▼
  Gemini 1.5 Flash (LLM)
  System prompt: travel expert persona
        │
        ▼
  Response displayed in chat bubble
        │
        ▼
  SQLite DB → query saved for history
```

---

## 🚀 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/travel-ai-agent.git
cd travel-ai-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```
Get a free key: https://aistudio.google.com/app/apikey

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🌐 Deployment (Streamlit Cloud)

1. Push repo to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. Set secrets: `GEMINI_API_KEY = "your_key"`
5. Deploy!

---

## 💡 Sample Queries

- "Plan a 5-day trip to Goa under ₹15,000"
- "What documents do I need for a Dubai visa from India?"
- "Best time to visit Japan for cherry blossoms"
- "Hidden gems in Southeast Asia for backpackers"
- "Budget itinerary for Europe — 3 weeks, ₹2 lakhs"

---

## 📊 Assessment Checklist (Track A)

- [x] **Core Functionality (40pts)** — AI agent with Gemini + weather tool + SQLite DB
- [x] **User Interface (20pts)** — Custom-themed Streamlit with chat bubbles, cards, sidebar
- [x] **Deployment (15pts)** — Deployed on Streamlit Cloud
- [x] **Documentation (15pts)** — This README + setup instructions
- [x] **Presentation (10pts)** — Demo video

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit + Custom CSS
- **LLM:** Google Gemini 1.5 Flash (free tier)
- **Framework:** google-generativeai SDK
- **Database:** SQLite (built into Python)
- **Tool:** OpenWeatherMap REST API
- **Deployment:** Streamlit Cloud

---

## 👨‍💻 Built By

**[Your Name]** — BTech CSM | AI/ML Enthusiast  
GitHub: [Sampath7890](https://github.com/Sampath7890)

---

## 🔮 Future Improvements

- [ ] Flight search via Skyscanner API
- [ ] Hotel booking with Booking.com API
- [ ] PDF itinerary export
- [ ] Voice input with Whisper API
- [ ] Multi-language support (Telugu, Hindi)
# travel_ai
 
