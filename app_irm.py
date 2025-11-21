# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 10:54:38 2025

@author: 20152
"""

import requests, json, re

MODEL_NAME = "cniongolo/biomistral"
OLLAMA_URL = "http://localhost:11434/api/generate"

OPENING_QUESTION = """Pouvez-vous me donner :
- le score Fazekas ?
- les scores Scheltens (droite et gauche) ?"""

def extract_three_scores(text):
    """
    从用户输入中提取恰好三个数字：
    Fazekas, Scheltens droite, Scheltens gauche

    支持：
    - 123 / 222
    - 1 2 3
    - 1 2/3
    - 1,2,3
    - Fazekas 1 Scheltens 2 3
    - 罗马数字 I/II/III（会转成 1/2/3）
    
    规则：输入里数字总数必须恰好=3（不多不少）
    """
    t = text.lower()

    # 罗马数字 → 阿拉伯数字
    roman_map = {"i": "1", "ii": "2", "iii": "3", "0": "0"}
    for r, v in roman_map.items():
        t = re.sub(rf"\b{r}\b", v, t)

    # 把所有数字字符抓出来（连写也能抓）
    digits = re.findall(r"\d", t)

    if len(digits) != 3:
        raise ValueError(
            f"请输入恰好 3 个数字（Fazekas, Scheltens droite, Scheltens gauche）。"
            f"当前识别到 {len(digits)} 个：{digits}"
        )

    fazekas, scheltens_d, scheltens_g = map(int, digits)

    return fazekas, scheltens_d, scheltens_g

def call_ollama(prompt, model=MODEL_NAME):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    res = requests.post(OLLAMA_URL, json=payload)
    data = res.json()

    if "error" in data:
        raise RuntimeError(f"Ollama error: {data['error']}")
    return data.get("response", "")


def extract_scores(user_input):
    """
    先用正则/规则提取（最稳），提不出来再用 LLM。
    """
    text = user_input.lower()

    # --- 1) Fazekas：支持数字或罗马数字 ---
    roman_map = {"i": 1, "ii": 2, "iii": 3, "0": 0}
    fazekas = None

    # 数字版：fazekas 0-3 / fazekas à 1
    m = re.search(r"fazekas\s*(?:à|=|:)?\s*([0-3])", text)
    if m:
        fazekas = int(m.group(1))
    else:
        # 罗马版：fazekas i/ii/iii
        m = re.search(r"fazekas\s*(?:à|=|:)?\s*(i{1,3})", text)
        if m:
            fazekas = roman_map.get(m.group(1), None)

    # --- 2) Scheltens：优先抓 “droite/gauche” 形式 ---
    scheltens_d = None
    scheltens_g = None

    md = re.search(r"scheltens\s*(?:à|=|:)?\s*([0-4])\s*(?:a|à)?\s*droite", text)
    mg = re.search(r"scheltens\s*(?:à|=|:)?\s*([0-4])\s*(?:a|à)?\s*gauche", text)

    if md:
        scheltens_d = int(md.group(1))
    if mg:
        scheltens_g = int(mg.group(1))

    # --- 3) Scheltens 简写：3/2 或 "3 droite, 2 gauche" ---
    if scheltens_d is None or scheltens_g is None:
        mslash = re.search(r"scheltens\s*[:=]?\s*([0-4])\s*/\s*([0-4])", text)
        if mslash:
            scheltens_d = scheltens_d if scheltens_d is not None else int(mslash.group(1))
            scheltens_g = scheltens_g if scheltens_g is not None else int(mslash.group(2))

    if scheltens_d is None:
        md2 = re.search(r"([0-4])\s*(?:a|à)?\s*droite", text)
        if md2:
            scheltens_d = int(md2.group(1))

    if scheltens_g is None:
        mg2 = re.search(r"([0-4])\s*(?:a|à)?\s*gauche", text)
        if mg2:
            scheltens_g = int(mg2.group(1))

    # --- 4) 如果规则已经提出来了，就直接返回 ---
    if fazekas is not None and scheltens_d is not None and scheltens_g is not None:
        return {
            "fazekas": fazekas,
            "scheltens_d": scheltens_d,
            "scheltens_g": scheltens_g
        }

    # --- 5) 规则提不全，再 fallback 用 LLM ---
    prompt = f"""
