"""Tests for data models."""

from datetime import datetime

import pytest

from vespa_finder.models import HiveLocation, Observation


class TestObservation:
    """Tests for Observation model."""

    def test_valid_observation(self):
        """Test creating a valid observation."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=390,  # 6.5 minutes
        )
        assert obs.latitude == 48.8584
        assert obs.longitude == 2.2945
        assert obs.bearing == 45.0
        assert obs.round_trip_time == 390

    def test_timestamp_auto_set(self):
        """Timestamp should be set automatically if not provided."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=300,
        )
        assert obs.timestamp is not None
        assert isinstance(obs.timestamp, datetime)

    def test_custom_timestamp(self):
        """Custom timestamp should be preserved."""
        custom_time = datetime(2024, 1, 15, 10, 30, 0)
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=300,
            timestamp=custom_time,
        )
        assert obs.timestamp == custom_time

    def test_optional_fields(self):
        """Test optional fields."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=300,
            speed=7.0,
            notes="Clear weather",
            hornet_color_mark="white",
        )
        assert obs.speed == 7.0
        assert obs.notes == "Clear weather"
        assert obs.hornet_color_mark == "white"

    # Validation tests
    def test_invalid_latitude_too_high(self):
        """Latitude > 90 should raise ValueError."""
        with pytest.raises(ValueError, match="Latitude"):
            Observation(
                latitude=91.0,
                longitude=2.2945,
                bearing=45.0,
                round_trip_time=300,
            )

    def test_invalid_latitude_too_low(self):
        """Latitude < -90 should raise ValueError."""
        with pytest.raises(ValueError, match="Latitude"):
            Observation(
                latitude=-91.0,
                longitude=2.2945,
                bearing=45.0,
                round_trip_time=300,
            )

    def test_invalid_longitude_too_high(self):
        """Longitude > 180 should raise ValueError."""
        with pytest.raises(ValueError, match="Longitude"):
            Observation(
                latitude=48.8584,
                longitude=181.0,
                bearing=45.0,
                round_trip_time=300,
            )

    def test_invalid_longitude_too_low(self):
        """Longitude < -180 should raise ValueError."""
        with pytest.raises(ValueError, match="Longitude"):
            Observation(
                latitude=48.8584,
                longitude=-181.0,
                bearing=45.0,
                round_trip_time=300,
            )

    def test_invalid_bearing_too_high(self):
        """Bearing > 360 should raise ValueError."""
        with pytest.raises(ValueError, match="Bearing"):
            Observation(
                latitude=48.8584,
                longitude=2.2945,
                bearing=361.0,
                round_trip_time=300,
            )

    def test_invalid_bearing_negative(self):
        """Bearing < 0 should raise ValueError."""
        with pytest.raises(ValueError, match="Bearing"):
            Observation(
                latitude=48.8584,
                longitude=2.2945,
                bearing=-1.0,
                round_trip_time=300,
            )

    def test_invalid_round_trip_time_zero(self):
        """Round trip time = 0 should raise ValueError."""
        with pytest.raises(ValueError, match="Round trip time"):
            Observation(
                latitude=48.8584,
                longitude=2.2945,
                bearing=45.0,
                round_trip_time=0,
            )

    def test_invalid_round_trip_time_negative(self):
        """Negative round trip time should raise ValueError."""
        with pytest.raises(ValueError, match="Round trip time"):
            Observation(
                latitude=48.8584,
                longitude=2.2945,
                bearing=45.0,
                round_trip_time=-60,
            )

    def test_invalid_speed_zero(self):
        """Speed = 0 should raise ValueError."""
        with pytest.raises(ValueError, match="Speed"):
            Observation(
                latitude=48.8584,
                longitude=2.2945,
                bearing=45.0,
                round_trip_time=300,
                speed=0,
            )

    def test_invalid_speed_negative(self):
        """Negative speed should raise ValueError."""
        with pytest.raises(ValueError, match="Speed"):
            Observation(
                latitude=48.8584,
                longitude=2.2945,
                bearing=45.0,
                round_trip_time=300,
                speed=-5.0,
            )

    # Distance calculation tests
    def test_estimated_distance_empirical(self):
        """Test empirical distance calculation (100m/min)."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=390,  # 6.5 minutes
        )
        # 6.5 minutes * 100m/min = 650 meters
        assert obs.estimated_distance_empirical == 650.0

    def test_estimated_distance_empirical_one_minute(self):
        """1 minute round trip should give 100m."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=60,  # 1 minute
        )
        assert obs.estimated_distance_empirical == 100.0

    def test_estimated_distance_theoretical(self):
        """Test theoretical distance calculation."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=300,  # 5 minutes
            speed=7.0,  # m/s
        )
        # distance = (7 * 300) / 2 = 1050 meters
        assert obs.estimated_distance_theoretical == 1050.0

    def test_estimated_distance_theoretical_no_speed(self):
        """Theoretical distance without speed should return None."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=300,
        )
        assert obs.estimated_distance_theoretical is None

    def test_estimated_distance_alias(self):
        """estimated_distance should be alias for empirical."""
        obs = Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            round_trip_time=390,
        )
        assert obs.estimated_distance == obs.estimated_distance_empirical


class TestHiveLocation:
    """Tests for HiveLocation model."""

    def test_valid_hive_location(self):
        """Test creating a valid hive location."""
        hive = HiveLocation(
            latitude=48.8630,
            longitude=2.2990,
            confidence_radius=100.0,
            distance_from_observer=650.0,
            bearing_from_observer=45.0,
        )
        assert hive.latitude == 48.8630
        assert hive.longitude == 2.2990
        assert hive.confidence_radius == 100.0

    def test_timestamp_auto_set(self):
        """Timestamp should be set automatically."""
        hive = HiveLocation(
            latitude=48.8630,
            longitude=2.2990,
            confidence_radius=100.0,
            distance_from_observer=650.0,
            bearing_from_observer=45.0,
        )
        assert hive.timestamp is not None

    def test_default_calculation_method(self):
        """Default calculation method should be set."""
        hive = HiveLocation(
            latitude=48.8630,
            longitude=2.2990,
            confidence_radius=100.0,
            distance_from_observer=650.0,
            bearing_from_observer=45.0,
        )
        assert hive.calculation_method == "single_observation_empirical"

    def test_custom_calculation_method(self):
        """Custom calculation method should be preserved."""
        hive = HiveLocation(
            latitude=48.8630,
            longitude=2.2990,
            confidence_radius=100.0,
            distance_from_observer=650.0,
            bearing_from_observer=45.0,
            calculation_method="triangulation_3_points_empirical",
        )
        assert hive.calculation_method == "triangulation_3_points_empirical"

    def test_str_representation(self):
        """Test string representation."""
        hive = HiveLocation(
            latitude=48.8630,
            longitude=2.2990,
            confidence_radius=100.0,
            distance_from_observer=650.0,
            bearing_from_observer=45.0,
        )
        result = str(hive)
        assert "Hive Location" in result
        assert "48.863000" in result
        assert "650m" in result
        assert "45.0°" in result
