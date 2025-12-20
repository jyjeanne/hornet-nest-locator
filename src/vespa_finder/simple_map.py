"""Simple standalone HTML map generator that works in embedded browsers."""

import os
from typing import List

from .geo_utils import destination_point
from .models import HiveLocation, Observation


class MapGenerationError(Exception):
    """Exception raised when map generation fails."""

    pass


class SimpleMapGenerator:
    """Generate simple HTML maps using Leaflet.js with embedded tiles."""

    def create_simple_map(
        self,
        observations: List[Observation],
        hive_locations: List[HiveLocation],
        output_file: str,
    ) -> str:
        """
        Create a simple HTML map that works in embedded browsers.

        Supports multiple observations and hive locations for triangulation display.

        Args:
            observations: List of hornet observations to display
            hive_locations: List of calculated hive locations
            output_file: Path to save the HTML file

        Returns:
            Path to created HTML file

        Raises:
            ValueError: If no observations provided
            MapGenerationError: If file cannot be written
        """
        if not observations:
            raise ValueError("Need at least one observation")

        # Calculate map bounds to fit all points
        all_lats = [obs.latitude for obs in observations]
        all_lons = [obs.longitude for obs in observations]

        for hive in hive_locations:
            all_lats.append(hive.latitude)
            all_lons.append(hive.longitude)

        min_lat = min(all_lats) - 0.005
        max_lat = max(all_lats) + 0.005
        min_lon = min(all_lons) - 0.005
        max_lon = max(all_lons) + 0.005

        # Calculate center point
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2

        html_content = self._generate_html_header(center_lat, center_lon)
        html_content += self._generate_observations_js(observations)
        html_content += self._generate_hive_locations_js(observations, hive_locations)
        html_content += self._generate_map_bounds_js(min_lat, max_lat, min_lon, max_lon)
        html_content += self._generate_legend_js(len(observations), len(hive_locations))
        html_content += self._generate_html_footer()

        # Write file with error handling
        try:
            # Ensure directory exists
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)
        except PermissionError as e:
            raise MapGenerationError(f"Permission denied writing to {output_file}: {e}")
        except OSError as e:
            raise MapGenerationError(f"Failed to write map file {output_file}: {e}")

        return output_file

    def _generate_html_header(self, center_lat: float, center_lon: float) -> str:
        """Generate HTML header with Leaflet setup."""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hornet Hive Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }}
        #map {{
            position: absolute;
            top: 0;
            bottom: 0;
            width: 100%;
            height: 100%;
        }}
        .legend {{
            background: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.4);
        }}
        .legend h4 {{
            margin: 0 0 10px 0;
            font-size: 14px;
        }}
        .legend-item {{
            margin: 5px 0;
            font-size: 12px;
        }}
        .legend-item span {{
            display: inline-block;
            width: 20px;
            height: 2px;
            margin-right: 5px;
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        // Initialize map
        var map = L.map('map').setView([{center_lat}, {center_lon}], 14);

        // Add OpenStreetMap tiles
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }}).addTo(map);

        // Color palette for multiple observations
        var colors = ['blue', 'green', 'purple', 'orange', 'darkred', 'darkblue', 'darkgreen', 'cadetblue'];
"""

    def _generate_observations_js(self, observations: List[Observation]) -> str:
        """Generate JavaScript for observation markers."""
        js = ""
        for i, obs in enumerate(observations):
            color = f"colors[{i % 8}]"
            marker_url = self._get_marker_url(i)

            js += f"""
        // Observation point {i + 1}
        var obsMarker{i} = L.marker([{obs.latitude}, {obs.longitude}], {{
            icon: L.icon({{
                iconUrl: '{marker_url}',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            }})
        }}).addTo(map);

        obsMarker{i}.bindPopup(`
            <div style="font-family: Arial; width: 220px;">
                <h4>🔵 Observation Point {i + 1}</h4>
                <b>Location:</b> {obs.latitude:.6f}, {obs.longitude:.6f}<br>
                <b>Time:</b> {obs.timestamp.strftime("%Y-%m-%d %H:%M:%S")}<br>
                <b>Bearing:</b> {obs.bearing}°<br>
                <b>Round trip:</b> {obs.round_trip_time:.0f}s ({obs.round_trip_time / 60:.1f}min)<br>
                <b>Distance:</b> {obs.estimated_distance:.0f}m
                {f"<br><b>Hornet mark:</b> {obs.hornet_color_mark}" if obs.hornet_color_mark else ""}
                {f"<br><b>Notes:</b> {obs.notes}" if obs.notes else ""}
            </div>
        `);

        // Flight direction arrow for observation {i + 1}
        var arrow{i}End = [{self._get_arrow_endpoint(obs)}];
        L.polyline([
            [{obs.latitude}, {obs.longitude}],
            arrow{i}End
        ], {{
            color: {color},
            weight: 3,
            opacity: 0.7
        }}).addTo(map).bindPopup('Observation {i + 1} - Flight direction: {obs.bearing}°');
