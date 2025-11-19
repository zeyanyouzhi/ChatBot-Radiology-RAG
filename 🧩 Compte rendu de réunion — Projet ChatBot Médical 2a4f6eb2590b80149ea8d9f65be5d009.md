# 🧩 Compte rendu de réunion — Projet ChatBot Médical 25.11.7 14:00

---

## 🎯 **Objet de la réunion**

Discussion sur la conception du ChatBot destiné à la génération automatique de comptes rendus d’imagerie médicale (TEP/IRM), l’organisation de la collecte de données et la préparation d’une session de travail sur site.

---

## 🧠 **1. Structure et format des comptes rendus**

- Les comptes rendus existants sont pour la plupart en **PDF**, dont la mise en page (zones de texte, entêtes, colonnes latérales) rend difficile l’extraction automatique.
- L’équipe étudiante a déjà mis en place une **méthode d’extraction du texte central**.
- Le SHFJ recommande d’utiliser des **fichiers Word (.docx)** pour simplifier le traitement.
- Une ingénieure d’*Explore* a indiqué la méthode permettant d’exporter directement les rapports en Word.
- **Décision :** transmettre **30 comptes rendus au format Word** pour un premier entraînement du modèle.

---

## 🧩 **2. Zones types d’un compte rendu**

| Zone | Caractéristiques | Traitement prévu |
| --- | --- | --- |
| **Indication** | Très variable selon le patient | Entrée manuelle ou question posée par le ChatBot |
| **Technique** | Invariante d’un compte rendu à l’autre | Texte standard réutilisé |
| **Interprétation (IRM / TEP)** | Structure fixe mais reformulable | Interaction ligne par ligne avec le ChatBot |

> Le SHFJ souligne qu’une observation sur place est nécessaire pour bien comprendre la logique rédactionnelle et les variations possibles entre cas.
> 

---

## 🤖 **3. Fonctionnement attendu du ChatBot**

- Le ChatBot doit permettre une **rédaction interactive**, où le médecin répond simplement à quelques questions :
    - *« Y a-t-il un hypométabolisme ? » → Oui / Non*
    - Si *Oui*, préciser les régions concernées.
- L’objectif est de **remplacer la dictée vocale** (jugée peu efficace) par un assistant interactif.
- L’équipe souhaite ajouter une **plus-value réelle** : simplifier la génération des rapports tout en gardant le contrôle médical.

---

## 💻 **4. Aspects techniques et contraintes**

- Le modèle ChatBot fonctionne actuellement sur l’ordinateur de **Yanzhi**.
- Une tentative d’installation sur l’ordinateur de **Mme Haddad** a échoué pour des raisons de dépendances logicielles.
- Le réseau du **CEA / SHFJ** présente des **limitations de connexion (Wi-Fi faible, accès restreint)**.

**Solutions proposées :**

1. Réaliser une **vidéo de démonstration** du ChatBot à l’école (enregistrement de l’écran).
2. Si possible, tester sur place avec **connexion filaire (câble Ethernet)**.
3. Prévoir une **démonstration de secours (backup)** en cas de problème réseau.

---

## 🧭 **5. Organisation de la visite sur site**

- Visite planifiée le **vendredi 14 novembre 2025**, de **14 h 30 à 16 h 30**, au **Service Hospitalier Frédéric Joliot (SHFJ, Orsay)**.
- Contenu de la séance :
    - Observation de la rédaction réelle de comptes rendus.
    - Présentation du ChatBot et de son code.
    - Discussion interactive pour améliorer la logique des questions/réponses.
- L’équipe étudiante devra **prévenir l’accueil du SHFJ** à l’avance (liste des participants requise pour l’accès au site).

---

## ✅ **6. Actions décidées**

| Action | Responsable | Échéance |
| --- | --- | --- |
| Fournir 30 comptes rendus au format Word | Équipe SHFJ | 7 novembre (soir) |
| Entraîner le modèle ChatBot sur ces rapports | Équipe étudiante | Avant le 13 novembre |
| Confirmer le scénario de démonstration avec Mme Haddad | Équipe étudiante | Début de semaine prochaine |
| Prévenir l’accueil du SHFJ (liste des participants) | Équipe étudiante | Avant le 13 novembre |
| Préparer une vidéo de démonstration en backup | Équipe étudiante | Avant le 14 novembre |

---

## 🧾 **7. Conclusion**

- Le SHFJ se montre **favorable au projet** et intéressé par un prototype fonctionnel.
- Les deux équipes valident une approche **modulaire et interactive** (Question → Réponse → Génération).
- La démonstration du **14 novembre** constituera une étape clé du projet.
- Le modèle reposera sur **faster-whisper**, un système de **génération automatique de texte et de Q/A** appliqué aux rapports radiologiques.