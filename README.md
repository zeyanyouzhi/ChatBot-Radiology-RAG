<p align="center">
  <img src="cover_radiology_rag.png" alt="Radiology RAG Chatbot – AI for Health" width="80%">
</p>



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
├── app/
│   └── app.py                  # 主入口：UI / demo（以后可以是 Gradio / Streamlit）
│
├── src/
│   ├── __init__.py
│   │
│   ├── rag/
│   │   ├── build_index.py      # 原来的 build_index.py
│   │   ├── rag_query.py        # 原来的 rag_query.py
│   │   └── model_description.txt
│   │
│   ├── stt/
│   │   ├── whisper_transcribe.py
│   │   └── audio_samples/      # 音频样例
│   │
│   ├── decision_tree/
│   │   ├── generate_tree.py    # 原来的 tools/generate_tree.py
│   │   └── arbre_config.yml    # 未来放“决策树”配置（医生给的 arbre）
│   │
│   └── templates/
│       └── reports/            # 将来放 CR 模板（normal / MAD / DFT 等）
│
├── data/
│   ├── corpus/
│   │   ├── termes_radiologiques.txt
│   │   ├── TEP_IRM_DOPA_PARKINSON/
│   │   ├── TEP_IRM_FDG_NEURODEGENERATIF/
│   │   ├── TEP_TDM_CHOLINE_PARATHYROIDE/
│   │   ├── TEP_TDM_FDG/
│   │   └── TEP_TDM_PSMA/
│   │
│   ├── raw_cr/                 # 50 comptes rendus（Word → txt）
│   └── index/                  # FAISS 
│
├── docs/
│   ├── README_project.md       
│   ├── architecture.md         # 架构图 + 流程说明（RAG + STT + 决策树）
│   └── meeting_2024-11-14_SHFJ.md  # 会议信息总结
│
├── tools/
│   └── __init__.py             # 如果以后还有一次性小脚本可以留这里
│
├── requirements.txt
└── README.md                   # 对外总 README（简短版）


````

---

## 🧪 Usage

### 1️⃣ Speech-to-Text
```bash
python speech_to_text/transcrit_apres_parole.py --audio sample_audio.wav
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
