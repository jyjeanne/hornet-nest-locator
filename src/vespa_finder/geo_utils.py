"""Geographic calculation utilities using haversine formula."""

import math

# Earth's radius in meters (WGS84 mean radius)
EARTH_RADIUS_METERS = 6371000.0


def destination_point(
    lat: float, lon: float, bearing: float, distance: float
) -> tuple[float, float]:
    """
    Calculate destination point given start point, bearing, and distance.

    Uses the haversine formula to account for Earth's curvature.

    Args:
        lat: Starting latitude in degrees
        lon: Starting longitude in degrees
        bearing: Bearing in degrees (0=North, clockwise)
        distance: Distance in meters

    Returns:
        Tuple of (destination_latitude, destination_longitude) in degrees
    """
    # Convert to radians
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)
    bearing_rad = math.radians(bearing)

    # Angular distance in radians
    angular_distance = distance / EARTH_RADIUS_METERS

    # Calculate destination point
    lat2 = math.asin(
        math.sin(lat1) * math.cos(angular_distance)
        + math.cos(lat1) * math.sin(angular_distance) * math.cos(bearing_rad)
    )

    lon2 = lon1 + math.atan2(
        math.sin(bearing_rad) * math.sin(angular_distance) * math.cos(lat1),
        math.cos(angular_distance) - math.sin(lat1) * math.sin(lat2),
    )

    # Convert back to degrees
    lat2_deg = math.degrees(lat2)
    lon2_deg = math.degrees(lon2)

    # Normalize longitude to -180 to 180
    lon2_deg = ((lon2_deg + 180) % 360) - 180

    return lat2_deg, lon2_deg


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.

    Args:
        lat1, lon1: First point coordinates in degrees
        lat2, lon2: Second point coordinates in degrees

    Returns:
        Distance in meters
    """
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    # Haversine formula
    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = EARTH_RADIUS_METERS * c

    return distance


def bearing_between_points(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate bearing from point 1 to point 2.

    Args:
        lat1, lon1: First point coordinates in degrees
        lat2, lon2: Second point coordinates in degrees

    Returns:
        Bearing in degrees (0=North, clockwise)
    """
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lon = math.radians(lon2 - lon1)

    # Calculate bearing
    y = math.sin(delta_lon) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(
        lat2_rad
    ) * math.cos(delta_lon)

    bearing_rad = math.atan2(y, x)

    # Convert to degrees and normalize to 0-360
    bearing_deg = (math.degrees(bearing_rad) + 360) % 360

    return bearing_deg


def format_coordinates(lat: float, lon: float) -> str:
    """
    Format coordinates as human-readable string.

    Args:
        lat: Latitude in degrees
        lon: Longitude in degrees

    Returns:
        Formatted string like "48.8566°N, 2.3522°E"
    """
    lat_dir = "N" if lat >= 0 else "S"
    lon_dir = "E" if lon >= 0 else "W"

    return f"{abs(lat):.6f}°{lat_dir}, {abs(lon):.6f}°{lon_dir}"


def format_bearing(bearing: float) -> str:
    """
    Format bearing as human-readable compass direction.

    Args:
        bearing: Bearing in degrees (0-360)

    Returns:
        String like "NE (45°)" or "N (0°)"
    """
    directions = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]

    index = int((bearing + 11.25) / 22.5) % 16
    direction = directions[index]

    return f"{direction} ({bearing:.1f}°)"
