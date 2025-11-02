


#  ChatBot-Radiology-RAG

> **AI assistant using RAG + BioMistral-7B + Whisper to assist in radiology report drafting and understanding.**

---

## 🧠 Overview
**ChatBot-Radiology-RAG** combines **speech-to-text transcription** and **retrieval-augmented generation (RAG)** to support radiologists and medical students in producing clear, structured, and accurate *comptes rendus d’imagerie médicale*.

The system enables clinicians to:
- 🎙️ Dictate findings orally through **Whisper**  
- 🧾 Automatically transcribe and interpret the text  
- 🔍 Retrieve similar radiology reports from a local FAISS index  
- 🧠 Generate a structured draft summary via **BioMistral-7B**  
- ✏️ Review, validate, and finalize the report  

---

## 🩺 Workflow Overview

**Process Summary**
1️⃣ Audio input (doctor dictation)  
2️⃣ Whisper transcribes speech → text  
3️⃣ FAISS searches for similar case reports  
4️⃣ BioMistral-7B generates a structured summary  
5️⃣ User reviews and finalizes  

---

## ⚙️ Tech Stack

| Layer | Technology | Description |
|-------|-------------|-------------|
| 🎤 **Speech Processing** | [OpenAI Whisper](https://github.com/openai/whisper) | High-accuracy multilingual speech-to-text |
| 🧠 **Language Model** | [BioMistral-7B](https://huggingface.co/BioMistral/BioMistral-7B) | French medical LLM specialized for radiology |
| 🔍 **Retrieval** | [FAISS](https://github.com/facebookresearch/faiss) | Vector database for semantic search |
| 🧩 **Pipeline Management** | LangChain / Transformers | LLM orchestration and RAG integration |
| 💻 **Interface (optional)** | Streamlit | Simple interactive chatbot interface |
| 🐍 **Core Language** | Python 3.10+ | Execution and integration layer |

---

## 📂 Project Structure

```

ChatBot-Radiology-RAG/
├── app.py
├── build_index.py
├── rag_query.py
├── model_description.txt
├── requirements.txt
│
├── speech_to_text/
│   ├── whisper_transcribe.py
│   └── audio_samples/
│
├── data/
│   ├── corpus/
│   │   ├── termes_radiologiques.txt
│   │   ├── TEP_IRM_DOPA_PARKINSON/
│   │   ├── TEP_IRM_FDG_NEURODEGENERATIF/
│   │   ├── TEP_TDM_CHOLINE_PARATHYROIDE/
│   │   ├── TEP_TDM_FDG/
│   │   └── TEP_TDM_PSMA/
│   └── index/          ← FAISS files (excluded from repo)
│
└── tools/
└── generate_tree.py

````

---

## 🧪 Usage

### 1️⃣ Speech-to-Text
```bash
python speech_to_text/whisper_transcribe.py --audio sample_audio.wav
````

**Output**

```
Transcription: "Hypofixation putaminale bilatérale suggérant une atteinte dopaminergique."
```

---

### 2️⃣ Build FAISS Index

```bash
python build_index.py
```

---

### 3️⃣ Query the RAG System

```bash
python rag_query.py --query "Quels sont les signes de la maladie de Parkinson à la 18F-FDOPA ?"
```

**Expected output**

```
Hypofixation putaminale bilatérale est un signe radiologique de la maladie de Parkinson.
→ Confirmed by multiple studies (VP03, VP06) in the dataset.
```

---

## 🔒 Data Protection Notice

This repository **does not contain any real patient data**.

> All radiology reports used for testing are anonymized or synthetic examples created for educational purposes.
> Any clinical data used in model validation are protected under **GDPR** and **CNIL** regulations and are **not publicly distributed**.

---

## 👤 Author

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
