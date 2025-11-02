# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 22:02:53 2025

@author: 20152
"""

# -*- coding: utf-8 -*-
import json, os
from pathlib import Path
import numpy as np
import faiss
import requests
import streamlit as st
from sentence_transformers import SentenceTransformer

# ==== 路径（按你的绝对路径）====
PROJECT_ROOT = Path("D:/Chatbot/RAG")
INDEX_DIR = PROJECT_ROOT / "data/index"
FAISS_PATH = INDEX_DIR / "corpus.faiss"
META_PATH  = INDEX_DIR / "metadata.json"
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "cniongolo/biomistral"  # 你本机的模型

# ==== 缓存加载 ====
@st.cache_resource
def load_index_and_meta():
    if not FAISS_PATH.exists() or not META_PATH.exists():
        raise FileNotFoundError(
            f"索引缺失：\n{FAISS_PATH}\n{META_PATH}\n请先运行 build_index.py 生成索引。"
        )
    index = faiss.read_index(str(FAISS_PATH))
    with open(META_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)
    docs  = np.array(meta["docs"], dtype=object)
    metas = meta["metas"]
    return index, docs, metas

@st.cache_resource
def get_embedder():
    return SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def embed_texts(texts):
    model = get_embedder()
    return model.encode(texts, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)

def categories_from_meta(metas):
    cats = [m.get("category") for m in metas if m.get("category")]
    cats = sorted(set(cats))
    return ["(全部)"] + cats if cats else ["(全部)"]

def retrieve(question, k=6, category=None):
    index, docs, metas = load_index_and_meta()
    qv = embed_texts([question])
    D, I = index.search(qv, max(k*4, k))

    def pick(Irow, catwant):
        picked = []
        for i in Irow:
            m = metas[i]
            cat = m.get("category")
            if catwant and catwant != "(全部)" and cat != catwant:
                continue
            picked.append((i, m, docs[i]))
            if len(picked) >= k: break
        return picked

    cand = pick(I[0], category)
    if not cand and category and category != "(全部)":
        cand = pick(I[0], None)  # 回退到全库

    ctx_lines = []
    for i, m, t in cand:
        tag = f"[{m.get('category')}/{m.get('source')}]"
        ctx_lines.append(f"{tag} {t}")
    return "\n".join(ctx_lines), cand

def build_prompt(question, context):
    system = (
        "Tu es un assistant médical spécialisé en imagerie (TEP/IRM/TDM).\n"
        "RÉPONDS UNIQUEMENT À PARTIR DU CONTEXTE fourni ci-dessous.\n"
        "Ne répète pas le contexte ni les consignes. Si l'information manque, réponds : « Je ne sais pas ».\n"
        "Structure impérativement la réponse en 4 parties : Indication, Technique, Résultats, Conclusion.\n"
        "Ne change pas les termes de la question. Cite brièvement les sources entre []."
    )
    return f"{system}\n\n### CONTEXTE\n{context}\n\n### QUESTION\n{question}\n\n### RÉPONSE ATTENDUE (FR)\n"

def ask_ollama(prompt, model=MODEL_NAME, temperature=0.1, max_tokens=700, host=OLLAMA_URL):
    try:
        r = requests.post(
            f"{host}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False,
                  "options": {"temperature": temperature, "num_predict": max_tokens}},
            timeout=120
        )
        if r.status_code != 200:
            return f"[错误] Ollama HTTP {r.status_code}：{r.text[:200]}"
        text = (r.json().get("response") or "").strip()
        return text if text else "Je ne sais pas."
    except requests.exceptions.RequestException as e:
        return f"[错误] 无法连接到 Ollama（{host}）：{e}"

def rag_answer(question, k=6, category=None):
    context, hits = retrieve(question, k=k, category=category)
    if not context or len(hits) == 0:
        return "Je ne sais pas. (Contexte insuffisant ou hors du corpus.)", context
    prompt = build_prompt(question, context)
    ans = ask_ollama(prompt)
    if ans.strip().startswith("Tu es un assistant") or ("Indication" not in ans and "Conclusion" not in ans):
        ans = "Je ne sais pas. (La réponse n'est pas basée sur le contexte.)"
    return ans, context

# ==== UI ====
st.set_page_config(page_title="RAG Radiologie (Local)", layout="wide")
st.title("🩻 RAG Radiologie — Local (Ollama + BioMistral)")

# 侧栏参数
with st.sidebar:
    st.markdown("### ⚙️ 参数")
    try:
        _, _, metas = load_index_and_meta()
        cat_options = categories_from_meta(metas)
    except Exception as e:
        cat_options = ["(全部)"]
        st.error(str(e))

    category = st.selectbox("类别（子文件夹）", cat_options, index=0)
    k = st.slider("检索条数 k", min_value=4, max_value=12, value=6, step=1)
    temp = st.slider("Temperature", 0.0, 1.0, 0.1, 0.05)
    max_new = st.slider("Max tokens", 128, 1024, 700, 64)

question = st.text_area("❓ 请输入你的问题（法语更佳）", height=100,
                        placeholder="Ex: Quelle est la structure d’un compte rendu TEP-IRM FDOPA ?")
col1, col2 = st.columns([1,1])
with col1:
    ask = st.button("🔎 提问")
with col2:
    demo = st.button("✨ 示例问题")

if demo and not question.strip():
    question = "Que signifie une hypofixation putaminale bilatérale ?"
    st.session_state["question"] = question

if ask or (demo and question):
    with st.spinner("检索与生成中…"):
        ans, ctx = rag_answer(question.strip(), k=k, category=category)
    st.markdown("### 🧠 答案")
    st.write(ans)

    with st.expander("🔎 本次使用的上下文（来源片段）"):
        st.code(ctx or "(无)", language="markdown")

st.caption("本地推理 · 模型：%s · 索引：%s" % (MODEL_NAME, FAISS_PATH))
