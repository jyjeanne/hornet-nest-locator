"""Tests for HiveCalculator."""

import math

import pytest

from vespa_finder.calculator import HiveCalculator
from vespa_finder.geo_utils import haversine_distance
from vespa_finder.models import HiveLocation, Observation


class TestHiveCalculatorSingleObservation:
    """Tests for single observation calculations."""

    def setup_method(self):
        """Set up calculator for each test."""
        self.calculator = HiveCalculator()

    def test_empirical_method_distance(self):
        """Test empirical method calculates correct distance."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=390,  # 6.5 minutes = 650m
        )
        hive = self.calculator.calculate_from_single_observation(obs, method="empirical")

        # Check distance
        assert abs(hive.distance_from_observer - 650.0) < 1

    def test_empirical_method_direction(self):
        """Test hive is placed in correct direction."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=0.0,  # North
            round_trip_time=60,  # 1 minute = 100m
        )
        hive = self.calculator.calculate_from_single_observation(obs, method="empirical")

        # Hive should be north of observation point
        assert hive.latitude > obs.latitude
        # Longitude should stay approximately the same
        assert abs(hive.longitude - obs.longitude) < 0.001

    def test_empirical_method_northeast(self):
        """Test northeast direction (45 degrees)."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=60,
        )
        hive = self.calculator.calculate_from_single_observation(obs, method="empirical")

        # Hive should be NE (higher lat and lon)
        assert hive.latitude > obs.latitude
        assert hive.longitude > obs.longitude

    def test_theoretical_method(self):
        """Test theoretical method with speed."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=300,  # 5 minutes
            speed=7.0,  # 7 m/s
        )
        hive = self.calculator.calculate_from_single_observation(obs, method="theoretical")

        # distance = (7 * 300) / 2 = 1050m
        assert abs(hive.distance_from_observer - 1050.0) < 1
        assert hive.calculation_method == "single_observation_theoretical"

    def test_theoretical_method_requires_speed(self):
        """Theoretical method without speed should raise error."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=300,
        )
        with pytest.raises(ValueError, match="Speed required"):
            self.calculator.calculate_from_single_observation(obs, method="theoretical")

    def test_unknown_method_raises_error(self):
        """Unknown method should raise error."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=300,
        )
        with pytest.raises(ValueError, match="Unknown method"):
            self.calculator.calculate_from_single_observation(obs, method="unknown")

    def test_confidence_radius_minimum(self):
        """Confidence radius should have a minimum of 50m."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=30,  # Very short time
        )
        hive = self.calculator.calculate_from_single_observation(obs, method="empirical")

        assert hive.confidence_radius >= 50.0

    def test_bearing_preserved(self):
        """Bearing from observer should match observation bearing."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=135.0,  # Southeast
            round_trip_time=300,
        )
        hive = self.calculator.calculate_from_single_observation(obs, method="empirical")

        assert hive.bearing_from_observer == 135.0

    def test_actual_distance_matches_calculated(self):
        """Haversine distance to hive should match reported distance."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=390,  # 650m
        )
        hive = self.calculator.calculate_from_single_observation(obs, method="empirical")

        actual_distance = haversine_distance(
            obs.latitude, obs.longitude, hive.latitude, hive.longitude
        )

        assert abs(actual_distance - hive.distance_from_observer) < 1


class TestHiveCalculatorMethodComparison:
    """Tests for method comparison functionality."""

    def setup_method(self):
        """Set up calculator for each test."""
        self.calculator = HiveCalculator()

    def test_compare_methods(self):
        """Test comparing empirical and theoretical methods."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=390,  # 6.5 min
            speed=7.0,
        )
        comparison = self.calculator.compare_methods(obs)

        assert "empirical" in comparison
        assert "theoretical" in comparison
        assert "difference_meters" in comparison
        assert "difference_percent" in comparison
        assert comparison["recommended"] == "empirical"

    def test_compare_methods_requires_speed(self):
        """Comparison requires speed for theoretical method."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=300,
        )
        with pytest.raises(ValueError, match="Speed required"):
            self.calculator.compare_methods(obs)

    def test_compare_methods_difference_calculation(self):
        """Test difference calculation is correct."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=300,  # 5 min = 500m empirical
            speed=7.0,  # (7*300)/2 = 1050m theoretical
        )
        comparison = self.calculator.compare_methods(obs)

        # Difference should be |1050 - 500| = 550m
        assert abs(comparison["difference_meters"] - 550.0) < 1
        # Percent difference should be 550/500 * 100 = 110%
        assert abs(comparison["difference_percent"] - 110.0) < 1


