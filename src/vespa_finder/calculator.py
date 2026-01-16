"""Calculate hive location from hornet observations."""

import math

from .geo_utils import bearing_between_points, destination_point, haversine_distance
from .models import HiveLocation, Observation


class HiveCalculator:
    """
    Calculate probable hive locations from hornet observations.

    Uses the professional empirical method from Vespawatchers:
    100 meters = 1 minute round trip time
    """

    # Professional empirical standard (Vespawatchers)
    DISTANCE_PER_MINUTE = 100.0  # meters per minute round trip

    # Uncertainty factors for confidence radius
    BEARING_UNCERTAINTY = 10.0  # ±10 degrees
    TIME_UNCERTAINTY = 5.0  # ±5 seconds

    # Minimum confidence radius (Vespawatchers note: "nest often slightly further than calculated")
    MIN_CONFIDENCE_RADIUS_METERS = 50.0

    def calculate_from_single_observation(
        self, observation: Observation, method: str = "empirical"
    ) -> HiveLocation:
        """
        Calculate hive location from a single observation.

        Args:
            observation: Single hornet observation with all required data
            method: "empirical" (recommended) or "theoretical"

        Returns:
            HiveLocation with estimated coordinates and confidence
        """
        # Calculate distance using selected method
        if method == "empirical":
            distance = observation.estimated_distance_empirical
            calc_method = "single_observation_empirical"
        elif method == "theoretical":
            if observation.speed is None:
                raise ValueError("Speed required for theoretical method")
            distance = observation.estimated_distance_theoretical
            calc_method = "single_observation_theoretical"
        else:
            raise ValueError(f"Unknown method: {method}. Use 'empirical' or 'theoretical'")

        # Project point along bearing
        hive_lat, hive_lon = destination_point(
            observation.latitude, observation.longitude, observation.bearing, distance
        )

        # Calculate confidence radius based on uncertainties
        confidence = self._calculate_confidence(observation, distance, method)

        return HiveLocation(
            latitude=hive_lat,
            longitude=hive_lon,
            confidence_radius=confidence,
            distance_from_observer=distance,
            bearing_from_observer=observation.bearing,
            calculation_method=calc_method,
        )

    def compare_methods(self, observation: Observation) -> dict:
        """
        Compare empirical and theoretical methods.

        Args:
            observation: Observation with speed data

        Returns:
            Dictionary with both results and comparison
        """
        if observation.speed is None:
            raise ValueError("Speed required for method comparison")

        empirical = self.calculate_from_single_observation(observation, method="empirical")
        theoretical = self.calculate_from_single_observation(observation, method="theoretical")

        difference = abs(empirical.distance_from_observer - theoretical.distance_from_observer)

        # Prevent division by zero (defensive check)
        if empirical.distance_from_observer > 0:
            difference_percent = (difference / empirical.distance_from_observer) * 100
        else:
            difference_percent = 0.0

        return {
            "empirical": empirical,
            "theoretical": theoretical,
            "difference_meters": difference,
            "difference_percent": difference_percent,
            "recommended": "empirical",
        }

    def calculate_from_multiple_observations(
        self, observations: list[Observation], method: str = "empirical"
    ) -> HiveLocation:
        """
        Calculate hive location from multiple observations using triangulation.

        Args:
            observations: List of 2+ observations from different locations
            method: "empirical" (recommended) or "theoretical"

        Returns:
            HiveLocation with triangulated coordinates and confidence
        """
        if len(observations) < 2:
            raise ValueError("Need at least 2 observations for triangulation")

        # Calculate individual hive estimates
        estimates = [
            self.calculate_from_single_observation(obs, method=method) for obs in observations
        ]

        # Simple average of all estimates (centroid method)
        avg_lat = sum(est.latitude for est in estimates) / len(estimates)
        avg_lon = sum(est.longitude for est in estimates) / len(estimates)

        # Calculate confidence as standard deviation of estimates
        distances_from_avg = [
            haversine_distance(avg_lat, avg_lon, est.latitude, est.longitude) for est in estimates
        ]

        avg_confidence = sum(est.confidence_radius for est in estimates) / len(estimates)
        spread = max(distances_from_avg) if distances_from_avg else 0

        # Confidence includes both individual uncertainties and spread between estimates
        total_confidence = avg_confidence + spread

        # Calculate distance and bearing from first observation point
        first_obs = observations[0]
        distance_from_first = haversine_distance(
            first_obs.latitude, first_obs.longitude, avg_lat, avg_lon
        )

        bearing_from_first = bearing_between_points(
            first_obs.latitude, first_obs.longitude, avg_lat, avg_lon
        )

        return HiveLocation(
            latitude=avg_lat,
            longitude=avg_lon,
            confidence_radius=total_confidence,
            distance_from_observer=distance_from_first,
            bearing_from_observer=bearing_from_first,
            calculation_method=f"triangulation_{len(observations)}_points_{method}",
        )

    def _calculate_confidence(
        self, observation: Observation, distance: float, method: str
    ) -> float:
        """
        Calculate confidence radius (uncertainty) for a single observation.

        Considers uncertainties in timing and bearing.

        Args:
            observation: The observation to calculate confidence for
            distance: Calculated distance to hive
            method: Calculation method used

        Returns:
            Confidence radius in meters
        """
        if method == "empirical":
            # Empirical method: error from timing uncertainty
            # ±5 seconds = ±(5/60) minutes = ±(5/60 * 100) meters
            time_error_meters = (self.TIME_UNCERTAINTY / 60.0) * self.DISTANCE_PER_MINUTE
        else:
            # Theoretical method: error from speed and timing
            if observation.speed is None:
                time_error_meters = 50.0  # Default
            else:
                time_error_meters = observation.speed * self.TIME_UNCERTAINTY / 2

        # Angular uncertainty from bearing error
        # At distance d, angular error of θ degrees creates lateral error of d*sin(θ)
        bearing_uncertainty_m = distance * math.sin(math.radians(self.BEARING_UNCERTAINTY))

        # Combined uncertainty (Pythagorean)
        total_uncertainty = math.sqrt(time_error_meters**2 + bearing_uncertainty_m**2)

        # Apply minimum confidence radius
        return max(self.MIN_CONFIDENCE_RADIUS_METERS, total_uncertainty)
