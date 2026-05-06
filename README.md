# 🚪 Which Door Are You Knocking On?

> *"Mama, take this badge off of me, I can't use it anymore."*  
> — Bob Dylan, Knockin' on Heaven's Door (1973)

An AI-powered interactive artwork for **CSE 358 Introduction to Artificial Intelligence**.  
Inspired by Bob Dylan's 1973 composition, this project asks: **what door are you knocking on?**

---

## 🎯 Concept

You write about a threshold moment in your life — a farewell, a transition, a loss.  
The system analyzes your emotions, searches historical documents from 1973 and beyond,  
and matches you to one of four symbolic doors. Each door carries its own poem and visual.

The four doors:
- **Billy the Kid's Door** — the outlaw escaping everything
- **The Vietnam Soldier's Door** — returning to a world that moved on
- **Dylan's Door** — the artist turning his back on the system
- **The Survivor's Door** — February 6, 2023, Türkiye. The door that opened without warning.

---

## 🤖 AI Techniques Used

| Technique | Tool | Role |
|---|---|---|
| Emotion Analysis (NLP) | HuggingFace `SamLowe/roberta-base-go_emotions` | Detects dominant emotions in user text |
| Retrieval-Augmented Generation (RAG) | ChromaDB + Gemini Embeddings | Retrieves relevant historical context from documents |
| Large Language Model (LLM) | Google Gemini 2.5 Flash Lite | Generates door matches and Dylan-style poems |
| Image Generation | Stability AI SDXL 1.0 | Generates a visual for the chosen door |

These techniques are deeply interwoven:  
`NLP output → enriches RAG query → context fed to LLM → LLM output triggers image generation`

---

## 🏗️ Architecture

```
User Input (text)
      ↓
[NLP] HuggingFace Emotion Classifier
      → top 3 emotions detected
      ↓
[RAG] ChromaDB Semantic Search
      → retrieves relevant chunks from historical documents
      → Dylan interviews, Vietnam testimonies, February 6 survivor accounts
      ↓
[LLM] Google Gemini
      → receives emotions + historical context
      → generates 4 symbolic doors with poems
      ↓
[User selects a door]
      ↓
[Image Gen] Stability AI SDXL
      → generates a visual representation of the chosen door
```

---

## 📁 Project Structure

```
knock/
├── app.py              # Streamlit web interface
├── emotion.py          # HuggingFace NLP emotion analysis
├── llm.py              # Gemini LLM integration
├── rag.py              # RAG pipeline (ChromaDB + embeddings)
├── image_gen.py        # Stability AI image generation
├── docs/               # Historical documents for RAG
│   ├── dylan_1973.txt
│   ├── vietnam_1973.txt
│   └── february6.txt
├── chroma_db/          # Vector database (auto-generated)
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/cemerdemir-0/Knock-AI.git
cd knock
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key
STABILITY_API_KEY=your_stability_api_key
HF_TOKEN=your_huggingface_token
```

Get your keys from:
- Gemini: [aistudio.google.com](https://aistudio.google.com)
- Stability AI: [platform.stability.ai](https://platform.stability.ai)
- HuggingFace: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 5. Build the vector database
```bash
python rag.py
```

### 6. Run the application
```bash
streamlit run app.py
```

---

## 📦 Dependencies

```
streamlit
google-genai
transformers
torch
requests
python-dotenv
Pillow
langchain
langchain-community
langchain-chroma
langchain-google-genai
langchain-text-splitters
chromadb
```

---

## 🌍 Historical Context

This project is rooted in two historical moments separated by 50 years:

**1973** — The year Dylan wrote the song. Vietnam War's final chapter, the counterculture movement, Pat Garrett & Billy the Kid. A generation standing at the threshold of disillusionment.

**February 6, 2023** — The Kahramanmaraş earthquake. 50,000+ lives lost in southeastern Turkey. A generation standing at a threshold they never chose — life before, and life after.

Both moments ask the same question the song asks: *what do you do when you reach a door you didn't know was there?*

---

## 👤 Author

**Cem Erdemir**  
Computer Science & Engineering, Akdeniz University  
CSE 358 Introduction to Artificial Intelligence — Spring 2025–2026  
GitHub: [@cemerdemir-0](https://github.com/cemerdemir-0)

---

## 📄 Academic Integrity

All AI tools, models, and APIs used in this project are explicitly listed above.  
The creative vision, architectural decisions, and philosophical reflection are the author's own.  
AI was used as a collaborator and material — the meaning was given by the human.
