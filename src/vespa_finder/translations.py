"""
Language translations for Hornet Nest Locator GUI
"""

TRANSLATIONS = {
    "en": {
        # Window title
        "window_title": "🐝 Hornet Nest Locator - Professional Edition",
        # Main sections
        "input_panel_title": "OBSERVATION DATA",
        "results_panel_title": "CALCULATION RESULTS",
        # GPS Section
        "gps_section": "GPS Position",
        "latitude": "Latitude:",
        "longitude": "Longitude:",
        "gps_help": "GPS Help",
        # Flight Data Section
        "flight_section": "Flight Data",
        "bearing": "Bearing (0-360°):",
        "bearing_help": "Direction where hornet flew\n0°=North, 90°=East, 180°=South, 270°=West",
        "round_trip": "Round Trip Time",
        "minutes": "Minutes:",
        "seconds": "Seconds:",
        # Optional Data
        "optional_section": "Optional Data",
        "hornet_mark": "Hornet Color Mark:",
        "speed": "Speed (m/s):",
        "speed_note": "Leave empty to use empirical method (recommended)",
        "notes": "Notes:",
        # Buttons
        "calculate": "CALCULATE HIVE LOCATION",
        "view_map": "View Map",
        "print_map": "Print Map",
        "save_report": "Save Report",
        "clear": "Clear Form",
        # Placeholders
        "example": "e.g.",
        "optional": "Optional",
        "add_notes": "Add observations, weather conditions, etc.",
        "warning_measure": "⚠️ Measure multiple times!",
        # Messages
        "success_title": "Success",
        "success_message": """✅ Hive location calculated!

📊 Results displayed
🗺️ Interactive map opened in browser

📁 Map saved to:
{filename}

The map shows:
  🔵 Your observation point
  🔴 Estimated hive location
  ⭕ Red circle = search zone

Click 'View Map' to reopen""",
        "error_title": "Input Error",
        "error_message": "Invalid input:\n{error}",
        "calc_error_title": "Error",
        "calc_error_message": "Calculation error:\n{error}",
        "no_map_title": "No Map",
        "no_map_message": "Please calculate a hive location first.",
        "print_title": "Print Map",
        "print_message": "Map opened in browser.\n\nPress Ctrl+P in your browser to print the map.",
        "no_data_title": "No Data",
        "no_data_message": "Please calculate a location first.",
        "saved_title": "Saved",
        "saved_message": "Report saved to:\n{filename}",
        "save_error_title": "Save Error",
        "save_error_message": "Could not save:\n{error}",
        "map_error_title": "Map Error",
        "map_error_message": "Could not generate map:\n{error}",
        "gps_help_title": "GPS Help",
        "gps_help_message": """Right-click on your location in Google Maps
and select 'What's here?' to get coordinates.

Format: Decimal degrees
Example: 45.764043, 4.835659""",
        # Results template
        "results_header": "CALCULATION RESULTS",
        "observation_point": "OBSERVATION POINT:",
        "location": "Location:",
        "time": "Time:",
        "hornet_mark_label": "Hornet mark:",
        "flight_data": "FLIGHT DATA:",
        "direction": "Direction:",
        "round_trip_time": "Round trip time:",
        "empirical_method": "📍 EMPIRICAL METHOD (RECOMMENDED - Vespawatchers)",
        "empirical_formula": "Formula: 100 meters = 1 minute round trip",
        "calculated_distance": "Calculated distance:",
        "estimated_hive": "📌 ESTIMATED HIVE LOCATION:",
        "coordinates": "Coordinates:",
        "bearing_from_you": "Bearing from you:",
        "confidence_radius": "Confidence radius:",
        "search_zone_note": "(This is your search zone - shown as red circle on map)",
        "gps_nav": "🗺️  GPS COORDINATES FOR NAVIGATION:",
        "google_maps": "Google Maps:",
        "practice_note": "⚠️  Note: In practice, nest is often slightly further than calculated",
        "theoretical_method": "📊 THEORETICAL METHOD (For Comparison Only)",
        "theoretical_formula": "Formula: distance = (speed × time) / 2",
        "speed_used": "Speed used:",
        "difference": "Difference from empirical:",
        "recommended_method": "⚠️ Recommended method: EMPIRICAL (100m/min standard)",
        "notes_label": "📝 NOTES:",
        "map_info": "🗺️ MAP INFORMATION",
        "map_opened": "Interactive map opened in your browser.",
        "map_saved": "Map saved to:",
        "map_features": """Map features:
🔵 Blue marker = Your observation point
🔴 Red marker = Estimated hive location
⭕ Red circle = Search zone (±{radius}m)
➡️ Blue line = Flight direction
--- Red dashed = Flight path""",
        "map_actions": """Actions:
• Zoom in/out with mouse wheel
• Click markers for details
• Click "View Map" to reopen
• Click "Print" to print""",
        "next_steps": "⚠️  NEXT STEPS & SAFETY",
        "equipment": """Equipment:
✓ Binoculars 8×42 (ESSENTIAL!)
✓ Wick pot, markers, butterfly net""",
        "search": """Search:
✓ Navigate to red circle area
✓ Check trees, sheds, ground, hedges
✓ Scan with binoculars""",
        "safety": """Safety:
✓ NEVER approach alone
✓ Use protection
✓ Contact professionals
✓ Report: vespawatch.be""",
    },
    "fr": {
        # Titre de fenêtre
        "window_title": "🐝 Localisateur de Nids de Frelons - Édition Professionnelle",
        # Sections principales
        "input_panel_title": "DONNÉES D'OBSERVATION",
        "results_panel_title": "RÉSULTATS DU CALCUL",
        # Section GPS
        "gps_section": "Position GPS",
        "latitude": "Latitude :",
        "longitude": "Longitude :",
        "gps_help": "Aide GPS",
        # Section Données de Vol
        "flight_section": "Données de Vol",
        "bearing": "Cap (0-360°) :",
        "bearing_help": "Direction du vol du frelon\n0°=Nord, 90°=Est, 180°=Sud, 270°=Ouest",
        "round_trip": "Temps d'Aller-Retour",
        "minutes": "Minutes :",
        "seconds": "Secondes :",
        # Données optionnelles
        "optional_section": "Données Optionnelles",
        "hornet_mark": "Marque Couleur du Frelon :",
        "speed": "Vitesse (m/s) :",
        "speed_note": "Laisser vide pour utiliser la méthode empirique (recommandé)",
        "notes": "Notes :",
        # Boutons
        "calculate": "CALCULER LA POSITION DU NID",
        "view_map": "Voir la Carte",
        "print_map": "Imprimer",
        "save_report": "Sauvegarder",
        "clear": "Effacer",
        # Placeholders
        "example": "ex.",
        "optional": "Optionnel",
        "add_notes": "Ajoutez observations, conditions météo, etc.",
        "warning_measure": "⚠️ Mesurez plusieurs fois !",
        # Messages
        "success_title": "Succès",
        "success_message": """✅ Position du nid calculée !

📊 Résultats affichés
🗺️ Carte interactive ouverte dans le navigateur

📁 Carte sauvegardée :
{filename}

La carte montre :
  🔵 Votre point d'observation
  🔴 Position estimée du nid
  ⭕ Cercle rouge = zone de recherche

Cliquez sur 'Voir la Carte' pour rouvrir""",
        "error_title": "Erreur de Saisie",
        "error_message": "Saisie invalide :\n{error}",
        "calc_error_title": "Erreur",
        "calc_error_message": "Erreur de calcul :\n{error}",
        "no_map_title": "Pas de Carte",
        "no_map_message": "Veuillez d'abord calculer une position de nid.",
        "print_title": "Imprimer la Carte",
        "print_message": "Carte ouverte dans le navigateur.\n\nAppuyez sur Ctrl+P dans votre navigateur pour imprimer.",
        "no_data_title": "Pas de Données",
        "no_data_message": "Veuillez d'abord calculer une position.",
        "saved_title": "Sauvegardé",
        "saved_message": "Rapport sauvegardé dans :\n{filename}",
        "save_error_title": "Erreur de Sauvegarde",
        "save_error_message": "Impossible de sauvegarder :\n{error}",
        "map_error_title": "Erreur de Carte",
        "map_error_message": "Impossible de générer la carte :\n{error}",
        "gps_help_title": "Aide GPS",
        "gps_help_message": """Clic droit sur votre position dans Google Maps
et sélectionnez 'Plus d\'infos sur cet endroit' pour obtenir les coordonnées.

Format : Degrés décimaux
Exemple : 45.764043, 4.835659""",
        # Template de résultats
        "results_header": "RÉSULTATS DU CALCUL",
        "observation_point": "POINT D'OBSERVATION :",
        "location": "Position :",
        "time": "Heure :",
        "hornet_mark_label": "Marque du frelon :",
        "flight_data": "DONNÉES DE VOL :",
        "direction": "Direction :",
        "round_trip_time": "Temps d'aller-retour :",
        "empirical_method": "📍 MÉTHODE EMPIRIQUE (RECOMMANDÉE - Vespawatchers)",
        "empirical_formula": "Formule : 100 mètres = 1 minute aller-retour",
        "calculated_distance": "Distance calculée :",
        "estimated_hive": "📌 POSITION ESTIMÉE DU NID :",
        "coordinates": "Coordonnées :",
        "bearing_from_you": "Cap depuis votre position :",
        "confidence_radius": "Rayon de confiance :",
        "search_zone_note": "(C'est votre zone de recherche - cercle rouge sur la carte)",
        "gps_nav": "🗺️  COORDONNÉES GPS POUR NAVIGATION :",
        "google_maps": "Google Maps :",
        "practice_note": "⚠️  Note : En pratique, le nid est souvent légèrement plus loin que calculé",
        "theoretical_method": "📊 MÉTHODE THÉORIQUE (Pour Comparaison Uniquement)",
        "theoretical_formula": "Formule : distance = (vitesse × temps) / 2",
        "speed_used": "Vitesse utilisée :",
        "difference": "Différence avec empirique :",
        "recommended_method": "⚠️ Méthode recommandée : EMPIRIQUE (standard 100m/min)",
        "notes_label": "📝 NOTES :",
        "map_info": "🗺️ INFORMATIONS CARTE",
        "map_opened": "Carte interactive ouverte dans votre navigateur.",
        "map_saved": "Carte sauvegardée :",
        "map_features": """Éléments de la carte :
🔵 Marqueur bleu = Votre point d'observation
🔴 Marqueur rouge = Position estimée du nid
⭕ Cercle rouge = Zone de recherche (±{radius}m)
➡️ Ligne bleue = Direction du vol
--- Pointillés rouges = Trajet du vol""",
        "map_actions": """Actions :
• Zoomer avec la molette de la souris
• Cliquer sur les marqueurs pour les détails
• Cliquer sur "Voir la Carte" pour rouvrir
• Cliquer sur "Imprimer" pour imprimer""",
        "next_steps": "⚠️  PROCHAINES ÉTAPES & SÉCURITÉ",
        "equipment": """Équipement :
✓ Jumelles 8×42 (ESSENTIEL !)
✓ Pot à mèche, marqueurs, filet à papillons""",
        "search": """Recherche :
✓ Naviguer vers la zone du cercle rouge
✓ Vérifier arbres, cabanes, sol, haies
✓ Scanner avec les jumelles""",
        "safety": """Sécurité :
✓ NE JAMAIS approcher seul
✓ Utiliser des protections
✓ Contacter des professionnels
✓ Signaler : vespawatch.be""",
    },
}


def get_text(lang, key):
    """Get translated text for a key."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
