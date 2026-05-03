# 🚪 KNOCK — Which Door Are You Knocking On?

> *"Mama, take this badge off of me, I can't use it anymore."*  
> — Bob Dylan, Knockin' on Heaven's Door (1973)

An AI-powered interactive artwork for **CSE 358 Introduction to Artificial Intelligence**.  
Inspired by Bob Dylan's 1973 composition, this project asks: **what door are you knocking on?**

---

## 🎯 Concept

You write about a threshold moment in your life — a farewell, a transition, a loss.  
The system analyzes your emotions, searches historical documents from 1973 and beyond,  
and matches you to one of four symbolic doors. Each door carries its own poem and visual.  
You can also name your own fifth door.

The four archetypal doors:
- **Billy the Kid's Door** — the outlaw escaping everything, the myth of absolute freedom
- **The Vietnam Soldier's Door** — returning to a world that moved on, carrying what cannot be named
- **Dylan's Door** — the artist turning his back on the system, refusing to be what others need
- **The Survivor's Door** — February 6, 2023, Türkiye. The door that opened without warning.

---

## 🤖 AI Techniques Used

| Technique | Tool | Role |
|---|---|---|
| **Emotion Analysis (NLP)** | HuggingFace `roberta-base-go_emotions` | Detects dominant emotions in user text — structured classification, not LLM guessing |
| **Retrieval-Augmented Generation (RAG)** | ChromaDB + Gemini Embeddings | Semantic search over historical documents; retrieved context fed to LLM and shown to user |
| **Large Language Model (LLM)** | Google Gemini 2.5 Flash Lite | Generates door matches, Dylan-style poems, and custom 5th door output |
| **Image Generation** | Stability AI SDXL 1.0 | Generates a visual for the chosen door, with poem overlaid |

**How they interlock:**

```
NLP → emotion scores (structured)
  ↓
RAG → semantic search over 1973 docs → historical context (shown to user + fed to LLM)
  ↓
LLM → receives emotions + historical context → generates 4 doors + poems
  ↓
User selects door (or creates a 5th)
  ↓
Image Gen → visual + poem overlay → downloadable artifact
```

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                               │
│              "Tell me about a threshold moment..."              │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │                             │
              ▼                             ▼
┌─────────────────────┐       ┌─────────────────────────────────┐
│   EMOTION ANALYSIS  │       │        RAG PIPELINE             │
│  HuggingFace NLP    │       │  ChromaDB + Gemini Embeddings   │
│                     │       │                                 │
│  roberta-base-      │       │  docs/dylan_1973.txt            │
│  go_emotions        │       │  docs/vietnam_1973.txt          │
│  → 28 emotion labels│       │  docs/february6.txt             │
│  → top 3 returned   │       │  docs/pat_garrett_1973.txt      │
└──────────┬──────────┘       └──────────────┬──────────────────┘
           │                                 │
           │   ┌─────────────────────────────┘
           │   │  historical_context (shown to user as "Archive Speaks")
           ▼   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LLM — Google Gemini 2.5                      │
│                                                                 │
│  Input:  user_text + emotions + historical_context              │
│  Output: 4 symbolic doors × (title + reason + 4-line poem)     │
│                                                                 │
│  Also: generate_custom_door() for the 5th Door feature         │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │                             │
              ▼                             ▼
┌───────