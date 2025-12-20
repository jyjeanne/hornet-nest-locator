#!/usr/bin/env python3
"""VespaFinder - CLI interface with professional methodology."""

import sys
from datetime import datetime

from vespa_finder import HiveCalculator, Observation
from vespa_finder.geo_utils import format_bearing, format_coordinates


def get_float_input(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """Get validated float input from user."""
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  Error: Value must be >= {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"  Error: Value must be <= {max_val}")
                continue
            return value
        except ValueError:
            print("  Error: Please enter a valid number")


def get_observation() -> Observation:
    """Collect observation data from user."""
    print("\n" + "=" * 70)
    print("HORNET OBSERVATION DATA ENTRY")
    print("Based on Vespawatchers Professional Methodology")
    print("=" * 70)

    print("\n1. OBSERVATION POINT LOCATION")
    print("-" * 50)
    latitude = get_float_input("  Latitude (degrees, -90 to 90): ", -90, 90)
    longitude = get_float_input("  Longitude (degrees, -180 to 180): ", -180, 180)

    print("\n2. FLIGHT DIRECTION")
    print("-" * 50)
    print("  Enter compass bearing:")
    print("    0° = North, 90° = East, 180° = South, 270° = West")
    bearing = get_float_input("  Bearing (degrees, 0-360): ", 0, 360)

    print("\n3. ROUND TRIP TIME")
    print("-" * 50)
    print("  ⚠️  IMPORTANT: Measure multiple times until consistent!")
    print("  Time from hornet departure until return")
    minutes = get_float_input("  Minutes: ", 0)
    seconds = get_float_input("  Seconds: ", 0)
    round_trip_time = minutes * 60 + seconds

    if round_trip_time < 10:
        print("  ⚠️  Warning: Very short time, results may be inaccurate")

    print("\n4. HORNET IDENTIFICATION (Optional)")
    print("-" * 50)
    color = input("  Color mark (if marked): ").strip()

    print("\n5. OPTIONAL: Speed for Comparison")
    print("-" * 50)
    print("  Professional method uses empirical formula (100m/min)")
    print("  You can optionally enter speed to compare methods")
    speed_input = input("  Speed in m/s [press Enter to skip]: ").strip()
    speed = float(speed_input) if speed_input else None

    print("\n6. NOTES (Optional)")
    print("-" * 50)
    notes = input("  Notes (weather, confidence, flight pattern, etc.): ").strip()

    # Create observation
    try:
        observation = Observation(
            latitude=latitude,
            longitude=longitude,
            bearing=bearing,
            round_trip_time=round_trip_time,
            speed=speed,
            hornet_color_mark=color if color else None,
            notes=notes,
        )
        return observation
    except ValueError as e:
        print(f"\n❌ Error creating observation: {e}")
        sys.exit(1)


def display_results(observation: Observation, calculator: HiveCalculator):
    """Display calculation results with professional methodology."""
    print("\n" + "=" * 70)
    print("CALCULATION RESULTS")
    print("=" * 70)

    print("\nOBSERVATION POINT:")
    print(f"  Location: {format_coordinates(observation.latitude, observation.longitude)}")
    print(f"  Time: {observation.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    if observation.hornet_color_mark:
        print(f"  Hornet mark: {observation.hornet_color_mark}")

    print("\nFLIGHT DATA:")
    print(f"  Direction: {format_bearing(observation.bearing)}")
    print(
        f"  Round trip time: {observation.round_trip_time:.0f} seconds ({observation.round_trip_time / 60:.2f} minutes)"
    )

    # Calculate using empirical method (professional standard)
    hive_empirical = calculator.calculate_from_single_observation(observation, method="empirical")

    print("\n" + "=" * 70)
    print("📍 EMPIRICAL METHOD (RECOMMENDED - Vespawatchers Standard)")
    print("=" * 70)
    print(f"  Formula: 100 meters = 1 minute round trip")
    print(
        f"  Calculated distance: {hive_empirical.distance_from_observer:.0f} meters ({hive_empirical.distance_from_observer / 1000:.2f} km)"
    )
    print(f"\n  📌 ESTIMATED HIVE LOCATION:")
    print(f"  Coordinates: {format_coordinates(hive_empirical.latitude, hive_empirical.longitude)}")
    print(f"  Bearing from you: {format_bearing(hive_empirical.bearing_from_observer)}")
    print(f"  Confidence: ±{hive_empirical.confidence_radius:.0f} meters")
    print(f"\n  ⚠️  Note: In practice, nest is often slightly further than calculated")
    print(f"\n  🗺️  GPS COORDINATES:")
    print(f"  {hive_empirical.latitude:.6f}, {hive_empirical.longitude:.6f}")
    print(
        f"  Google Maps: https://www.google.com/maps?q={hive_empirical.latitude},{hive_empirical.longitude}"
    )

    # If speed provided, show comparison
    if observation.speed is not None:
        comparison = calculator.compare_methods(observation)
        hive_theoretical = comparison["theoretical"]

        print("\n" + "=" * 70)
        print("📊 THEORETICAL METHOD (For Comparison Only)")
        print("=" * 70)
        print(f"  Formula: distance = (speed × time) / 2")
        print(f"  Speed used: {observation.speed} m/s ({observation.speed * 3.6:.1f} km/h)")
        print(
            f"  Calculated distance: {hive_theoretical.distance_from_observer:.0f} meters ({hive_theoretical.distance_from_observer / 1000:.2f} km)"
        )
        print(
            f"  Coordinates: {format_coordinates(hive_theoretical.latitude, hive_theoretical.longitude)}"
        )

        print(f"\n  📊 COMPARISON:")
        print(
            f"  Difference: {comparison['difference_meters']:.0f} meters ({comparison['difference_percent']:.1f}%)"
        )
        print(f"  Recommended method: {comparison['recommended'].upper()}")

    if observation.notes:
        print(f"\n📝 NOTES: {observation.notes}")

    print("\n" + "=" * 70)
    print("⚠️  SAFETY WARNING (Vespawatchers Recommendations):")
    print("=" * 70)
    print("  Essential Equipment:")
    print("  ✓ Binoculars (8×42) - MOST IMPORTANT TOOL")
    print("  ✓ Wick pot with sugar bait")
    print("  ✓ Marking materials (white marker recommended)")
    print("  ✓ Butterfly net (to catch interfering European hornets)")
    print()
    print("  Search Strategy:")
    print("  ✓ Don't just look in trees! Check ground, sheds, roofs, hedges")
    print("  ✓ Scan treetops with binoculars for flying hornets")
    print("  ✓ Walk in circles around suspected area")
    print("  ✓ Take small steps (100-200m) if relocating hornet")
    print()
    print("  Safety:")
    print("  ✓ Do NOT approach nest alone or without protection")
    print("  ✓ Contact professional pest control")
    print("  ✓ Report to: vespawatch.be / waarneming.nl / observatoire.biodiversite.wallonie.be")
    print("=" * 70)

    return hive_empirical


def save_to_file(observation: Observation, hive_location):
    """Save results to a text file."""
    filename = f"hornet_observation_{observation.timestamp.strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w") as f:
        f.write("VESPAFINDER - OBSERVATION REPORT\n")
        f.write("Based on Vespawatchers Professional Methodology\n")
        f.write("=" * 70 + "\n\n")

        f.write("OBSERVATION DATA:\n")
        f.write(f"  Date/Time: {observation.timestamp}\n")
        f.write(f"  Observer Location: {observation.latitude}, {observation.longitude}\n")
        f.write(f"  Bearing: {observation.bearing}°\n")
        f.write(
            f"  Round Trip Time: {observation.round_trip_time} seconds ({observation.round_trip_time / 60:.2f} min)\n"
        )
        if observation.hornet_color_mark:
            f.write(f"  Hornet Mark: {observation.hornet_color_mark}\n")
        if observation.speed:
            f.write(f"  Speed (for comparison): {observation.speed} m/s\n")
        f.write(f"  Notes: {observation.notes}\n\n")

        f.write("CALCULATED HIVE LOCATION (Empirical Method):\n")
        f.write(f"  Method: 100m = 1 minute round trip (Vespawatchers standard)\n")
        f.write(f"  Latitude: {hive_location.latitude}\n")
        f.write(f"  Longitude: {hive_location.longitude}\n")
        f.write(f"  Distance: {hive_location.distance_from_observer} meters\n")
        f.write(f"  Confidence: ±{hive_location.confidence_radius} meters\n")
        f.write(f"  Note: In practice, nest often slightly further\n\n")

        f.write(f"Google Maps Link:\n")
        f.write(
            f"https://www.google.com/maps?q={hive_location.latitude},{hive_location.longitude}\n\n"
        )

        f.write("REPORT TO:\n")
        f.write("  Flanders: vespawatch.be\n")
        f.write("  Netherlands: waarneming.nl\n")
        f.write("  Wallonia: observatoire.biodiversite.wallonie.be\n")

    print(f"\n✓ Results saved to: {filename}")


def main():
    """Main program entry point."""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║       VESPAFINDER v0.3.0                                     ║")
    print("║       Professional Methodology (Vespawatchers)               ║")
    print("║       Protect bees by locating hornet nests                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    print("\n📚 Based on: 'Méthode de localisation des nids de frelons asiatiques'")
    print("   Author: Tom Vrancken (Vespawatchers group)")
    print("   Standard: 100 meters = 1 minute round trip time")

    # Get observation data
    observation = get_observation()

    # Calculate hive location
    calculator = HiveCalculator()
    hive_location = display_results(observation, calculator)

    # Offer to save
    save = input("\nSave results to file? (y/n): ").strip().lower()
    if save == "y":
        save_to_file(observation, hive_location)

    print("\n🐝 Thank you for helping protect bees!")
    print("   Continue tracking to refine location (relocation method)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