class TestHiveCalculatorTriangulation:
    """Tests for multiple observation triangulation."""

    def setup_method(self):
        """Set up calculator for each test."""
        self.calculator = HiveCalculator()

    def test_triangulation_requires_two_observations(self):
        """Triangulation requires at least 2 observations."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=300,
        )
        with pytest.raises(ValueError, match="at least 2"):
            self.calculator.calculate_from_multiple_observations([obs])

    def test_triangulation_two_observations(self):
        """Test triangulation with two observations."""
        observations = [
            Observation(
                latitude=48.8584,
                longitude=2.2945,
                bearing=45.0,
                round_trip_time=300,
            ),
            Observation(
                latitude=48.8600,
                longitude=2.2900,
                bearing=90.0,
                round_trip_time=280,
            ),
        ]
        hive = self.calculator.calculate_from_multiple_observations(observations)

        assert hive.calculation_method == "triangulation_2_points_empirical"
        assert hive.latitude is not None
        assert hive.longitude is not None

    def test_triangulation_three_observations(self):
        """Test triangulation with three observations."""
        observations = [
            Observation(
                latitude=48.8584,
                longitude=2.2945,
                bearing=45.0,
                round_trip_time=300,
            ),
            Observation(
                latitude=48.8600,
                longitude=2.2900,
                bearing=90.0,
                round_trip_time=280,
            ),
            Observation(
                latitude=48.8560,
                longitude=2.2970,
                bearing=30.0,
                round_trip_time=310,
            ),
        ]
        hive = self.calculator.calculate_from_multiple_observations(observations)

        assert hive.calculation_method == "triangulation_3_points_empirical"

    def test_triangulation_confidence_includes_spread(self):
        """Confidence should account for spread between estimates."""
        # Two observations pointing to different areas
        observations = [
            Observation(
                latitude=48.8584,
                longitude=2.2945,
                bearing=0.0,  # North
                round_trip_time=300,
            ),
            Observation(
                latitude=48.8584,
                longitude=2.2945,
                bearing=90.0,  # East (very different direction)
                round_trip_time=300,
            ),
        ]
        hive = self.calculator.calculate_from_multiple_observations(observations)

        # Confidence should be larger due to disagreement
        assert hive.confidence_radius > 100  # Base confidence + spread

    def test_triangulation_theoretical_method(self):
        """Test triangulation with theoretical method."""
        observations = [
            Observation(
                latitude=48.8584,
                longitude=2.2945,
                bearing=45.0,
                round_trip_time=300,
                speed=7.0,
            ),
            Observation(
                latitude=48.8600,
                longitude=2.2900,
                bearing=90.0,
                round_trip_time=280,
                speed=7.0,
            ),
        ]
        hive = self.calculator.calculate_from_multiple_observations(
            observations, method="theoretical"
        )

        assert "theoretical" in hive.calculation_method


class TestHiveCalculatorConstants:
    """Tests for calculator constants."""

    def test_distance_per_minute_constant(self):
        """Verify the Vespawatchers standard constant."""
        assert HiveCalculator.DISTANCE_PER_MINUTE == 100.0

    def test_bearing_uncertainty(self):
        """Verify bearing uncertainty is reasonable."""
        assert HiveCalculator.BEARING_UNCERTAINTY == 10.0

    def test_time_uncertainty(self):
        """Verify time uncertainty is reasonable."""
        assert HiveCalculator.TIME_UNCERTAINTY == 5.0
