"""Data models for hornet observations and hive locations."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Observation:
    """A single hornet observation with tracking data."""

    latitude: float  # -90 to 90
    longitude: float  # -180 to 180
    bearing: float  # 0-360 degrees (0=North, clockwise)
    round_trip_time: float  # seconds
    speed: float | None = None  # meters per second (optional, for theoretical comparison)
    timestamp: datetime = None
    notes: str = ""
    hornet_color_mark: str | None = None  # Track individual hornets

    def __post_init__(self):
        """Validate input data."""
        if self.timestamp is None:
            self.timestamp = datetime.now()

        # Validate ranges BEFORE normalization
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Latitude must be between -90 and 90, got {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Longitude must be between -180 and 180, got {self.longitude}")
        if not 0 <= self.bearing <= 360:
            raise ValueError(f"Bearing must be between 0 and 360 (inclusive), got {self.bearing}")
        if self.round_trip_time <= 0:
            raise ValueError(f"Round trip time must be positive, got {self.round_trip_time}")
        if self.speed is not None and self.speed <= 0:
            raise ValueError(f"Speed must be positive, got {self.speed}")

        # Normalize bearing: 360° equals 0° in compass notation (using tolerance for float comparison)
        if abs(self.bearing - 360.0) < 1e-9:
            self.bearing = 0.0

    @property
    def estimated_distance_empirical(self) -> float:
        """
        Calculate estimated one-way distance using EMPIRICAL METHOD (Professional Standard).

        Based on Vespawatchers field observations:
        100 meters = 1 minute round trip

        This is the RECOMMENDED method used by professional hornet trackers.

        Returns:
            Distance in meters
        """
        round_trip_minutes = self.round_trip_time / 60.0
        return round_trip_minutes * 100.0

    @property
    def estimated_distance_theoretical(self) -> float | None:
        """
        Calculate estimated one-way distance using THEORETICAL METHOD.

        Formula: distance = (speed x time) / 2

        This method is less reliable than the empirical method.
        Only available if speed was provided.

        Returns:
            Distance in meters, or None if speed not provided
        """
        if self.speed is None:
            return None
        return (self.speed * self.round_trip_time) / 2.0

    @property
    def estimated_distance(self) -> float:
        """
        Get estimated distance using the professional empirical method.

        This is an alias for estimated_distance_empirical for backward compatibility.

        Returns:
            Distance in meters
        """
        return self.estimated_distance_empirical


@dataclass
class HiveLocation:
    """Calculated hive location from observations."""

    latitude: float
    longitude: float
    confidence_radius: float  # meters
    distance_from_observer: float  # meters
    bearing_from_observer: float  # degrees
    calculation_method: str = "single_observation_empirical"
    timestamp: datetime = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Hive Location:\n"
            f"  Coordinates: {self.latitude:.6f}°N, {self.longitude:.6f}°E\n"
            f"  Distance: {self.distance_from_observer:.0f}m ({self.distance_from_observer / 1000:.2f}km)\n"
            f"  Bearing: {self.bearing_from_observer:.1f}°\n"
            f"  Confidence: ±{self.confidence_radius:.0f}m\n"
            f"  Method: {self.calculation_method}"
        )
