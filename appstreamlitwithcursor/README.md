# 🧠 Strategic Intelligence Dashboard

## 📋 Description

Application Streamlit professionnelle pour transformer les analyses textuelles d'IA en tableau de bord décisionnel interactif. Cette application implémente le format **CRAFT** (Character, Role, Action, Format, Tone) pour produire des analyses stratégiques de niveau C-suite, comparables entre modèles IA.

## 🎯 Fonctionnalités Principales

### 📊 Dashboard Exécutif
- **Métriques Clés** : Analyses récentes, scores moyens, priorités critiques, ROI estimé
- **Visualisations Interactives** : Évolution des scores, répartition par priorité
- **Tableau des Analyses** : Vue d'ensemble des analyses récentes
- **Signaux d'Alerte** : Notifications des changements importants

### 🔍 Analyse Stratégique
- **Interface d'Analyse** : Saisie de contenu avec paramètres configurables
- **Modèles IA Multiples** : Support pour Claude-3, GPT-4, Gemini, et modèles personnalisés
- **Scoring Stratégique** : Évaluation multicritère (Impact, Urgence, Complexité, Risque, Fiabilité)
- **Format CRAFT** : Génération automatique d'analyses selon le standard défini

### 📈 Comparaison Multi-IA
- **Sélection d'Analyses** : Comparaison de plusieurs analyses
- **Graphiques Comparatifs** : Radar charts et métriques de comparaison
- **Rapports Automatisés** : Génération de rapports comparatifs

### ⚙️ Configuration
- **Seuils d'Alerte** : Configuration des niveaux de priorité
- **API Keys** : Gestion des clés API pour les modèles IA
- **Paramètres d'Export** : Configuration des formats d'export

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Installation des Dépendances

```bash

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration des Variables d'Environnement

Créer un fichier `.env` à la racine du projet :

```env
# API Keys (optionnel - l'application fonctionne en mode simulation sans clés)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Configuration de l'application
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

## 🎮 Utilisation

### Lancement de l'Application

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

### Guide d'Utilisation

#### 1. Dashboard
- **Vue d'ensemble** : Consultez les métriques clés et l'évolution des scores
- **Analyses récentes** : Parcourez les dernières analyses effectuées
- **Signaux d'alerte** : Surveillez les indicateurs de changement

#### 2. Analyse Stratégique
1. **Saisie du contenu** : Collez l'article, rapport ou contenu à analyser
2. **Configuration des paramètres** :
   - Domaine de focus (Concurrence, Marché, Technologie, etc.)
   - Niveau d'urgence (Critique, Élevé, Modéré, Faible)
   - Taille d'entreprise (Startup, PME, Grande Entreprise, Multinationale)
3. **Sélection du modèle IA** : Choisissez le modèle d'analyse
4. **Ajustement des poids** : Configurez l'importance relative des critères
5. **Lancement de l'analyse** : Cliquez sur "Lancer l'Analyse"

#### 3. Comparaison Multi-IA
1. **Sélection** : Choisissez au moins 2 analyses à comparer
2. **Comparaison** : Visualisez les différences entre les modèles
3. **Rapport** : Générez un rapport comparatif automatisé

#### 4. Configuration
- **Seuils** : Ajustez les seuils d'alerte selon vos besoins
- **APIs** : Configurez vos clés API pour les modèles IA
- **Export** : Définissez vos préférences d'export

## 📊 Format CRAFT

L'application génère des analyses selon le format **CRAFT** :

### 🧠 **C – CHARACTER (Personnalité & Expertise)**
- Chief Strategic Intelligence Officer avec 15+ ans d'expérience
- Expertise en analyse prédictive et signaux faibles
- Maîtrise de la modélisation des risques concurrentiels

### 👔 **R – ROLE (Fonction & Responsabilités)**
- Transformation de l'information brute en intelligence stratégique
- Analyse stratégique multicritère
- Scoring stratégique normalisé
- Recommandations actionnables

### 🚀 **A – ACTION (Processus d'Analyse)**
1. **Phase 1** : Extraction & Catégorisation
2. **Phase 2** : Scoring Stratégique (0-10)
3. **Phase 3** : Synthèse Décisionnelle

### 📄 **F – FORMAT (Structure de Sortie)**
- Synthèse exécutive
- Scoring stratégique détaillé
- Mapping concurrentiel
- Recommandations stratégiques (3 options)
- Métriques de suivi
- Signaux d'alerte
- Métadonnées pour comparaison IA

### 🎙 **T – TONE (Style & Communication)**
- Professionnel et stratégique
- Directif et factuel
- Synthétique et orienté ROI

## 🔧 Architecture Technique

### Structure du Projet
```
strategic-intelligence-dashboard/
├── app.py                 # Application Streamlit principale
├── strategic_analyzer.py  # Module d'analyse stratégique
├── data_manager.py       # Gestion des données et persistance
├── requirements.txt      # Dépendances Python
├── README.md            # Documentation
├── .env                 # Variables d'environnement
└── data/               # Données persistantes
    ├── analyses.json   # Analyses sauvegardées
    ├── config.json     # Configuration
    └── metrics.json    # Métriques de performance
```

### Technologies Utilisées
- **Streamlit** : Interface utilisateur web
- **Plotly/Altair** : Visualisations interactives
- **Pandas** : Manipulation de données
- **OpenAI/Anthropic** : APIs des modèles IA
- **JSON** : Persistance des données

### Critères de Scoring
1. **Impact Business** (0-10) : Potentiel de revenus/coûts
2. **Urgence Temporelle** (0-10) : Fenêtre d'opportunité
3. **Complexité d'Exécution** (0-10) : Faisabilité organisationnelle
4. **Risque Concurrentiel** (0-10) : Menace/opportunité vs. compétiteurs
5. **Fiabilité Source** (0-10) : Crédibilité et fraîcheur des données

## 📈 Exemples d'Utilisation

### Analyse d'un Article Tech
```
Titre : "Amazon développe sa stratégie d'IA générative pour concurrencer ChatGPT"
Domaine : Technologie
Urgence : Élevé
Taille : Grande Entreprise
```

### Comparaison Multi-Modèles
- **Claude-3** : Score global 8.2/10 - Priorité CRITIQUE
- **GPT-4** : Score global 7.8/10 - Priorité ÉLEVÉ
- **Gemini** : Score global 7.5/10 - Priorité ÉLEVÉ

## 🔒 Sécurité et Confidentialité

- **Données Locales** : Toutes les analyses sont stockées localement
- **APIs Sécurisées** : Utilisation sécurisée des APIs externes
- **Pas de Partage** : Aucune donnée n'est partagée avec des tiers

## 🚀 Déploiement

### Déploiement Local
```bash
streamlit run app.py
```

### Déploiement Cloud (Streamlit Cloud)
1. Connectez votre repository GitHub
2. Configurez les variables d'environnement
3. Déployez automatiquement

### Docker (Optionnel)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation
- Contactez l'équipe de développement

## 🔄 Mises à Jour

### Version 1.0.0
- Interface Streamlit complète
- Support multi-modèles IA
- Format CRAFT implémenté
- Dashboard exécutif
- Comparaison multi-IA
- Persistance des données

### Roadmap
- [ ] Support pour plus de modèles IA
- [ ] Export PDF automatisé
- [ ] Intégration avec des sources de données externes
- [ ] Alertes en temps réel
- [ ] API REST pour intégration
- [ ] Mode collaboratif multi-utilisateurs 