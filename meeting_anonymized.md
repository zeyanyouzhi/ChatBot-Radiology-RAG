# 🧩 Compte rendu de réunion — Projet ChatBot Médical (Version Anonymisée)

## 🎯 Objet de la réunion
Réunion sur la conception du ChatBot destiné à la génération de comptes rendus d’imagerie médicale, la collecte des données et la préparation d’une session d’observation dans un service clinique partenaire.

## 🧠 1. Structure et format des comptes rendus
- Les CR sources sont souvent en PDF, difficiles à exploiter automatiquement.
- Extraction du texte principal déjà mise en place.
- Recommandation : utilisation de fichiers Word (.docx) pour simplifier le traitement.
- Transmission d’un premier lot d’environ 30 CR Word.

## 🧩 2. Zones types d’un compte rendu
| Zone | Caractéristiques | Traitement prévu |
|------|------------------|------------------|
| Indication | Très variable | Entrée manuelle ou via questions |
| Technique | Quasi invariante | Réutilisation directe |
| Interprétation (IRM / TEP) | Structure stable | Interaction guidée |

## 🤖 3. Fonctionnement attendu du ChatBot
- Rédaction interactive basée sur des questions/réponses simples.
- Exemple : “Hypométabolisme ?” → Oui/Non + précisions orales.
- Objectif : gain de temps et cohérence → plus-value par rapport à la dictée vocale.
- Utilisation de modèles légers, compatibles avec un environnement local.

## 💻 4. Aspects techniques et contraintes
- Prototype fonctionnel sur un poste étudiant.
- Installation sur un autre poste bloquée par des dépendances manquantes.
- Réseau interne du site clinique : restrictions de connexion.

### Solutions envisagées
1. Vidéo de démonstration.
2. Test sur place via connexion filaire.
3. Scénario de démonstration alternatif en backup.

## 🧭 5. Organisation de la séance d’observation
- Observation du flux réel de rédaction.
- Validation du prototype et des enchaînements de questions.
- Accès au site nécessitant une liste de participants.

## ✅ 6. Actions décidées
| Action | Responsable |
|--------|-------------|
| Transmission des CR Word | Service clinique |
| Intégration + tests | Équipe étudiante |
| Scénario de démonstration | Équipe étudiante |
| Liste des participants | Équipe étudiante |
| Vidéo de backup | Équipe étudiante |

## 🧾 7. Conclusion
- Intérêt confirmé pour un prototype fonctionnel.
- L’approche Q/A → génération est jugée pertinente.
- La séance d’observation permettra d’aligner le modèle sur les pratiques cliniques réelles.
- Le système reposera sur des modèles légers compatibles avec l’environnement local.
