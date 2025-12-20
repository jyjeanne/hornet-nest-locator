"""Tests for geographic utility functions."""

from vespa_finder.geo_utils import (
    bearing_between_points,
    destination_point,
    format_bearing,
    format_coordinates,
    haversine_distance,
)


class TestDestinationPoint:
    """Tests for destination_point function."""

    def test_destination_north(self):
        """Moving north should increase latitude."""
        lat, lon = destination_point(48.8584, 2.2945, 0, 1000)  # 1km north
        assert lat > 48.8584
        assert abs(lon - 2.2945) < 0.0001  # Longitude should stay ~same

    def test_destination_south(self):
        """Moving south should decrease latitude."""
        lat, lon = destination_point(48.8584, 2.2945, 180, 1000)  # 1km south
        assert lat < 48.8584
        assert abs(lon - 2.2945) < 0.0001

    def test_destination_east(self):
        """Moving east should increase longitude."""
        lat, lon = destination_point(48.8584, 2.2945, 90, 1000)  # 1km east
        assert lon > 2.2945
        assert abs(lat - 48.8584) < 0.001

    def test_destination_west(self):
        """Moving west should decrease longitude."""
        lat, lon = destination_point(48.8584, 2.2945, 270, 1000)  # 1km west
        assert lon < 2.2945
        assert abs(lat - 48.8584) < 0.001

    def test_destination_zero_distance(self):
        """Zero distance should return same point."""
        lat, lon = destination_point(48.8584, 2.2945, 45, 0)
        assert abs(lat - 48.8584) < 1e-10
        assert abs(lon - 2.2945) < 1e-10

    def test_destination_known_distance(self):
        """Test with known distance - 1km north from equator."""
        lat, lon = destination_point(0, 0, 0, 1000)
        # 1km = ~0.009 degrees at equator
        assert abs(lat - 0.00899) < 0.001
        assert abs(lon) < 0.0001


class TestHaversineDistance:
    """Tests for haversine_distance function."""

    def test_same_point(self):
        """Distance from point to itself should be 0."""
        distance = haversine_distance(48.8584, 2.2945, 48.8584, 2.2945)
        assert distance == 0

    def test_known_distance_paris_london(self):
        """Test Paris to London distance (~344km)."""
        # Paris (Eiffel Tower) to London (Big Ben)
        distance = haversine_distance(48.8584, 2.2945, 51.5007, -0.1246)
        # Should be approximately 344 km
        assert 340000 < distance < 350000

    def test_symmetry(self):
        """Distance A->B should equal B->A."""
        d1 = haversine_distance(48.8584, 2.2945, 51.5007, -0.1246)
        d2 = haversine_distance(51.5007, -0.1246, 48.8584, 2.2945)
        assert abs(d1 - d2) < 0.01

    def test_short_distance(self):
        """Test short distance calculation (100m)."""
        # Move ~100m north from a point
        lat1, lon1 = 48.8584, 2.2945
        lat2, lon2 = destination_point(lat1, lon1, 0, 100)
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        assert abs(distance - 100) < 1  # Within 1 meter accuracy

    def test_roundtrip_accuracy(self):
        """Destination then distance should return original distance."""
        original_distance = 650  # meters (typical hornet tracking distance)
        lat1, lon1 = 48.8584, 2.2945
        lat2, lon2 = destination_point(lat1, lon1, 45, original_distance)
        calculated_distance = haversine_distance(lat1, lon1, lat2, lon2)
        assert abs(calculated_distance - original_distance) < 1


class TestBearingBetweenPoints:
    """Tests for bearing_between_points function."""

    def test_bearing_north(self):
        """Point directly north should have bearing ~0."""
        bearing = bearing_between_points(48.8584, 2.2945, 48.8684, 2.2945)
        assert abs(bearing) < 1 or abs(bearing - 360) < 1

    def test_bearing_east(self):
        """Point directly east should have bearing ~90."""
        bearing = bearing_between_points(48.8584, 2.2945, 48.8584, 2.3045)
        assert abs(bearing - 90) < 1

    def test_bearing_south(self):
        """Point directly south should have bearing ~180."""
        bearing = bearing_between_points(48.8584, 2.2945, 48.8484, 2.2945)
        assert abs(bearing - 180) < 1

    def test_bearing_west(self):
        """Point directly west should have bearing ~270."""
        bearing = bearing_between_points(48.8584, 2.2945, 48.8584, 2.2845)
        assert abs(bearing - 270) < 1

    def test_bearing_range(self):
        """Bearing should always be 0-360."""
        # Test various directions
        for bearing_input in [0, 45, 90, 135, 180, 225, 270, 315]:
            lat2, lon2 = destination_point(48.8584, 2.2945, bearing_input, 1000)
            calculated = bearing_between_points(48.8584, 2.2945, lat2, lon2)
            assert 0 <= calculated <= 360


class TestFormatCoordinates:
    """Tests for format_coordinates function."""

    def test_positive_coordinates(self):
        """Test formatting positive (N, E) coordinates."""
        result = format_coordinates(48.8584, 2.2945)
        assert "N" in result
        assert "E" in result
        assert "48.858400" in result

    def test_negative_latitude(self):
        """Test formatting negative latitude (S)."""
        result = format_coordinates(-33.8688, 151.2093)  # Sydney
        assert "S" in result
        assert "E" in result

    def test_negative_longitude(self):
        """Test formatting negative longitude (W)."""
        result = format_coordinates(40.7128, -74.0060)  # New York
        assert "N" in result
        assert "W" in result

    def test_both_negative(self):
        """Test formatting both negative (S, W)."""
        result = format_coordinates(-22.9068, -43.1729)  # Rio
        assert "S" in result
        assert "W" in result


class TestFormatBearing:
    """Tests for format_bearing function."""

    def test_cardinal_directions(self):
        """Test cardinal direction formatting."""
        assert "N" in format_bearing(0)
        assert "E" in format_bearing(90)
        assert "S" in format_bearing(180)
        assert "W" in format_bearing(270)

    def test_intercardinal_directions(self):
        """Test intercardinal direction formatting."""
        assert "NE" in format_bearing(45)
        assert "SE" in format_bearing(135)
        assert "SW" in format_bearing(225)
        assert "NW" in format_bearing(315)

    def test_includes_degrees(self):
        """Format should include degree value."""
        result = format_bearing(45)
        assert "45" in result
        assert "°" in result

    def test_boundary_360(self):
        """360 degrees should format as N."""
        result = format_bearing(360)
        assert "N" in result
