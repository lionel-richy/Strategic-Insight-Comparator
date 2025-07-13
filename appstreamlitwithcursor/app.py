import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import numpy as np
from streamlit_option_menu import option_menu
import altair as alt
from strategic_analyzer import StrategicAnalyzer
from data_manager import DataManager
import os

# Configuration de la page
st.set_page_config(
    page_title="Strategic Intelligence Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .priority-high { color: #d62728; font-weight: bold; }
    .priority-medium { color: #ff7f0e; font-weight: bold; }
    .priority-low { color: #2ca02c; font-weight: bold; }
    .stAlert { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

class StrategicDashboard:
    def __init__(self):
        self.data_manager = DataManager()
        self.analyzer = StrategicAnalyzer()
        
    def main(self):
        # Header principal
        st.markdown('<h1 class="main-header">🧠 Strategic Intelligence Dashboard</h1>', unsafe_allow_html=True)
        
        # Menu de navigation
        selected = option_menu(
            menu_title=None,
            options=["📊 Dashboard", "🔍 Analyse", "📈 Comparaison", "⚙️ Configuration"],
            icons=["bar-chart", "search", "graph-up", "gear"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )
        
        if selected == "📊 Dashboard":
            self.show_dashboard()
        elif selected == "🔍 Analyse":
            self.show_analysis()
        elif selected == "📈 Comparaison":
            self.show_comparison()
        elif selected == "⚙️ Configuration":
            self.show_configuration()
    
    def show_dashboard(self):
        st.markdown("## 📊 Tableau de Bord Exécutif")
        
        # Métriques clés
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>Analyses Récentes</h3>
                <h2>24</h2>
                <p>+12% vs mois dernier</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>Score Moyen</h3>
                <h2>7.2/10</h2>
                <p>+0.8 vs mois dernier</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>Priorités Critiques</h3>
                <h2>8</h2>
                <p>3 nouvelles cette semaine</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>ROI Estimé</h3>
                <h2>€2.4M</h2>
                <p>+15% vs projection</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Graphiques principaux
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Évolution des Scores Stratégiques")
            self.plot_score_evolution()
        
        with col2:
            st.markdown("### 🎯 Répartition par Priorité")
            self.plot_priority_distribution()
        
        # Tableau des analyses récentes
        st.markdown("### 📋 Analyses Récentes")
        self.show_recent_analyses()
        
        # Signaux d'alerte
        st.markdown("### ⚠️ Signaux d'Alerte")
        self.show_alert_signals()
    
    def show_analysis(self):
        st.markdown("## 🔍 Analyse Stratégique")
        
        # Interface d'analyse
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📝 Contenu à Analyser")
            content = st.text_area(
                "Entrez le contenu à analyser (article, rapport, etc.)",
                height=300,
                placeholder="Collez ici le contenu à analyser selon le format CRAFT..."
            )
            
            # Options d'analyse
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                focus_area = st.selectbox(
                    "Domaine de Focus",
                    ["Concurrence", "Marché", "Technologie", "Réglementation", "Général"]
                )
            with col_b:
                urgency_level = st.selectbox(
                    "Niveau d'Urgence",
                    ["Critique", "Élevé", "Modéré", "Faible"]
                )
            with col_c:
                company_size = st.selectbox(
                    "Taille d'Entreprise",
                    ["Startup", "PME", "Grande Entreprise", "Multinationale"]
                )
        
        with col2:
            st.markdown("### ⚙️ Paramètres")
            
            # Modèle IA
            ai_model = st.selectbox(
                "Modèle d'Analyse",
                ["Claude-3-Sonnet", "GPT-4", "Gemini-Pro", "Custom Model"]
            )
            
            # Critères de scoring
            st.markdown("**Critères de Scoring**")
            impact_weight = st.slider("Impact Business", 0.1, 1.0, 0.3, 0.1)
            urgency_weight = st.slider("Urgence Temporelle", 0.1, 1.0, 0.25, 0.1)
            complexity_weight = st.slider("Complexité Exécution", 0.1, 1.0, 0.2, 0.1)
            risk_weight = st.slider("Risque Concurrentiel", 0.1, 1.0, 0.15, 0.1)
            reliability_weight = st.slider("Fiabilité Source", 0.1, 1.0, 0.1, 0.1)
            
            # Bouton d'analyse
            if st.button("🚀 Lancer l'Analyse", type="primary"):
                if content:
                    with st.spinner("Analyse en cours..."):
                        analysis_result = self.analyzer.analyze_content(
                            content, focus_area, urgency_level, company_size,
                            ai_model, [impact_weight, urgency_weight, complexity_weight, 
                                     risk_weight, reliability_weight]
                        )
                        self.display_analysis_result(analysis_result)
                else:
                    st.error("Veuillez entrer du contenu à analyser.")
    
    def show_comparison(self):
        st.markdown("## 📈 Comparaison Multi-IA")
        
        # Sélection des analyses à comparer
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Sélection des Analyses")
            analyses = self.data_manager.get_all_analyses()
            
            if analyses:
                analysis_options = [f"{a['title']} ({a['date']})" for a in analyses]
                selected_analyses = st.multiselect(
                    "Sélectionnez les analyses à comparer",
                    analysis_options,
                    default=analysis_options[:3] if len(analysis_options) >= 3 else analysis_options
                )
                
                if st.button("🔄 Comparer", type="primary"):
                    if len(selected_analyses) >= 2:
                        self.show_comparison_results(selected_analyses)
                    else:
                        st.warning("Sélectionnez au moins 2 analyses pour la comparaison.")
            else:
                st.info("Aucune analyse disponible pour la comparaison.")
        
        with col2:
            st.markdown("### 📊 Métriques de Comparaison")
            if st.button("📈 Générer Rapport Comparatif"):
                self.generate_comparison_report()
    
    def show_configuration(self):
        st.markdown("## ⚙️ Configuration")
        
        # Paramètres généraux
        st.markdown("### 🔧 Paramètres Généraux")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Seuils d'Alerte**")
            critical_threshold = st.slider("Seuil Critique", 7, 10, 8)
            high_threshold = st.slider("Seuil Élevé", 5, 9, 6)
            moderate_threshold = st.slider("Seuil Modéré", 3, 7, 4)
            
            st.markdown("**Métriques de Suivi**")
            monitoring_frequency = st.selectbox(
                "Fréquence de Monitoring",
                ["Quotidien", "Hebdomadaire", "Mensuel"]
            )
        
        with col2:
            st.markdown("**API Configuration**")
            openai_key = st.text_input("OpenAI API Key", type="password")
            anthropic_key = st.text_input("Anthropic API Key", type="password")
            
            st.markdown("**Export**")
            export_format = st.selectbox(
                "Format d'Export",
                ["PDF", "Excel", "JSON", "CSV"]
            )
        
        # Sauvegarde
        if st.button("💾 Sauvegarder Configuration"):
            config = {
                "thresholds": {
                    "critical": critical_threshold,
                    "high": high_threshold,
                    "moderate": moderate_threshold
                },
                "monitoring_frequency": monitoring_frequency,
                "export_format": export_format
            }
            self.data_manager.save_config(config)
            st.success("Configuration sauvegardée !")
    
    def plot_score_evolution(self):
        # Données simulées pour l'exemple
        dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='M')
        scores = np.random.normal(7.2, 1.5, len(dates))
        
        df = pd.DataFrame({
            'Date': dates,
            'Score': scores
        })
        
        fig = px.line(df, x='Date', y='Score', 
                     title="Évolution des Scores Stratégiques",
                     labels={'Score': 'Score Moyen', 'Date': 'Période'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_priority_distribution(self):
        priorities = ['Critique', 'Élevé', 'Modéré', 'Faible']
        counts = [8, 12, 15, 5]
        
        fig = px.pie(values=counts, names=priorities, 
                    title="Répartition par Niveau de Priorité")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    def show_recent_analyses(self):
        # Données simulées
        data = {
            'Titre': ['Analyse Amazon IA', 'Rapport Tech Trends', 'Étude Marché SaaS'],
            'Date': ['2024-01-15', '2024-01-14', '2024-01-13'],
            'Score': [8.5, 7.2, 6.8],
            'Priorité': ['Critique', 'Élevé', 'Modéré'],
            'Modèle': ['Claude-3', 'GPT-4', 'Gemini']
        }
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    
    def show_alert_signals(self):
        alerts = [
            "🚨 Nouvelle entrée concurrente détectée dans le secteur SaaS",
            "⚠️ Changement réglementaire imminent en Europe",
            "📈 Hausse significative des investissements en IA générative"
        ]
        
        for alert in alerts:
            st.warning(alert)
    
    def display_analysis_result(self, result):
        st.markdown("## 📊 Résultat de l'Analyse")
        
        # Affichage du résultat formaté
        st.markdown(result)
        
        # Sauvegarde
        if st.button("💾 Sauvegarder l'Analyse"):
            self.data_manager.save_analysis(result)
            st.success("Analyse sauvegardée !")
    
    def show_comparison_results(self, selected_analyses):
        st.markdown("## 📊 Résultats de la Comparaison")
        
        # Graphique de comparaison des scores
        fig = go.Figure()
        
        # Données simulées
        models = ['Claude-3', 'GPT-4', 'Gemini']
        criteria = ['Impact', 'Urgence', 'Complexité', 'Risque', 'Fiabilité']
        
        for i, model in enumerate(models):
            scores = np.random.uniform(5, 9, len(criteria))
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=criteria,
                fill='toself',
                name=model
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Comparaison des Scores par Critère"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def generate_comparison_report(self):
        st.markdown("## 📋 Rapport Comparatif")
        
        # Génération du rapport
        report = """
        ### 📊 Synthèse Comparative
        
        **Convergences Principales :**
        - Impact Business : Consensus élevé (7.5-8.2/10)
        - Urgence Temporelle : Divergence modérée (6.8-8.1/10)
        
        **Divergences Notables :**
        - Complexité d'Exécution : Écart important entre modèles
        - Risque Concurrentiel : Évaluations variables selon la méthodologie
        
        **Recommandations :**
        1. Approfondir l'analyse de la complexité d'exécution
        2. Valider les hypothèses sur les risques concurrentiels
        3. Consolider les métriques de fiabilité des sources
        """
        
        st.markdown(report)

if __name__ == "__main__":
    dashboard = StrategicDashboard()
    dashboard.main() 