#!/usr/bin/env python3
"""
VespaFinder - Beautiful GUI Application
Professional methodology by Vespawatchers
"""

import logging
import os
import tkinter as tk
import traceback
import webbrowser
from datetime import datetime
from tkinter import messagebox, scrolledtext, ttk
from typing import Optional

from vespa_finder import HiveCalculator, Observation
from vespa_finder.geo_utils import format_bearing, format_coordinates
from vespa_finder.models import HiveLocation
from vespa_finder.simple_map import SimpleMapGenerator
from vespa_finder.translations import get_text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ScrollableFrame(ttk.Frame):
    """A scrollable frame container."""

    def __init__(self, container: ttk.Widget, *args, **kwargs) -> None:
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self, borderwidth=0, background="#f0f0f0")
        # Create scrollbar with explicit width for better visibility
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        # Note: ttk.Scrollbar width is controlled by the theme, but we configure the style
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind("<Enter>", lambda e: self._bind_mousewheel(canvas))
        self.scrollable_frame.bind("<Leave>", lambda e: self._unbind_mousewheel(canvas))

        self.canvas = canvas

    def _bind_mousewheel(self, canvas: tk.Canvas) -> None:
        canvas.bind_all(
            "<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    def _unbind_mousewheel(self, canvas: tk.Canvas) -> None:
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")


class HornetLocatorGUI:
    """Beautiful GUI for Hornet Nest Locator."""

    # Widget width standards for consistent UI
    ENTRY_WIDTH_STANDARD = 20  # Standard width for most entry fields
    ENTRY_WIDTH_SMALL = 10     # For numeric inputs like minutes, seconds, speed

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.current_lang = "en"  # Default language

        # Cache for translations to improve performance (initialize early)
        self._translation_cache: dict[str, str] = {}

        self.root.title(self.t("window_title"))

        # Responsive window sizing based on screen resolution
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Use 70% of screen width and 80% of screen height, with min/max constraints
        window_width = max(900, min(1400, int(screen_width * 0.7)))
        window_height = max(800, min(1200, int(screen_height * 0.8)))

        # Center window on screen
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.minsize(900, 800)  # Set minimum window size

        self.setup_styles()

        self.calculator = HiveCalculator()
        self.map_generator = SimpleMapGenerator()
        self.observations = []
        self.current_map_file = None
        self.current_hive_location = None

        # Ensure maps directory exists in project folder
        self.maps_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
        os.makedirs(self.maps_dir, exist_ok=True)

        # Store references to all labels and buttons for language switching
        self.labels = {}
        self.buttons = {}

        self.create_widgets()

    def t(self, key: str) -> str:
        """Get translated text for current language with caching."""
        cache_key = f"{self.current_lang}:{key}"
        if cache_key not in self._translation_cache:
            self._translation_cache[cache_key] = get_text(self.current_lang, key)
        return self._translation_cache[cache_key]

    def switch_language(self) -> None:
        """Switch between English and French."""
        self.current_lang = "fr" if self.current_lang == "en" else "en"
        # Clear translation cache when switching languages
        self._translation_cache.clear()
        self.update_all_labels()

    def update_all_labels(self) -> None:
        """Update all text labels and buttons when language changes."""
        # Update window title
        self.root.title(self.t("window_title"))

        # Update language button text (show opposite language)
        if self.current_lang == "en":
            self.buttons["language"].config(text="🇫🇷 FR")
        else:
            self.buttons["language"].config(text="🇬🇧 EN")

        # Update header labels
        self.labels["title"].config(text="🐝 Hornet Nest Locator")
        self.labels["subtitle"].config(
            text="Professional Methodology - Vespawatchers Standard (100m/min)"
        )

        # Update LabelFrame titles
        self.input_labelframe.config(text=f"📍 {self.t('input_panel_title')}")
        self.results_labelframe.config(text=f"📊 {self.t('results_panel_title')}")

        # Update section labels
        self.labels["gps_section"].config(text=f"1. {self.t('gps_section').upper()}")
        self.labels["latitude"].config(text=self.t("latitude"))
        self.labels["longitude"].config(text=self.t("longitude"))

        self.labels["flight_section"].config(text=f"2. {self.t('flight_section').upper()}")
        self.labels["bearing"].config(text=self.t("bearing"))
        self.labels["bearing_help"].config(text="N↑ NE↗ E→ SE↘\nS↓ SW↙ W← NW↖")

        self.labels["round_trip_section"].config(text=f"3. {self.t('round_trip').upper()}")
        self.labels["round_trip_warning"].config(
            text=self.t("warning_measure")
            if self.current_lang == "fr"
            else "⚠️ Measure multiple times!"
        )
        self.labels["minutes"].config(text=self.t("minutes"))
        self.labels["seconds"].config(text=self.t("seconds"))

        self.labels["optional_section"].config(text=f"4. {self.t('optional_section').upper()}")
        self.labels["hornet_mark"].config(text=self.t("hornet_mark"))
        self.labels["speed"].config(text=self.t("speed"))
        self.labels["notes"].config(text=self.t("notes"))

        # Update buttons
        self.buttons["calculate"].config(text=f"🎯 {self.t('calculate').upper()}")
        self.buttons["gps_help"].config(text=f"📍 {self.t('gps_help')}")
        self.buttons["view_map"].config(text=f"🗺️ {self.t('view_map')}")
        self.buttons["print_map"].config(text=f"🖨️ {self.t('print_map')}")
        self.buttons["save_report"].config(text=f"💾 {self.t('save_report')}")
        self.buttons["clear"].config(text=f"🔄 {self.t('clear')}")

        # Update initial results text if no calculation has been done yet
        if not self.observations:
            self.update_initial_results_text()

    def update_initial_results_text(self) -> None:
        """Update the initial help text in the results panel."""
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)

        if self.current_lang == "en":
            initial_text = f"""
╔══════════════════════════════════════════════════════════╗
║   HORNET HIVE LOCATOR - PROFESSIONAL EDITION             ║
║   Based on Vespawatchers Methodology                     ║
╚══════════════════════════════════════════════════════════╝

📋 QUICK START:

1. Enter your GPS coordinates (observation point)
2. Enter compass bearing (0-360°, where hornet flew)
3. Enter round trip time (minutes + seconds)
4. Optional: Enter speed for method comparison
5. Scroll down in the left panel if needed
6. Click "🎯 CALCULATE HIVE LOCATION"

📐 PROFESSIONAL FORMULA:
   100 meters = 1 minute round trip time
   (Vespawatchers empirical standard)

🔍 ESSENTIAL EQUIPMENT:
   • Binoculars 8×42 (MOST IMPORTANT TOOL!)
   • Wick pot with sugar bait
   • Color markers (white recommended)
   • Butterfly net, compass, stopwatch

🗺️ MAP FEATURES:
   After calculation, the map opens in your browser:
   🔵 Blue marker = Your observation point
   🔴 Red marker = Estimated hive location
   ⭕ Red circle = Search zone (where to look!)
   ➡️ Blue arrow = Flight direction
   --- Red dashed line = Flight path

📁 MAPS SAVED TO:
   {self.maps_dir}

⚠️  SAFETY:
   • Never approach nest alone
   • Use protective equipment
   • Contact professional pest control
   • Report to: vespawatch.be / waarneming.nl

🐝 Ready to locate hornet nests and protect bees!
            """
        else:
            initial_text = f"""
╔══════════════════════════════════════════════════════════╗
║   LOCALISATEUR DE NID DE FRELONS - ÉDITION PRO          ║
║   Basé sur la Méthodologie Vespawatchers                 ║
╚══════════════════════════════════════════════════════════╝

📋 DÉMARRAGE RAPIDE :

1. Entrez vos coordonnées GPS (point d'observation)
2. Entrez le cap au compas (0-360°, direction du frelon)
3. Entrez le temps d'aller-retour (minutes + secondes)
4. Optionnel : Entrez la vitesse pour comparaison
5. Faites défiler le panneau de gauche si nécessaire
6. Cliquez sur "🎯 CALCULER LA POSITION DU NID"

📐 FORMULE PROFESSIONNELLE :
   100 mètres = 1 minute temps aller-retour
   (Standard empirique Vespawatchers)

🔍 ÉQUIPEMENT ESSENTIEL :
   • Jumelles 8×42 (OUTIL LE PLUS IMPORTANT !)
   • Pot à mèche avec appât sucré
   • Marqueurs de couleur (blanc recommandé)
   • Filet à papillons, boussole, chronomètre

🗺️ FONCTIONNALITÉS DE LA CARTE :
   Après calcul, la carte s'ouvre dans votre navigateur :
   🔵 Marqueur bleu = Votre point d'observation
   🔴 Marqueur rouge = Position estimée du nid
   ⭕ Cercle rouge = Zone de recherche (où chercher !)
   ➡️ Flèche bleue = Direction du vol
   --- Ligne pointillée rouge = Trajet du vol

📁 CARTES SAUVEGARDÉES DANS :
   {self.maps_dir}

⚠️  SÉCURITÉ :
   • Ne jamais approcher le nid seul
   • Utiliser un équipement de protection
   • Contacter un professionnel de lutte antiparasitaire
   • Signaler sur : vespawatch.be / waarneming.nl

🐝 Prêt à localiser les nids de frelons et protéger les abeilles !
            """

        self.results_text.insert("1.0", initial_text)
        self.results_text.config(state="disabled")

    def setup_styles(self) -> None:
        """Configure modern styles."""
        style = ttk.Style()
        style.theme_use("clam")

        primary_color = "#2c3e50"
        accent_color = "#e74c3c"
        success_color = "#27ae60"

        style.configure("Title.TLabel", font=("Arial", 16, "bold"), foreground=primary_color)
        style.configure("Subtitle.TLabel", font=("Arial", 12, "bold"), foreground=primary_color)
        style.configure("Info.TLabel", font=("Arial", 10), foreground="#555")
        style.configure("Success.TLabel", font=("Arial", 10, "bold"), foreground=success_color)
        style.configure("Warning.TLabel", font=("Arial", 10, "bold"), foreground=accent_color)
        style.configure("Calculate.TButton", font=("Arial", 12, "bold"), padding=10)
        style.configure("Action.TButton", font=("Arial", 10), padding=5)

        # Configure scrollbar for better visibility
        style.configure("Vertical.TScrollbar", arrowsize=15, width=16)

    def create_widgets(self) -> None:
        """Create all GUI widgets."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        self.create_header(main_frame)
        self.create_input_panel(main_frame)
        self.create_results_panel(main_frame)

    def create_header(self, parent: ttk.Frame) -> None:
        """Create header section."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)

        self.labels["title"] = ttk.Label(
            header_frame, text="🐝 Hornet Nest Locator", style="Title.TLabel"
        )
        self.labels["title"].grid(row=0, column=0, sticky=tk.W)

        # Language switcher button
        self.buttons["language"] = ttk.Button(
            header_frame,
            text="🇫🇷 FR",
            command=self.switch_language,
            style="Action.TButton",
            width=10,
        )
        self.buttons["language"].grid(row=0, column=1, sticky=tk.E, padx=5)

        self.labels["subtitle"] = ttk.Label(
            header_frame,
            text="Professional Methodology - Vespawatchers Standard (100m/min)",
            style="Info.TLabel",
        )
        self.labels["subtitle"].grid(row=1, column=0, columnspan=2, sticky=tk.W)

    def create_input_panel(self, parent: ttk.Frame) -> None:
        """Create input form panel with scrollbar."""
        self.input_labelframe = ttk.LabelFrame(
            parent, text=f"📍 {self.t('input_panel_title')}", padding="5"
        )
        self.input_labelframe.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        self.input_labelframe.rowconfigure(0, weight=1)
        self.input_labelframe.columnconfigure(0, weight=1)

        scrollable = ScrollableFrame(self.input_labelframe)
        scrollable.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        input_frame = scrollable.scrollable_frame
        row = 0

        # GPS Section
        self.labels["gps_section"] = ttk.Label(
            input_frame, text=f"1. {self.t('gps_section').upper()}", style="Subtitle.TLabel"
        )
        self.labels["gps_section"].grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(5, 10))
        row += 1

        self.labels["latitude"] = ttk.Label(input_frame, text=self.t("latitude"))
        self.labels["latitude"].grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
        self.lat_entry = ttk.Entry(input_frame, width=self.ENTRY_WIDTH_STANDARD)
        self.lat_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.lat_entry.insert(0, "48.8584")
        row += 1

        self.labels["longitude"] = ttk.Label(input_frame, text=self.t("longitude"))
        self.labels["longitude"].grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
        self.lon_entry = ttk.Entry(input_frame, width=self.ENTRY_WIDTH_STANDARD)
        self.lon_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.lon_entry.insert(0, "2.2945")
        row += 1

        self.buttons["gps_help"] = ttk.Button(
            input_frame,
            text=f"📍 {self.t('gps_help')}",
            command=self.open_gps_help,
            style="Action.TButton",
        )
        self.buttons["gps_help"].grid(row=row, column=0, columnspan=2, pady=5)
        row += 1

        ttk.Separator(input_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        row += 1

        # Flight Direction Section
        self.labels["flight_section"] = ttk.Label(
            input_frame, text=f"2. {self.t('flight_section').upper()}", style="Subtitle.TLabel"
        )
        self.labels["flight_section"].grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        row += 1

        self.labels["bearing"] = ttk.Label(input_frame, text=self.t("bearing"))
        self.labels["bearing"].grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
        self.bearing_entry = ttk.Entry(input_frame, width=self.ENTRY_WIDTH_SMALL)
        self.bearing_entry.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
        self.bearing_entry.insert(0, "45")
        row += 1

        self.labels["bearing_help"] = ttk.Label(
            input_frame, text="N↑ NE↗ E→ SE↘\nS↓ SW↙ W← NW↖", style="Info.TLabel", justify=tk.CENTER
        )
        self.labels["bearing_help"].grid(row=row, column=0, columnspan=2, pady=5)
        row += 1

        ttk.Separator(input_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        row += 1

        # Round Trip Time Section
        self.labels["round_trip_section"] = ttk.Label(
            input_frame, text=f"3. {self.t('round_trip').upper()}", style="Subtitle.TLabel"
        )
        self.labels["round_trip_section"].grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        row += 1

        self.labels["round_trip_warning"] = ttk.Label(
            input_frame, text="⚠️ Measure multiple times!", style="Warning.TLabel"
        )
        self.labels["round_trip_warning"].grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        self.labels["minutes"] = ttk.Label(input_frame, text=self.t("minutes"))
        self.labels["minutes"].grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
        self.minutes_entry = ttk.Entry(input_frame, width=self.ENTRY_WIDTH_SMALL)
        self.minutes_entry.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
        self.minutes_entry.insert(0, "6")
        row += 1

        self.labels["seconds"] = ttk.Label(input_frame, text=self.t("seconds"))
        self.labels["seconds"].grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
        self.seconds_entry = ttk.Entry(input_frame, width=self.ENTRY_WIDTH_SMALL)
        self.seconds_entry.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
        self.seconds_entry.insert(0, "30")
        row += 1

        ttk.Separator(input_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        row += 1

        # Optional Section
        self.labels["optional_section"] = ttk.Label(
            input_frame, text=f"4. {self.t('optional_section').upper()}", style="Subtitle.TLabel"
        )
        self.labels["optional_section"].grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        row += 1

        self.labels["hornet_mark"] = ttk.Label(input_frame, text=self.t("hornet_mark"))
        self.labels["hornet_mark"].grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
        self.color_entry = ttk.Entry(input_frame, width=self.ENTRY_WIDTH_STANDARD)
        self.color_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        row += 1

        self.labels["speed"] = ttk.Label(input_frame, text=self.t("speed"))
        self.labels["speed"].grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
        self.speed_entry = ttk.Entry(input_frame, width=self.ENTRY_WIDTH_SMALL)
        self.speed_entry.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
        row += 1

        self.labels["notes"] = ttk.Label(input_frame, text=self.t("notes"))
        self.labels["notes"].grid(row=row, column=0, sticky=(tk.W, tk.N), pady=5, padx=5)
        self.notes_entry = tk.Text(input_frame, height=3)
        self.notes_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        row += 1

        ttk.Separator(input_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        row += 1

        # Calculate Button
        self.buttons["calculate"] = ttk.Button(
            input_frame,
            text=f"🎯 {self.t('calculate').upper()}",
            command=self.calculate_location,
            style="Calculate.TButton",
        )
        self.buttons["calculate"].grid(
            row=row, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E)
        )
        row += 1

        # Action Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)

        self.buttons["view_map"] = ttk.Button(
            button_frame,
            text=f"🗺️ {self.t('view_map')}",
            command=self.view_map,
            style="Action.TButton",
        )
        self.buttons["view_map"].pack(side=tk.LEFT, padx=2)

        self.buttons["print_map"] = ttk.Button(
            button_frame,
            text=f"🖨️ {self.t('print_map')}",
            command=self.print_map,
            style="Action.TButton",
        )
        self.buttons["print_map"].pack(side=tk.LEFT, padx=2)

        self.buttons["save_report"] = ttk.Button(
            button_frame,
            text=f"💾 {self.t('save_report')}",
            command=self.save_report,
            style="Action.TButton",
        )
        self.buttons["save_report"].pack(side=tk.LEFT, padx=2)

        self.buttons["clear"] = ttk.Button(
            button_frame,
            text=f"🔄 {self.t('clear')}",
            command=self.clear_form,
            style="Action.TButton",
        )
        self.buttons["clear"].pack(side=tk.LEFT, padx=2)
        row += 1

        ttk.Label(input_frame, text="").grid(row=row, column=0, pady=20)
        input_frame.columnconfigure(1, weight=1)

    def create_results_panel(self, parent: ttk.Frame) -> None:
        """Create results display panel with scrollbar."""
        self.results_labelframe = ttk.LabelFrame(
            parent, text=f"📊 {self.t('results_panel_title')}", padding="10"
        )
        self.results_labelframe.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        self.results_labelframe.rowconfigure(0, weight=1)
        self.results_labelframe.columnconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(
            self.results_labelframe, height=30, wrap=tk.WORD, font=("Courier", 10)
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.update_initial_results_text()

    def open_gps_help(self) -> None:
        """Open Google Maps for GPS coordinates."""
        webbrowser.open("https://www.google.com/maps")
        messagebox.showinfo(self.t("gps_help_title"), self.t("gps_help_message"))

    def calculate_location(self) -> None:
        """Calculate hive location from input data."""
        try:
            latitude = float(self.lat_entry.get())
            longitude = float(self.lon_entry.get())
            bearing = float(self.bearing_entry.get())
            minutes = float(self.minutes_entry.get())
            seconds = float(self.seconds_entry.get())
            round_trip_time = minutes * 60 + seconds

            color = self.color_entry.get().strip() or None
            speed_text = self.speed_entry.get().strip()
            speed = float(speed_text) if speed_text else None
            notes = self.notes_entry.get("1.0", tk.END).strip()

            observation = Observation(
                latitude=latitude,
                longitude=longitude,
                bearing=bearing,
                round_trip_time=round_trip_time,
                speed=speed,
                hornet_color_mark=color,
                notes=notes,
            )

            hive_empirical = self.calculator.calculate_from_single_observation(
                observation, method="empirical"
            )

            self.observations.append(observation)
            self.current_hive_location = hive_empirical

            # Generate map FIRST so self.current_map_file is set
            self.generate_and_open_map(observation, hive_empirical)
            # Then display results (which references self.current_map_file)
            self.display_results(observation, hive_empirical, speed)

            # Show success message with translation
            messagebox.showinfo(
                self.t("success_title"),
                self.t("success_message").format(filename=os.path.basename(self.current_map_file)),
            )
            logger.info(f"Successfully calculated hive location and generated map: {self.current_map_file}")

        except ValueError as e:
            logger.error(f"Validation error in calculate_location: {e}")
            messagebox.showerror(
                self.t("error_title"), self.t("error_message").format(error=str(e))
            )
        except (OSError, IOError) as e:
            logger.error(f"File I/O error in calculate_location: {e}")
            messagebox.showerror(
                "File Error",
                f"Failed to create or save map file: {e}"
            )
        except Exception as e:
            logger.exception(f"Unexpected error in calculate_location: {e}")
            messagebox.showerror(
                self.t("calc_error_title"), self.t("calc_error_message").format(error=str(e))
            )
            traceback.print_exc()

    def display_results(
        self, observation: Observation, hive_empirical: HiveLocation, speed: Optional[float]
    ) -> None:
        """Display calculation results."""
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)

        output = f"""
{"=" * 60}
{self.t("results_header")}
{"=" * 60}

{self.t("observation_point")}
  {self.t("location")} {format_coordinates(observation.latitude, observation.longitude)}
  {self.t("time")} {observation.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
  {f"{self.t('hornet_mark_label')} {observation.hornet_color_mark}" if observation.hornet_color_mark else ""}

{self.t("flight_data")}
  {self.t("direction")} {format_bearing(observation.bearing)}
  {self.t("round_trip_time")} {observation.round_trip_time:.0f}s ({observation.round_trip_time / 60:.2f}min)

{"=" * 60}
{self.t("empirical_method")}
{"=" * 60}
  {self.t("empirical_formula")}

  {self.t("calculated_distance")} {hive_empirical.distance_from_observer:.0f} meters
                       ({hive_empirical.distance_from_observer / 1000:.2f} km)

  {self.t("estimated_hive")}
     {self.t("coordinates")} {format_coordinates(hive_empirical.latitude, hive_empirical.longitude)}

     {self.t("bearing_from_you")} {format_bearing(hive_empirical.bearing_from_observer)}

     {self.t("confidence_radius")} ±{hive_empirical.confidence_radius:.0f} meters
     {self.t("search_zone_note")}

  {self.t("gps_nav")}
     {hive_empirical.latitude:.6f}, {hive_empirical.longitude:.6f}

  {self.t("google_maps")}
  https://www.google.com/maps?q={hive_empirical.latitude},{hive_empirical.longitude}

  {self.t("practice_note")}
"""

        if speed is not None:
            comparison = self.calculator.compare_methods(observation)
            output += f"""
{"=" * 60}
{self.t("theoretical_method")}
{"=" * 60}
  {self.t("theoretical_formula")}
  {self.t("speed_used")} {speed} m/s ({speed * 3.6:.1f} km/h)

  {self.t("calculated_distance")} {comparison["theoretical"].distance_from_observer:.0f} meters
                       ({comparison["theoretical"].distance_from_observer / 1000:.2f} km)

  📊 {self.t("difference")} {comparison["difference_meters"]:.0f} meters ({comparison["difference_percent"]:.1f}%)

  {self.t("recommended_method")}
"""

        if observation.notes:
            output += f"\n{self.t('notes_label')}\n{observation.notes}\n"

        output += f"""
{"=" * 60}
{self.t("map_info")}
{"=" * 60}
  {self.t("map_opened")}
  {self.t("map_saved")} {os.path.basename(self.current_map_file)}

  {self.t("map_features").format(radius=hive_empirical.confidence_radius)}

  {self.t("map_actions")}

{"=" * 60}
{self.t("next_steps")}
{"=" * 60}
  {self.t("equipment")}

  {self.t("search")}

  {self.t("safety")}
{"=" * 60}
"""

        self.results_text.insert("1.0", output)
        self.results_text.config(state="disabled")

    def generate_and_open_map(
        self, observation: Observation, hive_location: HiveLocation
    ) -> None:
        """Generate interactive map and open in browser."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.current_map_file = os.path.join(self.maps_dir, f"hornet_map_{timestamp}.html")

            self.map_generator.create_simple_map(
                observations=[observation],
                hive_locations=[hive_location],
                output_file=self.current_map_file,
            )

            # Open in browser
            webbrowser.open("file://" + os.path.abspath(self.current_map_file))
            logger.info(f"Map generated and opened: {self.current_map_file}")

        except (OSError, IOError) as e:
            logger.error(f"File I/O error generating map: {e}")
            messagebox.showerror(
                "Map Generation Error",
                f"Failed to create map file: {e}"
            )
        except Exception as e:
            logger.exception(f"Unexpected error generating map: {e}")
            messagebox.showerror(
                self.t("map_error_title"), self.t("map_error_message").format(error=str(e))
            )
            traceback.print_exc()

    def view_map(self) -> None:
        """Open/reopen map in browser."""
        if self.current_map_file and os.path.exists(self.current_map_file):
            webbrowser.open("file://" + os.path.abspath(self.current_map_file))
        else:
            messagebox.showwarning(self.t("no_map_title"), self.t("no_map_message"))

    def print_map(self) -> None:
        """Print the map."""
        if self.current_map_file and os.path.exists(self.current_map_file):
            webbrowser.open("file://" + os.path.abspath(self.current_map_file))
            messagebox.showinfo(self.t("print_title"), self.t("print_message"))
        else:
            messagebox.showwarning(self.t("no_map_title"), self.t("no_map_message"))

    def save_report(self) -> None:
        """Save results to file."""
        if not self.observations:
            messagebox.showwarning(self.t("no_data_title"), self.t("no_data_message"))
            return

        try:
            filename = f"hornet_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            content = self.results_text.get("1.0", tk.END)

            with open(filename, "w") as f:
                f.write(content)
                if self.current_map_file:
                    f.write(f"\n\nInteractive map file: {self.current_map_file}\n")

            messagebox.showinfo(
                self.t("saved_title"), self.t("saved_message").format(filename=filename)
            )
            logger.info(f"Report saved to: {filename}")
        except (OSError, IOError, PermissionError) as e:
            logger.error(f"File I/O error saving report: {e}")
            messagebox.showerror(
                self.t("save_error_title"), self.t("save_error_message").format(error=str(e))
            )
        except Exception as e:
            logger.exception(f"Unexpected error saving report: {e}")
            messagebox.showerror(
                self.t("save_error_title"), self.t("save_error_message").format(error=str(e))
            )

    def clear_form(self) -> None:
        """Clear the input form."""
        self.bearing_entry.delete(0, tk.END)
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)
        self.color_entry.delete(0, tk.END)
        self.speed_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)

        self.bearing_entry.insert(0, "45")
        self.minutes_entry.insert(0, "6")
        self.seconds_entry.insert(0, "30")


def main() -> None:
    """Launch the GUI application."""
    root = tk.Tk()
    app = HornetLocatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