"""
        return js

    def _get_marker_url(self, index: int) -> str:
        """Get marker URL for observation index."""
        colors = [
            "blue",
            "green",
            "violet",
            "orange",
            "red",
            "darkblue",
            "darkgreen",
            "cadetblue",
        ]
        color = colors[index % len(colors)]
        return f"https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-{color}.png"

    def _get_arrow_endpoint(self, obs: Observation) -> str:
        """Calculate arrow endpoint coordinates."""
        arrow_lat, arrow_lon = destination_point(obs.latitude, obs.longitude, obs.bearing, 100)
        return f"{arrow_lat}, {arrow_lon}"

    def _generate_hive_locations_js(
        self, observations: List[Observation], hive_locations: List[HiveLocation]
    ) -> str:
        """Generate JavaScript for hive location markers."""
        if not hive_locations:
            return ""

        js = ""
        for i, hive in enumerate(hive_locations):
            # Find corresponding observation for flight path
            obs_index = min(i, len(observations) - 1)
            obs = observations[obs_index]

            js += f"""
        // Hive location {i + 1}
        var hiveMarker{i} = L.marker([{hive.latitude}, {hive.longitude}], {{
            icon: L.icon({{
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            }})
        }}).addTo(map);

        hiveMarker{i}.bindPopup(`
            <div style="font-family: Arial; width: 220px;">
                <h4 style="color: red;">🔴 Estimated Hive{" " + str(i + 1) if len(hive_locations) > 1 else ""}</h4>
                <b>Location:</b> {hive.latitude:.6f}, {hive.longitude:.6f}<br>
                <b>Distance:</b> {hive.distance_from_observer:.0f}m ({hive.distance_from_observer / 1000:.2f}km)<br>
                <b>Bearing:</b> {hive.bearing_from_observer:.1f}°<br>
                <b>Confidence:</b> ±{hive.confidence_radius:.0f}m<br>
                <b>Method:</b> {hive.calculation_method}<br>
                <br>
                <a href="https://www.google.com/maps?q={hive.latitude},{hive.longitude}" target="_blank">
                    Open in Google Maps
                </a>
            </div>
        `);

        // Search zone circle for hive {i + 1}
        L.circle([{hive.latitude}, {hive.longitude}], {{
            color: 'red',
            fillColor: 'red',
            fillOpacity: 0.1,
            radius: {hive.confidence_radius}
        }}).addTo(map).bindPopup('Search zone {i + 1}: ±{hive.confidence_radius:.0f}m');
"""

        # Draw flight paths from all observations to hive(s)
        # For triangulation, draw from each observation to the triangulated hive
        if len(hive_locations) == 1 and len(observations) > 1:
            # Triangulation case: draw from all observations to single hive
            hive = hive_locations[0]
            for obs_i, obs in enumerate(observations):
                js += f"""
        // Flight path from observation {obs_i + 1} to triangulated hive
        L.polyline([
            [{obs.latitude}, {obs.longitude}],
            [{hive.latitude}, {hive.longitude}]
        ], {{
            color: 'red',
            weight: 2,
            opacity: 0.5,
            dashArray: '10, 5'
        }}).addTo(map).bindPopup('Flight path from observation {obs_i + 1}');
"""
        else:
            # Single observation or multiple hives: pair observations with hives
            for i, hive in enumerate(hive_locations):
                obs_index = min(i, len(observations) - 1)
                obs = observations[obs_index]
                js += f"""
        // Flight path from observation {obs_index + 1} to hive {i + 1}
        L.polyline([
            [{obs.latitude}, {obs.longitude}],
            [{hive.latitude}, {hive.longitude}]
        ], {{
            color: 'red',
            weight: 2,
            opacity: 0.5,
            dashArray: '10, 5'
        }}).addTo(map).bindPopup('Estimated flight path ({hive.distance_from_observer:.0f}m)');
"""

        return js

    def _generate_map_bounds_js(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> str:
        """Generate JavaScript to fit map bounds."""
        return f"""
        // Fit bounds to show all markers
        var bounds = L.latLngBounds([
            [{min_lat}, {min_lon}],
            [{max_lat}, {max_lon}]
        ]);
        map.fitBounds(bounds);
"""

    def _generate_legend_js(self, num_observations: int, num_hives: int) -> str:
        """Generate JavaScript for map legend."""
        obs_text = f"Observation Point{'s' if num_observations > 1 else ''} ({num_observations})"
        hive_text = f"Estimated Hive{'s' if num_hives > 1 else ''} ({num_hives})"

        return f"""
        // Add legend
        var legend = L.control({{position: 'topright'}});
        legend.onAdd = function(map) {{
            var div = L.DomUtil.create('div', 'legend');
            div.innerHTML = `
                <h4>Hornet Nest Locator</h4>
                <div class="legend-item">🔵 {obs_text}</div>
                <div class="legend-item">🔴 {hive_text}</div>
                <div class="legend-item"><span style="background: blue;"></span> Flight direction</div>
                <div class="legend-item"><span style="background: red; border: 1px dashed red;"></span> Flight path</div>
                <div class="legend-item">⭕ Search zone</div>
            `;
            return div;
        }};
        legend.addTo(map);
"""

    def _generate_html_footer(self) -> str:
        """Generate HTML footer."""
        return """
    </script>
</body>
</html>
"""
