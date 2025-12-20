"""Map visualization for hornet observations and hive locations."""

import os
from typing import List, Optional

import folium

from .models import HiveLocation, Observation


class MapGenerationError(Exception):
    """Exception raised when map generation fails."""

    pass


class MapVisualizer:
    """Create interactive maps showing observations and hive locations."""

    def create_map(
        self,
        observations: List[Observation],
        hive_locations: List[HiveLocation],
        output_file: str = "hornet_map.html",
    ) -> str:
        """
        Create an interactive HTML map.

        Args:
            observations: List of observations to display
            hive_locations: List of calculated hive locations
            output_file: Output filename for HTML map

        Returns:
            Path to created HTML file
        """
        if not observations:
            raise ValueError("Need at least one observation to create map")

        # Center map on first observation
        center_lat = observations[0].latitude
        center_lon = observations[0].longitude

        # Create map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="OpenStreetMap")

        # Add observation points
        for i, obs in enumerate(observations, 1):
            # Observation marker
            folium.Marker(
                location=[obs.latitude, obs.longitude],
                popup=self._create_observation_popup(obs, i),
                tooltip=f"Observation {i}",
                icon=folium.Icon(color="blue", icon="eye", prefix="fa"),
            ).add_to(m)

            # Draw arrow showing flight direction
            from .geo_utils import destination_point

            arrow_length = 100  # meters
            arrow_end_lat, arrow_end_lon = destination_point(
                obs.latitude, obs.longitude, obs.bearing, arrow_length
            )

            folium.PolyLine(
                locations=[[obs.latitude, obs.longitude], [arrow_end_lat, arrow_end_lon]],
                color="blue",
                weight=3,
                opacity=0.7,
                popup=f"Bearing: {obs.bearing}°",
            ).add_to(m)

            # Draw line to estimated hive location if available
            if i <= len(hive_locations):
                hive = hive_locations[i - 1]
                folium.PolyLine(
                    locations=[[obs.latitude, obs.longitude], [hive.latitude, hive.longitude]],
                    color="red",
                    weight=2,
                    opacity=0.5,
                    dash_array="10, 5",
                    popup=f"Estimated flight path ({hive.distance_from_observer:.0f}m)",
                ).add_to(m)

        # Add hive location markers
        for i, hive in enumerate(hive_locations, 1):
            # Hive marker
            folium.Marker(
                location=[hive.latitude, hive.longitude],
                popup=self._create_hive_popup(hive, i),
                tooltip=f"Estimated Hive {i}",
                icon=folium.Icon(color="red", icon="home", prefix="fa"),
            ).add_to(m)

            # Confidence circle
            folium.Circle(
                location=[hive.latitude, hive.longitude],
                radius=hive.confidence_radius,
                color="red",
                fill=True,
                fillColor="red",
                fillOpacity=0.1,
                popup=f"Confidence: ±{hive.confidence_radius:.0f}m",
            ).add_to(m)

        # Add legend
        legend_html = self._create_legend(len(observations), len(hive_locations))
        m.get_root().html.add_child(folium.Element(legend_html))

        # Save map with error handling
        try:
            # Ensure directory exists
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            m.save(output_file)
        except PermissionError as e:
            raise MapGenerationError(f"Permission denied writing to {output_file}: {e}")
        except OSError as e:
            raise MapGenerationError(f"Failed to write map file {output_file}: {e}")

        return output_file

    def _create_observation_popup(self, obs: Observation, number: int) -> str:
        """Create HTML popup for observation marker."""
        # Build speed info only if speed is provided
        speed_info = ""
        if obs.speed is not None:
            speed_info = f"<b>Speed:</b> {obs.speed} m/s ({obs.speed * 3.6:.1f} km/h)<br>"

        return f"""
        <div style="font-family: Arial; width: 250px;">
            <h4>Observation {number}</h4>
            <b>Location:</b> {obs.latitude:.6f}, {obs.longitude:.6f}<br>
            <b>Time:</b> {obs.timestamp.strftime("%Y-%m-%d %H:%M:%S")}<br>
            <b>Bearing:</b> {obs.bearing}°<br>
            {speed_info}
            <b>Round trip:</b> {obs.round_trip_time:.0f}s ({obs.round_trip_time / 60:.1f}min)<br>
            <b>Estimated distance:</b> {obs.estimated_distance:.0f}m<br>
            {f"<b>Notes:</b> {obs.notes}" if obs.notes else ""}
        </div>
        """

    def _create_hive_popup(self, hive: HiveLocation, number: int) -> str:
        """Create HTML popup for hive location marker."""
        return f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="color: red;">Estimated Hive Location {number}</h4>
            <b>Coordinates:</b> {hive.latitude:.6f}, {hive.longitude:.6f}<br>
            <b>Distance:</b> {hive.distance_from_observer:.0f}m ({hive.distance_from_observer / 1000:.2f}km)<br>
            <b>Bearing:</b> {hive.bearing_from_observer:.1f}°<br>
            <b>Confidence:</b> ±{hive.confidence_radius:.0f}m<br>
            <b>Method:</b> {hive.calculation_method}<br>
            <br>
            <a href="https://www.google.com/maps?q={hive.latitude},{hive.longitude}" target="_blank">
                Open in Google Maps
            </a>
        </div>
        """

    def _create_legend(self, num_obs: int, num_hives: int) -> str:
        """Create HTML legend for the map."""
        return f"""
        <div style="
            position: fixed;
            top: 10px;
            right: 10px;
            width: 200px;
            background-color: white;
            border: 2px solid grey;
            border-radius: 5px;
            padding: 10px;
            font-family: Arial;
            font-size: 12px;
            z-index: 9999;
        ">
            <h4 style="margin-top: 0;">Hornet Nest Locator</h4>
            <p style="margin: 5px 0;">
                <i class="fa fa-eye" style="color: blue;"></i>
                Observation Point ({num_obs})
            </p>
            <p style="margin: 5px 0;">
                <i class="fa fa-home" style="color: red;"></i>
                Estimated Hive ({num_hives})
            </p>
            <p style="margin: 5px 0;">
                <span style="color: blue;">━━</span> Flight bearing
            </p>
            <p style="margin: 5px 0;">
                <span style="color: red;">- - -</span> Estimated path
            </p>
            <p style="margin: 5px 0;">
                <span style="color: red;">◯</span> Confidence area
            </p>
        </div>
        """
