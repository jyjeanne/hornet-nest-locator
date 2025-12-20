"""Wildlife database API integration for reporting hornet observations."""

import json
import logging
from typing import Dict, List, Optional, Union
from urllib.parse import urlencode

import requests

from .models import HiveLocation, Observation


class WildlifeAPIError(Exception):
    """Exception raised when wildlife API operations fail."""
    pass


class WildlifeReporter:
    """
    Report hornet observations to wildlife conservation databases.
    
    Supports multiple European databases for Asian hornet reporting.
    """
    
    # Wildlife database endpoints
    DATABASES = {
        "vespawatch": {
            "name": "Vespawatch (Flanders, Belgium)",
            "url": "https://vespawatch.be",
            "api_url": None,  # No public API, website submission only
            "website": "https://vespawatch.be/melding",
        },
        "waarneming": {
            "name": "Waarneming.nl (Netherlands)",
            "url": "https://waarneming.nl",
            "api_url": "https://waarneming.nl/api/v1/observations",
            "website": "https://waarneming.nl/soort/invasieve_wesp",
            "requires_auth": True,
        },
        "observatoire": {
            "name": "Observatoire Biodiversité Wallonie (Wallonia, Belgium)",
            "url": "https://observatoire.biodiversite.wallonie.be",
            "api_url": None,  # No public API, website submission only
            "website": "https://observatoire.biodiversite.wallonie.be/frelon-asiatique",
        },
    }
    
    def __init__(self):
        """Initialize wildlife reporter."""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "VespaFinder/0.3.0 (+https://github.com/YOUR-USERNAME/vespa-finder)",
            "Accept": "application/json",
        })
        
    def get_available_databases(self) -> List[Dict[str, str]]:
        """Get list of available wildlife databases."""
        return [
            {
                "id": db_id,
                "name": info["name"],
                "url": info["url"],
                "has_api": info["api_url"] is not None,
                "website": info["website"],
            }
            for db_id, info in self.DATABASES.items()
        ]
    
    def report_to_vespawatch(self, observation: Observation, hive_location: HiveLocation) -> Dict[str, str]:
        """
        Generate Vespawatch report (website submission only).
        
        Returns instructions for manual submission since Vespawatch doesn't have a public API.
        """
        return {
            "database": "vespawatch",
            "status": "manual_submission_required",
            "website": "https://vespawatch.be/melding",
            "instructions": (
                "Vespawatch requires manual submission. Please visit their website "
                "and enter the following details:"
            ),
            "data": self._prepare_vespawatch_data(observation, hive_location),
        }
    
    def report_to_waarneming(self, observation: Observation, hive_location: HiveLocation, 
                            api_key: Optional[str] = None) -> Dict[str, Union[str, bool]]:
        """
        Report to Waarneming.nl API.
        
        Note: This requires an API key from Waarneming.nl.
        """
        if not api_key:
            raise WildlifeAPIError(
                "Waarneming.nl API requires authentication. "
                "Please obtain an API key from https://waarneming.nl"
            )
        
        db_info = self.DATABASES["waarneming"]
        if not db_info["api_url"]:
            raise WildlifeAPIError("Waarneming.nl API endpoint not configured")
        
        # Prepare observation data
        observation_data = self._prepare_waarneming_data(observation, hive_location)
        
        try:
            # Add authentication
            self.session.headers["Authorization"] = f"Bearer {api_key}"
            
            # Submit observation
            response = self.session.post(
                db_info["api_url"],
                json=observation_data,
                timeout=30,
            )
            
            response.raise_for_status()
            result = response.json()
            
            return {
                "database": "waarneming",
                "status": "success",
                "observation_id": result.get("id"),
                "url": result.get("url"),
                "message": "Observation successfully submitted to Waarneming.nl",
            }
            
        except requests.exceptions.RequestException as e:
            raise WildlifeAPIError(f"Failed to submit to Waarneming.nl: {e}")
        finally:
            # Clean up authentication header
            self.session.headers.pop("Authorization", None)
    
    def report_to_observatoire(self, observation: Observation, hive_location: HiveLocation) -> Dict[str, str]:
        """
        Generate Observatoire Biodiversité Wallonie report (website submission only).
        
        Returns instructions for manual submission.
        """
        return {
            "database": "observatoire",
            "status": "manual_submission_required",
            "website": "https://observatoire.biodiversite.wallonie.be/frelon-asiatique",
            "instructions": (
                "Observatoire Biodiversité Wallonie requires manual submission. "
                "Please visit their website and enter the following details:"
            ),
            "data": self._prepare_observatoire_data(observation, hive_location),
        }
    
    def _prepare_vespawatch_data(self, observation: Observation, hive_location: HiveLocation) -> Dict[str, str]:
        """Prepare data for Vespawatch submission."""
        return {
            "species": "Vespa velutina (Asian hornet)",
            "observation_date": observation.timestamp.strftime("%Y-%m-%d"),
            "observation_time": observation.timestamp.strftime("%H:%M"),
            "observer_location": f"{observation.latitude}, {observation.longitude}",
            "estimated_hive_location": f"{hive_location.latitude}, {hive_location.longitude}",
            "distance_from_observer": f"{hive_location.distance_from_observer:.0f} meters",
            "bearing": f"{observation.bearing}°",
            "round_trip_time": f"{observation.round_trip_time:.0f} seconds",
            "method": "Vespawatchers empirical method (100m/min)",
            "confidence": f"±{hive_location.confidence_radius:.0f} meters",
            "notes": observation.notes or "Submitted via VespaFinder",
        }
    
    def _prepare_waarneming_data(self, observation: Observation, hive_location: HiveLocation) -> Dict[str, Union[str, int, float]]:
        """Prepare data for Waarneming.nl API."""
        return {
            "species": "Vespa velutina",
            "latitude": observation.latitude,
            "longitude": observation.longitude,
            "date": observation.timestamp.strftime("%Y-%m-%d"),
            "time": observation.timestamp.strftime("%H:%M"),
            "count": 1,
            "notes": (
                f"Asian hornet observation. Estimated hive location: "
                f"{hive_location.latitude}, {hive_location.longitude} (±{hive_location.confidence_radius:.0f}m). "
                f"Method: Vespawatchers empirical (100m/min). "
                f"Distance: {hive_location.distance_from_observer:.0f}m, Bearing: {observation.bearing}°"
            ),
            "accuracy": hive_location.confidence_radius,
            "source": "VespaFinder 0.3.0",
        }
    
    def _prepare_observatoire_data(self, observation: Observation, hive_location: HiveLocation) -> Dict[str, str]:
        """Prepare data for Observatoire Biodiversité Wallonie submission."""
        return {
            "species": "Frelon asiatique (Vespa velutina)",
            "date_observation": observation.timestamp.strftime("%d/%m/%Y"),
            "heure_observation": observation.timestamp.strftime("%H:%M"),
            "lieu_observation": f"{observation.latitude}, {observation.longitude}",
            "emplacement_nid_estime": f"{hive_location.latitude}, {hive_location.longitude}",
            "distance_observateur": f"{hive_location.distance_from_observer:.0f} mètres",
            "cap": f"{observation.bearing}°",
            "temps_parcours": f"{observation.round_trip_time:.0f} secondes",
            "methode": "Méthode empirique Vespawatchers (100m/min)",
            "precision": f"±{hive_location.confidence_radius:.0f} mètres",
            "remarques": observation.notes or "Soumis via VespaFinder",
        }
    
    def generate_combined_report(self, observation: Observation, hive_location: HiveLocation) -> Dict[str, Dict]:
        """Generate a combined report for all databases."""
        return {
            "vespawatch": self.report_to_vespawatch(observation, hive_location),
            "waarneming": {
                "database": "waarneming",
                "status": "api_available",
                "requires_auth": True,
                "website": "https://waarneming.nl",
                "api_info": "API key required for automatic submission",
            },
            "observatoire": self.report_to_observatoire(observation, hive_location),
        }
    
    def get_reporting_guide(self, country: str = "belgium") -> str:
        """Get reporting guide for specific country/region."""
        guides = {
            "belgium": {
                "flanders": {
                    "name": "Flanders (Vlaanderen)",
                    "database": "Vespawatch",
                    "website": "https://vespawatch.be/melding",
                    "phone": "+32 78 15 15 15",
                    "email": "info@vespawatch.be",
                },
                "wallonia": {
                    "name": "Wallonia (Wallonie)",
                    "database": "Observatoire Biodiversité",
                    "website": "https://observatoire.biodiversite.wallonie.be/frelon-asiatique",
                    "phone": "+32 81 33 59 99",
                    "email": "biodiversite@spw.wallonie.be",
                },
            },
            "netherlands": {
                "name": "Netherlands (Nederland)",
                "database": "Waarneming.nl",
                "website": "https://waarneming.nl/soort/invasieve_wesp",
                "phone": None,
                "email": None,
            },
            "france": {
                "name": "France",
                "database": "Frelons Asiatiques",
                "website": "https://www.frelonsasiatiques.fr",
                "phone": "18 (for emergency nest removal)",
                "email": None,
            },
        }
        
        if country not in guides:
            country = "belgium"  # Default to Belgium
        
        if country == "belgium":
            return guides[country]
        else:
            return guides[country]