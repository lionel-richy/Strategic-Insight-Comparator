import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        self.analyses_file = os.path.join(self.data_dir, "analyses.json")
        self.config_file = os.path.join(self.data_dir, "config.json")
        self.metrics_file = os.path.join(self.data_dir, "metrics.json")
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Crée le répertoire de données s'il n'existe pas"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_analysis(self, analysis_content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Sauvegarde une analyse dans le fichier JSON"""
        try:
            # Charger les analyses existantes
            analyses = self.load_analyses()
            
            # Créer un nouvel enregistrement
            new_analysis = {
                "id": self._generate_id(),
                "content": analysis_content,
                "date": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            # Ajouter l'analyse
            analyses.append(new_analysis)
            
            # Sauvegarder
            with open(self.analyses_file, 'w', encoding='utf-8') as f:
                json.dump(analyses, f, ensure_ascii=False, indent=2)
            
            return True
        
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'analyse: {e}")
            return False
    
    def load_analyses(self) -> List[Dict[str, Any]]:
        """Charge toutes les analyses depuis le fichier JSON"""
        try:
            if os.path.exists(self.analyses_file):
                with open(self.analyses_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Erreur lors du chargement des analyses: {e}")
            return []
    
    def get_all_analyses(self) -> List[Dict[str, Any]]:
        """Récupère toutes les analyses avec formatage pour l'affichage"""
        analyses = self.load_analyses()
        formatted_analyses = []
        
        for analysis in analyses:
            # Extraire le titre de l'analyse
            title = self._extract_title_from_analysis(analysis["content"])
            
            formatted_analysis = {
                "id": analysis["id"],
                "title": title,
                "date": analysis["date"],
                "content": analysis["content"],
                "metadata": analysis.get("metadata", {})
            }
            formatted_analyses.append(formatted_analysis)
        
        return formatted_analyses
    
    def get_analysis_by_id(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Récupère une analyse spécifique par son ID"""
        analyses = self.load_analyses()
        for analysis in analyses:
            if analysis["id"] == analysis_id:
                return analysis
        return None
    
    def delete_analysis(self, analysis_id: str) -> bool:
        """Supprime une analyse par son ID"""
        try:
            analyses = self.load_analyses()
            analyses = [a for a in analyses if a["id"] != analysis_id]
            
            with open(self.analyses_file, 'w', encoding='utf-8') as f:
                json.dump(analyses, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'analyse: {e}")
            return False
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Sauvegarde la configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration: {e}")
            return False
    
    def load_config(self) -> Dict[str, Any]:
        """Charge la configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self._get_default_config()
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            return self._get_default_config()
    
    def save_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Sauvegarde les métriques de performance"""
        try:
            # Charger les métriques existantes
            all_metrics = self.load_metrics()
            
            # Ajouter timestamp
            metrics["timestamp"] = datetime.now().isoformat()
            
            # Ajouter les nouvelles métriques
            all_metrics.append(metrics)
            
            # Garder seulement les 100 dernières entrées
            if len(all_metrics) > 100:
                all_metrics = all_metrics[-100:]
            
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(all_metrics, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des métriques: {e}")
            return False
    
    def load_metrics(self) -> List[Dict[str, Any]]:
        """Charge les métriques de performance"""
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Erreur lors du chargement des métriques: {e}")
            return []
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Récupère les données pour le dashboard"""
        analyses = self.get_all_analyses()
        metrics = self.load_metrics()
        
        # Calculer les statistiques
        total_analyses = len(analyses)
        
        # Scores moyens
        scores = []
        priorities = {"CRITIQUE": 0, "ÉLEVÉ": 0, "MODÉRÉ": 0, "FAIBLE": 0}
        
        for analysis in analyses:
            # Extraire les scores de l'analyse
            extracted_metrics = self._extract_metrics_from_analysis(analysis["content"])
            if extracted_metrics["global_score"] > 0:
                scores.append(extracted_metrics["global_score"])
            
            # Compter les priorités
            priority = extracted_metrics.get("priority_level", "MODÉRÉ")
            if priority in priorities:
                priorities[priority] += 1
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Évolution des scores (dernières 10 analyses)
        recent_scores = scores[-10:] if len(scores) >= 10 else scores
        
        # ROI estimé (simulation basée sur les scores)
        estimated_roi = sum(scores) * 100000 if scores else 0  # €100k par point de score
        
        dashboard_data = {
            "total_analyses": total_analyses,
            "average_score": round(avg_score, 1),
            "critical_priorities": priorities["CRITIQUE"],
            "estimated_roi": estimated_roi,
            "recent_scores": recent_scores,
            "priority_distribution": priorities,
            "recent_analyses": analyses[-5:] if len(analyses) >= 5 else analyses
        }
        
        return dashboard_data
    
    def export_analyses(self, format: str = "json") -> str:
        """Exporte les analyses dans différents formats"""
        analyses = self.get_all_analyses()
        
        if format.lower() == "json":
            return json.dumps(analyses, ensure_ascii=False, indent=2)
        
        elif format.lower() == "csv":
            # Convertir en DataFrame pour export CSV
            df_data = []
            for analysis in analyses:
                df_data.append({
                    "ID": analysis["id"],
                    "Titre": analysis["title"],
                    "Date": analysis["date"],
                    "Contenu": analysis["content"][:500] + "..." if len(analysis["content"]) > 500 else analysis["content"]
                })
            
            df = pd.DataFrame(df_data)
            return df.to_csv(index=False)
        
        elif format.lower() == "excel":
            # Créer un fichier Excel temporaire
            df_data = []
            for analysis in analyses:
                df_data.append({
                    "ID": analysis["id"],
                    "Titre": analysis["title"],
                    "Date": analysis["date"],
                    "Contenu": analysis["content"][:500] + "..." if len(analysis["content"]) > 500 else analysis["content"]
                })
            
            df = pd.DataFrame(df_data)
            excel_file = os.path.join(self.data_dir, "analyses_export.xlsx")
            df.to_excel(excel_file, index=False)
            return excel_file
        
        else:
            raise ValueError(f"Format d'export non supporté: {format}")
    
    def _generate_id(self) -> str:
        """Génère un ID unique pour une analyse"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _extract_title_from_analysis(self, analysis_content: str) -> str:
        """Extrait le titre d'une analyse depuis son contenu"""
        lines = analysis_content.split('\n')
        for line in lines:
            if line.startswith('# 📈 ANALYSE STRATÉGIQUE -'):
                return line.replace('# 📈 ANALYSE STRATÉGIQUE -', '').strip()
            elif line.startswith('#'):
                return line.replace('#', '').strip()
        return "Analyse sans titre"
    
    def _extract_metrics_from_analysis(self, analysis_content: str) -> Dict[str, Any]:
        """Extrait les métriques d'une analyse"""
        import re
        
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
            global_score_match = re.search(r'SCORE GLOBAL DE PRIORITÉ :\s*([\d.]+)/10', analysis_content)
            if global_score_match:
                metrics["global_score"] = float(global_score_match.group(1))
            
            # Extraction du niveau de priorité
            priority_match = re.search(r'Niveau :\s*([A-ZÉ]+)', analysis_content)
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
                match = re.search(pattern, analysis_content, re.DOTALL)
                if match:
                    metrics[key] = float(match.group(1))
        
        except Exception as e:
            print(f"Erreur lors de l'extraction des métriques: {e}")
        
        return metrics
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Retourne la configuration par défaut"""
        return {
            "thresholds": {
                "critical": 8,
                "high": 6,
                "moderate": 4
            },
            "monitoring_frequency": "Hebdomadaire",
            "export_format": "JSON",
            "ai_models": {
                "claude_enabled": True,
                "gpt4_enabled": True,
                "gemini_enabled": False
            }
        }
    
    def search_analyses(self, query: str) -> List[Dict[str, Any]]:
        """Recherche dans les analyses"""
        analyses = self.get_all_analyses()
        results = []
        
        query_lower = query.lower()
        
        for analysis in analyses:
            if (query_lower in analysis["title"].lower() or 
                query_lower in analysis["content"].lower()):
                results.append(analysis)
        
        return results
    
    def get_analyses_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """Filtre les analyses par niveau de priorité"""
        analyses = self.get_all_analyses()
        filtered_analyses = []
        
        for analysis in analyses:
            extracted_metrics = self._extract_metrics_from_analysis(analysis["content"])
            if extracted_metrics["priority_level"] == priority:
                filtered_analyses.append(analysis)
        
        return filtered_analyses
    
    def get_analyses_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Filtre les analyses par plage de dates"""
        analyses = self.get_all_analyses()
        filtered_analyses = []
        
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        
        for analysis in analyses:
            analysis_dt = datetime.fromisoformat(analysis["date"])
            if start_dt <= analysis_dt <= end_dt:
                filtered_analyses.append(analysis)
        
        return filtered_analyses 