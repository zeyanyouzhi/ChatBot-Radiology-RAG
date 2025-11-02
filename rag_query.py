# -*- coding: utf-8 -*-
"""
RAG 推理脚本（绝对路径版，支持类别过滤 + BioMistral/Ollama）
用法：
  1) 先在命令行确保 Ollama 有 biomistral 模型： ollama list
  2) Spyder 里运行本文件，查看示例输出
"""

import os, json, time, sys
from pathlib import Path
import numpy as np
import faiss
import requests
from sentence_transformers import SentenceTransformer

# ========= 1) 绝对路径配置（按你现在的项目结构） =========
PROJECT_ROOT = Path("D:/Chatbot/RAG")
INDEX_DIR    = PROJECT_ROOT / "data/index"              # 存放 corpus.faiss / metadata.json
FAISS_PATH   = INDEX_DIR / "corpus.faiss"
META_PATH    = INDEX_DIR / "metadata.json"

# ========= 2) 基础加载 =========
def load_index_and_meta():
    if not FAISS_PATH.exists() or not META_PATH.exists():
        raise FileNotFoundError(
            f"索引或元数据缺失：\n  {FAISS_PATH}\n  {META_PATH}\n"
            "请先运行 build_index.py 生成索引。"
        )
    index = faiss.read_index(str(FAISS_PATH))
    with open(META_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)
    docs  = np.array(meta["docs"], dtype=object)
    metas = meta["metas"]
    return index, docs, metas

# 统一加载一次 embedding 模型（多语言、小巧、够用）
_EMB_MODEL = None
def get_embedder():
    global _EMB_MODEL
    if _EMB_MODEL is None:
        _EMB_MODEL = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return _EMB_MODEL

def embed_texts(texts):
    model = get_embedder()
    vecs = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)
    return vecs

# ========= 3) 检索（可选类别过滤） =========
def retrieve(question, k=6, category=None):
    index, docs, metas = load_index_and_meta()
    qv = embed_texts([question])
    D, I = index.search(qv, max(k*4, k))

    def pick(Irow, category):
        picked = []
        for i in Irow:
            m = metas[i]
            cat = m.get("category")
            if category and cat != category:
                continue
            picked.append((i, m, docs[i]))
            if len(picked) >= k:
                break
        return picked

    cand = pick(I[0], category)

    # ★ 回退策略：类别结果为空 → 再来一次不带类别
    if not cand and category:
        cand = pick(I[0], category=None)

    ctx_lines = []
    for i, m, t in cand:
        tag = f"[{m.get('category')}/{m.get('source')}]"
        ctx_lines.append(f"{tag} {t}")
    context = "\n".join(ctx_lines)
    return context, cand

# ========= 4) Prompt 构建（严格模式 + 结构化输出） =========
def build_prompt(question, context):
    system = (
        "Tu es un assistant médical spécialisé en imagerie (TEP/IRM/TDM).\n"
        "RÉPONDS UNIQUEMENT À PARTIR DU CONTEXTE fourni ci-dessous.\n"
        "Ne répète pas le contexte ni les consignes. Si l'information manque, réponds : « Je ne sais pas ».\n"
        "Structure impérativement la réponse en 4 parties : Indication, Technique, Résultats, Conclusion.\n"
        "Ne change pas les termes de la question. Cite brièvement les sources entre []."
    )
    return (
        f"{system}\n\n"
        f"### CONTEXTE\n{context}\n\n"
        f"### QUESTION\n{question}\n\n"
        f"### RÉPONSE ATTENDUE (FR)\n"
    )


# ========= 5) 调用 Ollama / BioMistral =========
def ask_ollama(prompt, model="cniongolo/biomistral", temperature=0.2, max_tokens=512, host="http://localhost:11434"):
    import requests, json
    url = f"{host}/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens}
    }
    try:
        resp = requests.post(url, json=data, timeout=120)
        if resp.status_code != 200:
            return f"[错误] Ollama HTTP {resp.status_code}：{resp.text[:200]}"
        j = resp.json()
        return (j.get("response") or "").strip() or "[错误] 模型返回空字符串。"
    except requests.exceptions.RequestException as e:
        return f"[错误] 无法连接到 Ollama：{e}"
    except Exception as e:
        return f"[错误] 解析模型返回失败：{e}"


# ========= 6) 一次性问答封装 =========
def rag_answer(question, k=6, category=None):
    context, hits = retrieve(question, k=k, category=category)
    if not context or len(hits) == 0:
        return "Je ne sais pas. (Contexte insuffisant ou hors du corpus.)"
    prompt = build_prompt(question, context)
    ans = ask_ollama(prompt, temperature=0.1, max_tokens=700)
    # 防止回显：若输出仍只有系统句，且没出现 Indication 等关键词，则退回不知道
    if ans.strip().startswith("Tu es un assistant") and ("Indication" not in ans):
        return "Je ne sais pas. (La réponse n'est pas basée sur le contexte.)"
    return ans


# ========= 7) 示例：直接运行本文件做三次测试 =========
if __name__ == "__main__":
    print(">>> 测试 1：结构类（不指定类别）")
    q1 = "Quelle est la structure d’un compte rendu TEP-IRM FDOPA ?"
    print(rag_answer(q1, k=6, category=None))
    print("\n" + "-"*80 + "\n")

    print(">>> 测试 2：术语解释（按类别 dopa_parkinson 检索）")
    q2 = "Que signifie une hypofixation putaminale bilatérale dans ce contexte ?"
    print(rag_answer(q2, k=6, category="dopa_parkinson"))
    print("\n" + "-"*80 + "\n")

    print(">>> 测试 3：否定/缺失信息的处理")
    q3 = "Y a-t-il une atrophie pontique sévère décrite dans ces cas ?"
    print(rag_answer(q3, k=6, category="dopa_parkinson"))
