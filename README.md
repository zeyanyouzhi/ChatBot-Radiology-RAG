# 🩻 ChatBot-Radiology-RAG

> AI assistant using **RAG + BioMistral-7B + Whisper** to assist in **radiology report drafting and understanding**.

---

## 🧠 Overview
This project integrates **speech-to-text** and **retrieval-augmented generation (RAG)** to support radiologists in writing structured and accurate *comptes rendus d’imagerie médicale*.

It enables clinicians or students to:
- Dictate findings orally (via Whisper)
- Automatically transcribe and interpret the text
- Retrieve similar radiology reports
- Generate structured draft summaries using BioMistral-7B

---

## 🩺 Architecture

**Workflow Summary:**
1️⃣ Audio input →  
2️⃣ Whisper transcribes speech to text →  
3️⃣ FAISS searches for similar cases →  
4️⃣ BioMistral-7B generates structured report →  
5️⃣ User reviews and finalizes.

---

## ⚙️ Tech Stack

* **Python 3.10+**
* **OpenAI Whisper** – speech-to-text model
* **FAISS** – vector search engine for document retrieval
* **BioMistral-7B** – French medical language model
* **LangChain / Transformers** – model orchestration
* *(Optional)* **Streamlit** – chatbot web interface

---

## 📂 Project Structure

```
ChatBot-Radiology-RAG/
├── speech_to_text/
│   ├── whisper_transcribe.py
│   └── audio_samples/
├── data/
│   └── corpus/
│        ├── dopa_parkinson/
│        ├── fdg_neurodegeneratif/
│        ├── choline_parathyroide/
│        ├── fdg/
│        └── psma/
├── index/
│   └── index.faiss
├── build_index.py
├── rag_query.py
└── README.md
```

---

## 🧪 Usage

### 1️⃣ Speech-to-Text

```bash
python speech_to_text/whisper_transcribe.py --audio sample_audio.wav
```

Output:

```
Transcription: "Hypofixation putaminale bilatérale suggérant une atteinte dopaminergique."
```

### 2️⃣ Build Index

```bash
python build_index.py
```

### 3️⃣ Query the RAG System

```bash
python rag_query.py --query "Quels sont les signes de la maladie de Parkinson à la 18F-FDOPA ?"
```

Expected output:

```
Hypofixation putaminale bilatérale est un signe radiologique de la maladie de Parkinson.
→ Confirmed by multiple studies (VP03, VP06) in the dataset.
```

---

## 🧩 Example Workflow

1. Doctor dictates findings using microphone
2. Whisper converts audio → text
3. FAISS searches for similar cases
4. BioMistral-7B generates a draft radiology report
5. User reviews and validates the result before finalization

---

## 🔒 Data Protection Notice

This repository **does not include any real patient data**.

> The original hospital reports used for model testing are protected under **GDPR** and **CNIL** regulations and cannot be shared.
> Only synthetic or anonymized examples are included for educational and demonstration purposes.

---

## 💬 Author

**Yanzhi Qiu**
EPF Cachan – Management & Ingénierie de la Santé
AI for Health • RAG Systems • Speech & Language Interfaces

---

## 📜 License

MIT License © 2025 Yanzhi Qiu

---

## 🌐 Keywords

`RAG` · `BioMistral` · `Whisper` · `Radiology` · `AI for Health` · `EPF Cachan`

```

---

