#!/usr/bin/env python3
"""VespaFinder CLI entry point."""

import sys


def main():
    """Main entry point for CLI."""
    # Import here to avoid circular imports
    from . import HiveCalculator, Observation
    from .geo_utils import format_bearing, format_coordinates

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║       VESPAFINDER v0.3.0                                     ║")
    print("║       Professional Methodology (Vespawatchers)               ║")
    print("║       Protect bees by locating hornet nests                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # For now, delegate to main.py logic
    # This can be expanded later
    print("\nFor full CLI, run: python main.py")
    print("For GUI, run: python gui.py or vespa-finder-gui")


if __name__ == "__main__":
    main()
