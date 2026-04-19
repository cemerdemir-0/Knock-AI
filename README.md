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
| Emotion Analysis (NLP) | HuggingFace `distilbert-base-uncased-emotion` | Detects dominant emotions in user text |
| Retrieval-Augmented Generation (RAG) | ChromaDB + Gemini Embeddings | Retrieves relevant historical context from documents |
| Large Language Model (LLM) | Google Gemini 2.5 Flash Lite | Generates door matches and Dylan-style poems |
| Image Generation | Stability AI SDXL 1.0 | Generates a visual for the chosen door |

These techniques are deeply interwoven:  
`NLP output → enriches RAG query → context fed to LLM → LLM output triggers image generation`

---

## 🏗️ Architecture