Tu es un extracteur STRICT et tu ne produis QUE du JSON.
Ne mets aucun texte autour. Pas de HTML.

Texte utilisateur:
\"\"\"{user_input}\"\"\"

Retourne EXACTEMENT:
{{
  "fazekas": <0-3 ou null>,
  "scheltens_d": <0-4 ou null>,
  "scheltens_g": <0-4 ou null>
}}
"""
    raw = call_ollama(prompt).strip()
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        # 最后兜底：把目前能提出来的先返回
        return {
            "fazekas": fazekas,
            "scheltens_d": scheltens_d,
            "scheltens_g": scheltens_g
        }

    data = json.loads(match.group(0))
    return data



def generate_irm_report(fazekas, scheltens_d, scheltens_g):
    template = (
        "IRM : Absence de signe ischémique récent en séquence de Diffusion. "
        "Pas de saignement récent ni de stigmate de microsaignement. "
        "Leucopathie vasculaire Fazekas {FAZEKAS}. "
        "Pas d’anomalie de signal du parenchyme cérébral par ailleurs. "
        "Atrophie corticale non significative pour l'âge. "
        "Les hippocampes sont cotés Scheltens à {SCHELTENS_D} droite et {SCHELTENS_G} à gauche. "
        "Pas de processus expansif intra ou extra axial. "
        "Structures de la ligne médiane et amygdales cérébelleuses en place."
    )

    roman = {0: "0", 1:"I", 2:"II", 3:"III"}
    fazekas_roman = roman.get(int(fazekas), str(fazekas))

    report = template.replace("{FAZEKAS}", str(fazekas_roman)) \
                     .replace("{SCHELTENS_D}", str(scheltens_d)) \
                     .replace("{SCHELTENS_G}", str(scheltens_g))
    return report

def main():
    # ====== 1) 问 Indication ======
    print("Assistant: Quelle est l’indication clinique ?")
    indication = input("User: ").strip()

    # ====== 2) 先问 Lot（批号） ======
    print("Assistant: Numéro de lot du radiopharmaceutique ?")
    lot_number = input("User: ").strip()

    # ====== 3) 再问 Glycémie ======
    print("Assistant: Glycémie ? (ex : 0.97 g/l)")
    glycemie = input("User: ").strip()
    if glycemie and "g" not in glycemie.lower():
        glycemie = glycemie + " g/l"

    # ====== 4) IRM 部分：问三个数字 ======
    print("\nAssistant: Veuillez entrer Fazekas, Scheltens droite, Scheltens gauche (ex : '1 2 3' ou '1/2/3' ou '123') :")
    irm_input = input("User: ").strip()
    
    fazekas, scheltens_d, scheltens_g = extract_three_scores(irm_input)
    
    report_irm = generate_irm_report(
        fazekas=fazekas,
        scheltens_d=scheltens_d,
        scheltens_g=scheltens_g
    )

    # ====== 5) Technique 固定模板 ======
    technique_text = (
        f"Technique de l’examen :\n"
        f"Injection de 205,037 MBq de F 18 – Lot : {lot_number}.\n"
        f"Acquisition TEP/IRM du crâne 30 minutes après l'injection du radiopharmaceutique, "
        f"sur une caméra TEP/IRM 3 Tesla GE Signa (date de première mise en service clinique: "
        f"15 mars 2017, décision n°16-305).\n"
        f"Séquences : DIFFUSION, FLAIR, T2, T2*, T1 volumique.\n"
        f"Glycémie : {glycemie}\n"
    )

    # ====== 6) 合并输出 ======
    final_report = (
        f"Indication : {indication}\n"
        + technique_text
        + "\n---\n\n"
        + "Resultat:\n"
        + report_irm
    )

    # ====== 7) 输出报告 ======
    print("\nAssistant (Compte-rendu final):\n")
    print(final_report)



if __name__ == "__main__":
    main()
