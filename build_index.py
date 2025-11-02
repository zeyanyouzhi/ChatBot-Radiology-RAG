# build_index.py
import os, json, glob
from sentence_transformers import SentenceTransformer
import faiss, numpy as np
from pathlib import Path

BASE = Path("data/corpus")
paths = []
for folder in ["CR_anonymises/dopa_parkinson", "normes"]:
    paths += sorted(glob.glob(str(BASE/folder/"*.txt")))
# 术语表也可以作为一条长文本加入（可选）
paths += [str(BASE/"termes_radiologiques.txt")]

docs, metas = [], []
for fp in paths:
    with open(fp, "r", encoding="utf-8") as f:
        text = f.read().strip()
    # 简单切块：按空行/句号分块，避免块过长
    chunks = [c.strip() for c in text.split("\n") if c.strip()]
    for i, ch in enumerate(chunks):
        docs.append(ch)
        metas.append({"source": os.path.basename(fp), "chunk_id": i})

# 多语 embedding（稳妥通用）
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
emb = model.encode(docs, convert_to_numpy=True, show_progress_bar=True, normalize_embeddings=True)

dim = emb.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(emb)

os.makedirs("index", exist_ok=True)
faiss.write_index(index, "index/corpus.faiss")
with open("index/metadata.json", "w", encoding="utf-8") as f:
    json.dump({"docs": docs, "metas": metas}, f, ensure_ascii=False, indent=2)

print(f"Built index with {len(docs)} chunks.")
