#!/usr/bin/env python3
"""Example usage of the Hornet Nest Locator."""
# ruff: noqa: T201

from vespa_finder import HiveCalculator, Observation
from vespa_finder.geo_utils import format_bearing, format_coordinates
from vespa_finder.visualizer import MapVisualizer


def example_single_observation():
    """Example: Single observation near Paris."""
    print("=" * 60)
    print("EXAMPLE 1: Single Observation")
    print("=" * 60)

    # Create observation (near Eiffel Tower, Paris)
    observation = Observation(
        latitude=48.8584,  # Eiffel Tower
        longitude=2.2945,
        bearing=45.0,  # Northeast direction
        speed=7.0,  # 7 m/s (25 km/h)
        round_trip_time=300,  # 5 minutes total
        notes="Clear weather, confident observation",
    )

    print(f"\nObservation Point: {format_coordinates(observation.latitude, observation.longitude)}")
    print(f"Flight Direction: {format_bearing(observation.bearing)}")
    print(f"Speed: {observation.speed} m/s ({observation.speed * 3.6:.1f} km/h)")
    print(
        f"Round Trip: {observation.round_trip_time}s ({observation.round_trip_time / 60:.1f} min)"
    )
    print(f"Calculated Distance: {observation.estimated_distance:.0f}m")

    # Calculate hive location
    calculator = HiveCalculator()
    hive = calculator.calculate_from_single_observation(observation)

    print("\n--- CALCULATED HIVE LOCATION ---")
    print(f"Coordinates: {format_coordinates(hive.latitude, hive.longitude)}")
    print(
        f"Distance: {hive.distance_from_observer:.0f}m ({hive.distance_from_observer / 1000:.2f}km)"
    )
    print(f"Bearing: {format_bearing(hive.bearing_from_observer)}")
    print(f"Confidence: ±{hive.confidence_radius:.0f}m")
    print(f"Google Maps: https://www.google.com/maps?q={hive.latitude},{hive.longitude}")

    # Create map
    visualizer = MapVisualizer()
    map_file = visualizer.create_map(
        observations=[observation],
        hive_locations=[hive],
        output_file="example_single_observation.html",
    )
    print(f"\n✓ Map saved to: {map_file}")

    return observation, hive


def example_multiple_observations():
    """Example: Triangulation from multiple observation points."""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 2: Triangulation from Multiple Observations")
    print("=" * 60)

    # Three observations from different locations
    observations = [
        Observation(
            latitude=48.8584,
            longitude=2.2945,
            bearing=45.0,
            speed=7.0,
            round_trip_time=300,
            notes="Observation Point 1 - Eiffel Tower",
        ),
        Observation(
            latitude=48.8606,
            longitude=2.2900,  # ~400m NW of point 1
            bearing=90.0,
            speed=7.0,
            round_trip_time=280,
            notes="Observation Point 2 - Trocadéro",
        ),
        Observation(
            latitude=48.8560,
            longitude=2.2970,  # ~300m SE of point 1
            bearing=30.0,
            speed=7.0,
            round_trip_time=310,
            notes="Observation Point 3 - Champ de Mars",
        ),
    ]

    print(f"\nNumber of observations: {len(observations)}")
    for i, obs in enumerate(observations, 1):
        print(f"\n  Observation {i}:")
        print(f"    Location: {format_coordinates(obs.latitude, obs.longitude)}")
        print(f"    Bearing: {format_bearing(obs.bearing)}")
        print(f"    Estimated distance: {obs.estimated_distance:.0f}m")

    # Calculate using triangulation
    calculator = HiveCalculator()
    hive = calculator.calculate_from_multiple_observations(observations)

    print("\n--- TRIANGULATED HIVE LOCATION ---")
    print(f"Coordinates: {format_coordinates(hive.latitude, hive.longitude)}")
    print(f"Confidence: ±{hive.confidence_radius:.0f}m")
    print(f"Method: {hive.calculation_method}")
    print(f"Google Maps: https://www.google.com/maps?q={hive.latitude},{hive.longitude}")

    # Create map with all observations
    visualizer = MapVisualizer()
    map_file = visualizer.create_map(
        observations=observations, hive_locations=[hive], output_file="example_triangulation.html"
    )
    print(f"\n✓ Map saved to: {map_file}")

    return observations, hive


def example_different_speeds():
    """Example: Comparing different assumed speeds."""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 3: Effect of Speed Variation")
    print("=" * 60)

    # Same observation with different speed assumptions
    base_obs = {
        "latitude": 48.8584,
        "longitude": 2.2945,
        "bearing": 45.0,
        "round_trip_time": 300,
    }

    speeds = [6.0, 7.0, 8.0]  # m/s

    calculator = HiveCalculator()

    print("\nSame observation with different speed assumptions:\n")
    print(f"  Observation: {format_coordinates(base_obs['latitude'], base_obs['longitude'])}")
    print(f"  Bearing: {format_bearing(base_obs['bearing'])}")
    print(f"  Round trip: {base_obs['round_trip_time']}s")
    print("\n  Speed | Distance | Hive Location")
    print("  ------|----------|---------------")

    for speed in speeds:
        obs = Observation(**base_obs, speed=speed)
        hive = calculator.calculate_from_single_observation(obs)

        print(
            f"  {speed:.1f} m/s | {obs.estimated_distance:4.0f}m   | "
            f"{hive.latitude:.6f}°N, {hive.longitude:.6f}°E"
        )

    print("\n  → Speed variation significantly affects distance calculation")
    print("  → Use marked hornets and measure actual speed if possible")


if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║     HORNET HIVE LOCATOR - EXAMPLES                     ║")
    print("╚════════════════════════════════════════════════════════╝\n")

    # Run examples
    example_single_observation()
    example_multiple_observations()
    example_different_speeds()

    print("\n" + "=" * 60)
    print("Examples complete! Check the HTML files to view maps.")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - example_single_observation.html")
    print("  - example_triangulation.html")
    print("\nOpen these files in your web browser to see interactive maps.")
    print("\n🐝 Happy hornet hunting!")
