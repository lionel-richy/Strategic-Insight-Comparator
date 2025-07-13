#!/usr/bin/env python3
"""
Script de test pour vérifier le bon fonctionnement de l'application Strategic Intelligence Dashboard
"""

import sys
import os
import importlib.util

def test_imports():
    """Teste l'importation des modules requis"""
    print("🔍 Test des imports...")
    
    required_modules = [
        'streamlit',
        'pandas', 
        'plotly',
        'numpy',
        'json',
        'datetime'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - MANQUANT")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️ Modules manquants: {', '.join(missing_modules)}")
        print("Installez-les avec: pip install -r requirements.txt")
        return False
    
    print("✅ Tous les imports sont OK")
    return True

def test_local_modules():
    """Teste l'importation des modules locaux"""
    print("\n🔍 Test des modules locaux...")
    
    local_modules = [
        'strategic_analyzer',
        'data_manager'
    ]
    
    for module in local_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}.py")
        except ImportError as e:
            print(f"❌ {module}.py - ERREUR: {e}")
            return False
    
    print("✅ Tous les modules locaux sont OK")
    return True

def test_data_manager():
    """Teste le module DataManager"""
    print("\n🔍 Test du DataManager...")
    
    try:
        from data_manager import DataManager
        
        # Créer une instance
        dm = DataManager()
        print("✅ Instance DataManager créée")
        
        # Test de sauvegarde de configuration
        config = {"test": "value"}
        result = dm.save_config(config)
        print(f"✅ Sauvegarde config: {result}")
        
        # Test de chargement de configuration
        loaded_config = dm.load_config()
        print(f"✅ Chargement config: {loaded_config is not None}")
        
        # Test de récupération des analyses
        analyses = dm.get_all_analyses()
        print(f"✅ Récupération analyses: {len(analyses)} analyses trouvées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur DataManager: {e}")
        return False

def test_strategic_analyzer():
    """Teste le module StrategicAnalyzer"""
    print("\n🔍 Test du StrategicAnalyzer...")
    
    try:
        from strategic_analyzer import StrategicAnalyzer
        
        # Créer une instance
        analyzer = StrategicAnalyzer()
        print("✅ Instance StrategicAnalyzer créée")
        
        # Test d'analyse simulée
        test_content = """
        Amazon développe sa stratégie d'IA générative pour concurrencer ChatGPT.
        La société investit massivement dans le développement de modèles de langage
        et prévoit de lancer de nouveaux services d'IA dans les prochains mois.
        """
        
        result = analyzer.analyze_content(
            content=test_content,
            focus_area="Technologie",
            urgency_level="Élevé",
            company_size="Grande Entreprise",
            ai_model="Simulation",
            weights=[0.3, 0.25, 0.2, 0.15, 0.1]
        )
        
        print(f"✅ Analyse générée: {len(result)} caractères")
        print(f"✅ Contient 'ANALYSE STRATÉGIQUE': {'ANALYSE STRATÉGIQUE' in result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur StrategicAnalyzer: {e}")
        return False

def test_streamlit_app():
    """Teste que l'application Streamlit peut être importée"""
    print("\n🔍 Test de l'application Streamlit...")
    
    try:
        # Test d'importation de l'app
        spec = importlib.util.spec_from_file_location("app", "app.py")
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        print("✅ Application Streamlit importée avec succès")
        
        # Test de création de l'instance dashboard
        dashboard = app_module.StrategicDashboard()
        print("✅ Instance StrategicDashboard créée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur application Streamlit: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧠 Strategic Intelligence Dashboard - Tests\n")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Modules locaux", test_local_modules),
        ("DataManager", test_data_manager),
        ("StrategicAnalyzer", test_strategic_analyzer),
        ("Application Streamlit", test_streamlit_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur inattendue dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nRésultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 Tous les tests sont passés ! L'application est prête à être lancée.")
        print("\nPour lancer l'application:")
        print("streamlit run app.py")
    else:
        print(f"\n⚠️ {total - passed} test(s) ont échoué. Vérifiez les erreurs ci-dessus.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 