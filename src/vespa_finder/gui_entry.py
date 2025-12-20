#!/usr/bin/env python3
"""VespaFinder GUI entry point for PyInstaller."""
# ruff: noqa: T201, PLC0415

import os
import sys


def main():
    """Main entry point for GUI application."""
    # Add src to path if running from package
    if getattr(sys, "frozen", False):
        # Running as compiled executable
        application_path = os.path.dirname(sys.executable)
    else:
        # Running as script
        application_path = os.path.dirname(os.path.abspath(__file__))

    # Import and run the GUI
    try:
        # Try importing from the installed package first
        # Import the main GUI class - we need to import the gui module
        import importlib.util
        import tkinter as tk
        import webbrowser
        from datetime import datetime
        from tkinter import messagebox, ttk

        from vespa_finder import HiveCalculator, Observation
        from vespa_finder.geo_utils import format_bearing, format_coordinates
        from vespa_finder.simple_map import SimpleMapGenerator
        from vespa_finder.translations import get_text

        # For frozen app, gui.py should be bundled
        if getattr(sys, "frozen", False):
            gui_path = os.path.join(application_path, "gui.py")
        else:
            # Development mode - gui.py is at project root
            gui_path = os.path.join(os.path.dirname(application_path), "..", "..", "gui.py")
            gui_path = os.path.abspath(gui_path)

        if os.path.exists(gui_path):
            spec = importlib.util.spec_from_file_location("gui", gui_path)
            gui_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(gui_module)
            gui_module.main()
        else:
            # Fallback: try direct import (when installed as package)
            root = tk.Tk()
            root.title("VespaFinder")
            root.geometry("400x200")

            label = ttk.Label(
                root,
                text="VespaFinder v0.3.0\n\nGUI module not found.\nPlease run from project directory:\n\npython gui.py",
                justify=tk.CENTER,
            )
            label.pack(expand=True)

            root.mainloop()

    except ImportError as e:
        print(f"Error importing GUI dependencies: {e}")
        print("Make sure tkinter is installed on your system.")
        sys.exit(1)


if __name__ == "__main__":
    main()
