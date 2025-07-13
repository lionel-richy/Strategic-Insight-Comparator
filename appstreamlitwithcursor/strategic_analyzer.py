import json
import re
from datetime import datetime
from typing import List, Dict, Any
import openai
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class StrategicAnalyzer:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.setup_clients()
    
    def setup_clients(self):
        """Configure les clients API pour les différents modèles IA"""
        try:
            if os.getenv("OPENAI_API_KEY"):
                self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            if os.getenv("ANTHROPIC_API_KEY"):
                self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        except Exception as e:
            print(f"Erreur lors de la configuration des clients API: {e}")
    
    def analyze_content(self, content: str, focus_area: str, urgency_level: str, 
                       company_size: str, ai_model: str, weights: List[float]) -> str:
        """
        Analyse le contenu selon le format CRAFT et retourne une analyse stratégique
        """
        try:
            # Préparation du prompt selon le format CRAFT
            prompt = self._create_craft_prompt(content, focus_area, urgency_level, 
                                             company_size, ai_model, weights)
            
            # Analyse selon le modèle sélectionné
            if ai_model == "Claude-3-Sonnet" and self.anthropic_client:
                return self._analyze_with_claude(prompt)
            elif ai_model == "GPT-4" and self.openai_client:
                return self._analyze_with_gpt4(prompt)
            else:
                return self._analyze_with_simulation(prompt, content, focus_area, 
                                                   urgency_level, company_size, weights)
        
        except Exception as e:
            return f"Erreur lors de l'analyse: {str(e)}"
    
    def _create_craft_prompt(self, content: str, focus_area: str, urgency_level: str,
                           company_size: str, ai_model: str, weights: List[float]) -> str:
        """Crée le prompt selon le format CRAFT"""
        
        prompt = f"""
# 🧠 **C – CHARACTER (Personnalité & Expertise)**
Tu es un **Chief Strategic Intelligence Officer** avec 15+ ans d'expérience en intelligence économique. Tu maîtrises :
- L'analyse prédictive et les signaux faibles
- La modélisation des risques concurrentiels
- L'évaluation multicritère des opportunités stratégiques
- La synthèse exécutive pour comités de direction

**Mission** : Produire une analyse stratégique de niveau C-suite selon le format CRAFT.

---

# 👔 **R – ROLE (Fonction & Responsabilités)**
Ton rôle est de **transformer l'information brute en intelligence stratégique exploitable** via :

**🔍 Analyse Stratégique Multicritère**
- Détection d'opportunités de marché et menaces concurrentielles
- Évaluation de l'urgence décisionnelle et du potentiel d'impact
- Identification des acteurs clés et des dynamiques sectorielles

**📊 Scoring Stratégique Normalisé**
- Matrices de priorisation standardisées
- Métriques de fiabilité et de consensus
- Indicateurs de volatilité temporelle

**🎯 Recommandations Actionnables**
- Scénarios d'action avec timelines
- Allocation de ressources suggérée
- Métriques de suivi proposées

---

# 🚀 **A – ACTION (Processus d'Analyse)**

## **Phase 1 : Extraction & Catégorisation**
1. **Analyse sémantique** : Sentiment, tonalité, niveau d'incertitude
2. **Mapping concurrentiel** : Identification des acteurs, relations, positions
3. **Détection de signaux** : Tendances émergentes, ruptures, innovations

## **Phase 2 : Scoring Stratégique (Échelle 0-10)**
- **Impact Business** : Potentiel de revenus/coûts (Poids: {weights[0]})
- **Urgence Temporelle** : Fenêtre d'opportunité (Poids: {weights[1]})
- **Complexité d'Exécution** : Faisabilité organisationnelle (Poids: {weights[2]})
- **Risque Concurrentiel** : Menace/opportunité vs. compétiteurs (Poids: {weights[3]})
- **Fiabilité Source** : Crédibilité et fraîcheur des données (Poids: {weights[4]})

## **Phase 3 : Synthèse Décisionnelle**
- **Matrice de Priorisation** : Urgence vs. Impact
- **Scénarios d'Action** : 3 options stratégiques
- **Métriques de Suivi** : KPIs de monitoring

---

# 📄 **F – FORMAT (Structure de Sortie Normalisée)**

Analyse le contenu suivant selon le format CRAFT :

**CONTENU À ANALYSER :**
{content}

**PARAMÈTRES D'ANALYSE :**
- Domaine de Focus : {focus_area}
- Niveau d'Urgence : {urgency_level}
- Taille d'Entreprise : {company_size}
- Modèle IA : {ai_model}

**FORMAT DE SORTIE ATTENDU :**

```markdown
# 📈 ANALYSE STRATÉGIQUE - [TITRE ARTICLE]
**🗓️ Date d'Analyse :** {datetime.now().strftime('%Y-%m-%d %H:%M')} | **🔍 Analyste IA :** {ai_model}

## 🎯 SYNTHÈSE EXÉCUTIVE
[Résumé de 2-3 phrases pour C-level avec impact business immédiat]

## 📊 SCORING STRATÉGIQUE
| Critère | Score | Justification |
|---------|-------|---------------|
| **Impact Business** | x/10 | [Potentiel financier quantifié] |
| **Urgence Temporelle** | x/10 | [Fenêtre d'action disponible] |
| **Complexité Exécution** | x/10 | [Faisabilité organisationnelle] |
| **Risque Concurrentiel** | x/10 | [Menace/opportunité vs. concurrents] |
| **Fiabilité Source** | x/10 | [Crédibilité et fraîcheur] |

**🎯 SCORE GLOBAL DE PRIORITÉ :** [x/10] - **Niveau : [CRITIQUE/ÉLEVÉ/MODÉRÉ/FAIBLE]**

## 🏢 MAPPING CONCURRENTIEL
### Acteurs Principaux
- **[Entreprise 1]** : [Position/Stratégie]
- **[Entreprise 2]** : [Position/Stratégie]

### Dynamiques Sectorielles
- **[Tendance 1]** : [Impact et temporalité]
- **[Tendance 2]** : [Impact et temporalité]

## 🚀 RECOMMANDATIONS STRATÉGIQUES

### Option 1 : [Nom Stratégie] - **[PRIORITÉ : HAUTE/MOYENNE/BASSE]**
- **Action** : [Décision concrète]
- **Timeline** : [Horizon temporel]
- **Ressources** : [Investissement requis]
- **ROI Estimé** : [Retour attendu]

### Option 2 : [Nom Stratégie] - **[PRIORITÉ]**
- **Action** : [Décision concrète]
- **Timeline** : [Horizon temporel]
- **Ressources** : [Investissement requis]
- **ROI Estimé** : [Retour attendu]

### Option 3 : [Nom Stratégie] - **[PRIORITÉ]**
- **Action** : [Décision concrète]
- **Timeline** : [Horizon temporel]
- **Ressources** : [Investissement requis]
- **ROI Estimé** : [Retour attendu]

## 📈 MÉTRIQUES DE SUIVI PROPOSÉES
- **KPI Principal** : [Métrique mesurable]
- **KPI Secondaire** : [Métrique de soutien]
- **Fréquence de Monitoring** : [Quotidien/Hebdomadaire/Mensuel]

## ⚠️ SIGNAUX D'ALERTE
- **Signal 1** : [Indicateur de changement]
- **Signal 2** : [Indicateur de risque]

## 🔍 MÉTADONNÉES POUR COMPARAISON IA
- **Niveau de Confiance** : [Élevé/Moyen/Faible]
- **Données Manquantes** : [Limitations identifiées]
- **Biais Potentiels** : [Angles morts possibles]
```

**IMPORTANT :** 
- Utilise des scores réalistes et justifiés
- Adapte l'analyse au contexte {company_size} et {focus_area}
- Fournis des recommandations actionnables
- Inclus des métriques quantifiables
- Identifie clairement les risques et opportunités
"""
        return prompt
    
    def _analyze_with_claude(self, prompt: str) -> str:
        """Analyse avec Claude-3-Sonnet"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Erreur Claude API: {str(e)}"
    
    def _analyze_with_gpt4(self, prompt: str) -> str:
        """Analyse avec GPT-4"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un expert en analyse stratégique et intelligence économique."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erreur GPT-4 API: {str(e)}"
    
    def _analyze_with_simulation(self, prompt: str, content: str, focus_area: str,
                               urgency_level: str, company_size: str, weights: List[float]) -> str:
        """Analyse simulée pour démonstration (quand les APIs ne sont pas disponibles)"""
        
        # Extraction du titre du contenu
        title = self._extract_title(content)
        
        # Scoring simulé basé sur le contenu et les paramètres
        scores = self._generate_simulated_scores(content, focus_area, urgency_level, company_size)
        
        # Calcul du score global pondéré
        global_score = sum(scores[i] * weights[i] for i in range(len(scores)))
        
        # Détermination du niveau de priorité
        priority_level = self._determine_priority_level(global_score)
        
        # Génération de l'analyse selon le format CRAFT
        analysis = f"""# 📈 ANALYSE STRATÉGIQUE - {title}
**🗓️ Date d'Analyse :** {datetime.now().strftime('%Y-%m-%d %H:%M')} | **🔍 Analyste IA :** Modèle Simulé

## 🎯 SYNTHÈSE EXÉCUTIVE
Analyse stratégique automatisée du contenu fourni, adaptée au contexte {company_size} dans le domaine {focus_area}. 
Impact business estimé avec niveau d'urgence {urgency_level.lower()}.

## 📊 SCORING STRATÉGIQUE
| Critère | Score | Justification |
|---------|-------|---------------|
| **Impact Business** | {scores[0]}/10 | Potentiel financier significatif pour {company_size} |
| **Urgence Temporelle** | {scores[1]}/10 | Fenêtre d'action {urgency_level.lower()} identifiée |
| **Complexité Exécution** | {scores[2]}/10 | Faisabilité adaptée à {company_size} |
| **Risque Concurrentiel** | {scores[3]}/10 | Positionnement dans {focus_area} |
| **Fiabilité Source** | {scores[4]}/10 | Qualité des données analysées |

**🎯 SCORE GLOBAL DE PRIORITÉ :** {global_score:.1f}/10 - **Niveau : {priority_level}**

## 🏢 MAPPING CONCURRENTIEL
### Acteurs Principaux
- **[Acteur Principal]** : Position dominante dans {focus_area}
- **[Nouveau Entrant]** : Innovation disruptive détectée

### Dynamiques Sectorielles
- **[Tendance 1]** : Évolution rapide du marché {focus_area}
- **[Tendance 2]** : Transformation technologique en cours

## 🚀 RECOMMANDATIONS STRATÉGIQUES

### Option 1 : Stratégie Offensive - **[PRIORITÉ : HAUTE]**
- **Action** : Investissement immédiat dans {focus_area}
- **Timeline** : 3-6 mois
- **Ressources** : 15-25% du budget innovation
- **ROI Estimé** : 150-200% sur 18 mois

### Option 2 : Stratégie Défensive - **[PRIORITÉ : MOYENNE]**
- **Action** : Renforcement des capacités existantes
- **Timeline** : 6-12 mois
- **Ressources** : 10-15% du budget opérationnel
- **ROI Estimé** : 80-120% sur 24 mois

### Option 3 : Stratégie d'Observation - **[PRIORITÉ : BASSE]**
- **Action** : Monitoring et veille concurrentielle
- **Timeline** : 12-18 mois
- **Ressources** : 5-8% du budget R&D
- **ROI Estimé** : 40-60% sur 36 mois

## 📈 MÉTRIQUES DE SUIVI PROPOSÉES
- **KPI Principal** : Part de marché dans {focus_area}
- **KPI Secondaire** : Taux d'adoption des innovations
- **Fréquence de Monitoring** : Hebdomadaire

## ⚠️ SIGNAUX D'ALERTE
- **Signal 1** : Nouvelle réglementation dans {focus_area}
- **Signal 2** : Entrée de nouveaux concurrents majeurs

## 🔍 MÉTADONNÉES POUR COMPARAISON IA
- **Niveau de Confiance** : Moyen
- **Données Manquantes** : Informations détaillées sur les concurrents
- **Biais Potentiels** : Analyse basée sur données simulées
"""
        return analysis
    
    def _extract_title(self, content: str) -> str:
        """Extrait un titre du contenu"""
        lines = content.split('\n')
        for line in lines:
            if line.strip() and len(line.strip()) < 100:
                return line.strip()
        return "Analyse Stratégique"
    
    def _generate_simulated_scores(self, content: str, focus_area: str, 
                                 urgency_level: str, company_size: str) -> List[float]:
        """Génère des scores simulés basés sur le contenu et les paramètres"""
        import random
        
        # Base scores selon les paramètres
        base_scores = {
            "Impact Business": 7.5,
            "Urgence Temporelle": 6.8,
            "Complexité Exécution": 5.2,
            "Risque Concurrentiel": 6.5,
            "Fiabilité Source": 7.0
        }
        
        # Ajustements selon les paramètres
        if urgency_level == "Critique":
            base_scores["Urgence Temporelle"] += 2.0
        elif urgency_level == "Élevé":
            base_scores["Urgence Temporelle"] += 1.0
        
        if company_size == "Startup":
            base_scores["Complexité Exécution"] -= 1.0
            base_scores["Impact Business"] += 1.0
        elif company_size == "Multinationale":
            base_scores["Complexité Exécution"] += 1.0
            base_scores["Risque Concurrentiel"] += 0.5
        
        # Ajout de variabilité
        scores = []
        for score in base_scores.values():
            scores.append(min(10.0, max(0.0, score + random.uniform(-0.5, 0.5))))
        
        return scores
    
    def _determine_priority_level(self, global_score: float) -> str:
        """Détermine le niveau de priorité basé sur le score global"""
        if global_score >= 8.0:
            return "CRITIQUE"
        elif global_score >= 6.5:
            return "ÉLEVÉ"
        elif global_score >= 5.0:
            return "MODÉRÉ"
        else:
            return "FAIBLE"
    
    def extract_metrics_from_analysis(self, analysis: str) -> Dict[str, Any]:
        """Extrait les métriques clés d'une analyse pour le dashboard"""
        metrics = {
            "global_score": 0.0,
            "priority_level": "MODÉRÉ",
            "impact_score": 0.0,
            "urgency_score": 0.0,
            "complexity_score": 0.0,
            "risk_score": 0.0,
            "reliability_score": 0.0
        }
        
        try:
            # Extraction du score global
            global_score_match = re.search(r'SCORE GLOBAL DE PRIORITÉ :\s*([\d.]+)/10', analysis)
            if global_score_match:
                metrics["global_score"] = float(global_score_match.group(1))
            
            # Extraction du niveau de priorité
            priority_match = re.search(r'Niveau :\s*([A-ZÉ]+)', analysis)
            if priority_match:
                metrics["priority_level"] = priority_match.group(1)
            
            # Extraction des scores individuels
            score_patterns = {
                "impact_score": r'Impact Business.*?(\d+(?:\.\d+)?)/10',
                "urgency_score": r'Urgence Temporelle.*?(\d+(?:\.\d+)?)/10',
                "complexity_score": r'Complexité Exécution.*?(\d+(?:\.\d+)?)/10',
                "risk_score": r'Risque Concurrentiel.*?(\d+(?:\.\d+)?)/10',
                "reliability_score": r'Fiabilité Source.*?(\d+(?:\.\d+)?)/10'
            }
            
            for key, pattern in score_patterns.items():
                match = re.search(pattern, analysis, re.DOTALL)
                if match:
                    metrics[key] = float(match.group(1))
        
        except Exception as e:
            print(f"Erreur lors de l'extraction des métriques: {e}")
        
        return metrics 