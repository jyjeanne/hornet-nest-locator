# 📱 VespaFinder Mobile Application - Development Plan

## Overview

This document outlines the comprehensive plan for developing native Android and iOS mobile applications for the Hornet Nest Locator (VespaFinder) project using the Kivy framework.

**Target Release**: v0.8.0 (Q1-Q2 2027)

---

## 🎯 Why Mobile?

### Field Work Requirements
Beekeepers and conservationists working in the field need:
- ✅ **Portability** - Lightweight device vs. laptop
- ✅ **Built-in sensors** - GPS, compass, accelerometer
- ✅ **Camera** - Document hornets and nests
- ✅ **Offline capability** - Work without internet connection
- ✅ **Long battery life** - Extended field sessions
- ✅ **One-handed operation** - Easier in field conditions

### Current Desktop Limitations
- ❌ Requires laptop in field (heavy, fragile)
- ❌ Separate GPS device needed
- ❌ Separate compass required
- ❌ Separate stopwatch/chronometer
- ❌ Separate camera for documentation
- ❌ Internet connection often required for maps

### Mobile Advantages
- ✅ All-in-one device
- ✅ Native GPS with high accuracy
- ✅ Built-in compass (magnetometer)
- ✅ High-precision timer
- ✅ Quality camera with GPS metadata
- ✅ Touch-optimized interface
- ✅ Push notifications for reminders
- ✅ Offline maps and data storage

---

## 🛠️ Technology Stack

### Framework: Kivy 2.3.0+

**Why Kivy?**
- ✅ **Pure Python** - Reuse existing codebase (calculator.py, models.py, geo_utils.py)
- ✅ **Cross-platform** - Single codebase for Android + iOS
- ✅ **Native performance** - Compiles to native code via Cython
- ✅ **Active community** - Well-maintained with good documentation
- ✅ **Rich widgets** - Built-in UI components for mobile
- ✅ **Gesture support** - Touch, swipe, pinch-to-zoom
- ✅ **Proven track record** - Used in many production apps

**Alternatives Considered:**
- ❌ **Flutter** - Requires Dart (different language)
- ❌ **React Native** - Requires JavaScript/React
- ❌ **Native (Java/Kotlin)** - Complete rewrite, can't reuse Python code
- ❌ **Xamarin** - Requires C#

### Build Tools

#### Android
- **Buildozer** - Automated packaging for Android
- **Python-for-Android (p4a)** - Python to Android APK compiler
- **Cython** - Python to C compilation for performance
- **Android SDK/NDK** - Android development tools

#### iOS (Future)
- **Kivy-iOS** - iOS toolchain for Kivy
- **Xcode** - Apple's IDE for iOS development
- **CocoaPods** - Dependency management for iOS

### Core Libraries

```python
# Existing codebase (reusable)
vespa_finder/
├── calculator.py       # ✅ Reuse as-is
├── models.py          # ✅ Reuse as-is
├── geo_utils.py       # ✅ Reuse as-is
├── simple_map.py      # ⚠️ Adapt for mobile webview
└── translations.py    # ✅ Reuse as-is

# Kivy-specific additions
mobile/
├── main.py           # Kivy app entry point
├── ui/
│   ├── screens/      # Different screens (observation, map, settings)
│   ├── widgets/      # Custom widgets (GPS display, compass, timer)
│   └── layouts/      # Layout definitions (.kv files)
├── platform/
│   ├── android/      # Android-specific code (GPS, camera, sensors)
│   └── ios/          # iOS-specific code (future)
└── storage/
    └── database.py   # SQLite for local storage
```

### Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.12"
kivy = "^2.3.0"
kivymd = "^1.2.0"              # Material Design components
plyer = "^2.1.0"               # Platform-specific APIs (GPS, camera, compass)
pyjnius = "^1.6.0"             # Android Java/Python bridge
sqlite3 = "^3.0"               # Built-in, for local storage
requests = "^2.32.0"           # HTTP requests (existing)
folium = "^0.15.0"             # Maps (existing, via WebView)

[tool.poetry.group.dev.dependencies]
buildozer = "^1.5.0"           # Android packaging
cython = "^3.0.0"              # Performance optimization
black = "^24.0.0"              # Code formatting
pytest = "^8.0.0"              # Testing
```

---

## 📱 Feature Set

### Core Features (MVP - Minimum Viable Product)

#### 1. GPS Integration
- **Live location display**
  - Latitude/longitude in decimal degrees
  - Accuracy indicator (±X meters)
  - Altitude display
  - Location refresh rate: 1 second

- **GPS status indicators**
  - Signal strength (1-5 bars)
  - Satellite count
  - Fix type (GPS, GLONASS, GALILEO)
  - Last update timestamp

- **Manual coordinate entry**
  - Fallback for poor GPS signal
  - Copy/paste from other apps
  - Coordinate format validation

#### 2. Digital Compass
- **360° bearing display**
  - Visual compass rose
  - Numeric bearing (0-360°)
  - Cardinal directions (N, NE, E, SE, S, SW, W, NW)
  - Magnetic declination correction

- **Bearing measurement modes**
  - **Point & capture** - Point phone, tap to record
  - **Lock bearing** - Freeze bearing while moving
  - **Average mode** - Average multiple readings

- **Compass calibration**
  - Figure-8 calibration routine
  - Accuracy indicator
  - Recalibration reminders

#### 3. High-Precision Timer
- **Round-trip stopwatch**
  - Start on hornet departure
  - Stop on hornet return
  - Display: MM:SS.ms (minutes:seconds.milliseconds)
  - Large start/stop button (easy with gloves)

- **Multi-measurement tracking**
  - Record 3-5 measurements automatically
  - Calculate average automatically
  - Flag outliers (>20% deviation)
  - Delete individual measurements

- **Timer features**
  - **Vibration feedback** - Haptic on start/stop
  - **Audio cues** - Optional beep/voice feedback
  - **Lap times** - Record intermediate times
  - **Timer history** - Review past measurements

#### 4. Observation Recording
- **Quick observation entry**
  - GPS auto-filled from current location
  - Bearing auto-filled from compass
  - Timer values auto-populated
  - One-tap "Save Observation" button

- **Optional fields**
  - Hornet color mark (white/yellow/red)
  - Weather conditions (sunny/cloudy/rainy)
  - Temperature (manual or from weather API)
  - Wind speed/direction
  - Notes (voice-to-text supported)

- **Photo documentation**
  - Camera integration
  - GPS metadata embedded in photos
  - Timestamp overlay
  - Photo gallery per observation
  - Compress for storage

#### 5. Map Visualization
- **Interactive map display**
  - OpenStreetMap base layer
  - Satellite imagery option
  - Offline map caching (10km radius)
  - Pinch-to-zoom, pan gestures

- **Map markers**
  - Blue: Observation point
  - Red: Calculated nest location
  - Red circle: Search zone
  - Flight path arrow
  - Custom marker icons

- **Navigation to nest**
  - "Navigate" button → opens Google Maps/Waze
  - Distance to target
  - Compass pointing to nest
  - Arrival notification

#### 6. Offline Capability
- **Local data storage**
  - SQLite database for observations
  - Cached map tiles (50MB limit)
  - Offline calculation engine
  - Queue for later sync

- **Sync features**
  - Auto-sync when online
  - Manual sync button
  - Conflict resolution
  - Backup to cloud (optional)

---

### Advanced Features (Post-MVP)

#### 7. Camera Integration
- **Hornet marking photos**
  - Before/after marking
  - Close-up of paint mark
  - Metadata: GPS, timestamp, observation ID

- **Nest documentation**
  - Photos with zoom lens
  - Distance estimation from photo
  - Tree/building identification
  - Share with authorities

#### 8. Voice Notes
- **Hands-free recording**
  - Voice button while observing
  - Automatic transcription (offline)
  - Attach to observation
  - Playback in field

#### 9. Team Collaboration
- **Share observations**
  - Export observation as JSON/GPX
  - Send via email/messaging apps
  - QR code for quick sharing
  - Team workspace (cloud)

- **Multi-user triangulation**
  - Import observations from team members
  - Automatic triangulation calculation
  - Visual intersection display
  - Team chat integration

#### 10. Smart Features
- **Auto-start timer**
  - Detect when hornet leaves (motion?)
  - Optional feature (can be disabled)

- **Bearing assist**
  - AR (Augmented Reality) overlay
  - Point camera at hornet
  - Bearing auto-captured

- **Weather integration**
  - Auto-fetch weather data
  - Warn if conditions poor
  - Historical weather correlation

---

## 🎨 User Interface Design

### Design Principles
1. **Large touch targets** - Minimum 48×48 dp (9mm)
2. **High contrast** - Readable in sunlight
3. **One-handed operation** - Important controls within thumb reach
4. **Minimal text input** - Use pickers, sliders, buttons
5. **Clear hierarchy** - Most important info at top
6. **Consistent navigation** - Bottom nav bar or drawer

### Screen Flow

```
App Launch
    ↓
┌─────────────────────┐
│   Home Screen       │
│                     │
│  [New Observation]  │ ← Primary action
│  [View Map]         │
│  [History]          │
│  [Settings]         │
└─────────────────────┘
    ↓ (Tap "New Observation")
┌─────────────────────┐
│  Observation Screen │
│                     │
│  GPS: 48.8584°N     │ ← Auto-populated
│       2.2945°E      │
│                     │
│  Bearing: 135°      │ ← From compass
│  [Capture Bearing]  │
│                     │
│  Timer: 00:06:30    │
│  [Start] [Stop]     │
│                     │
│  [Calculate & Map]  │ ← Submit
└─────────────────────┘
    ↓
┌─────────────────────┐
│   Map Screen        │
│                     │
│  [Interactive Map]  │
│   🔵 You           │
│   🔴 Nest          │
│   ⭕ Search zone   │
│                     │
│  [Navigate to Nest] │
│  [Save Report]      │
└─────────────────────┘
```

### UI Mockup (Text-based)

```
┌──────────────────────────────────┐
│ VespaFinder        🔋 89%  📶    │ ← Status bar
├──────────────────────────────────┤
│                                  │
│  📍 GPS Location                 │
│  ┌────────────────────────────┐ │
│  │  Lat:  48.8584°N           │ │
│  │  Lon:   2.2945°E           │ │
│  │  Accuracy: ±5m             │ │
│  │  🛰️ 12 satellites          │ │
│  └────────────────────────────┘ │
│                                  │
│  🧭 Bearing                      │
│  ┌────────────────────────────┐ │
│  │        N                    │ │
│  │    NW  ↑  NE               │ │
│  │  W  ← 135° →  E            │ │
│  │    SW  ↓  SE               │ │
│  │        S                    │ │
│  │                             │ │
│  │  [📸 Capture Bearing]      │ │
│  └────────────────────────────┘ │
│                                  │
│  ⏱️ Round Trip Timer            │
│  ┌────────────────────────────┐ │
│  │                             │ │
│  │      06:30.45               │ │ ← Large display
│  │                             │ │
│  │  [▶️ START]  [⏸️ STOP]     │ │ ← Big buttons
│  └────────────────────────────┘ │
│                                  │
│  📊 Measurements (3)             │
│  • 06:28 • 06:32 • 06:30 ✓     │
│  Average: 06:30                 │
│                                  │
│  ┌────────────────────────────┐ │
│  │   🗺️ CALCULATE & MAP       │ │ ← Primary CTA
│  └────────────────────────────┘ │
│                                  │
├──────────────────────────────────┤
│  🏠  📍  📊  ⚙️                 │ ← Bottom nav
└──────────────────────────────────┘
```

### Color Scheme
- **Primary**: `#2196F3` (Blue) - Actions, buttons
- **Accent**: `#FFC107` (Amber) - Highlights, warnings
- **Success**: `#4CAF50` (Green) - GPS lock, completed
- **Warning**: `#FF9800` (Orange) - Caution
- **Error**: `#F44336` (Red) - Errors, nest marker
- **Background**: `#FFFFFF` / `#121212` (Light/Dark mode)
- **Text**: `#212121` / `#E0E0E0` (Light/Dark mode)

---

## 🔧 Technical Architecture

### App Structure

```
VespaFinderMobile/
├── buildozer.spec              # Build configuration
├── main.py                     # App entry point
├── assets/
│   ├── icons/                  # App icons (adaptive, legacy)
│   ├── images/                 # UI images, splash screen
│   ├── fonts/                  # Custom fonts
│   └── sounds/                 # Timer beeps, notifications
├── data/
│   └── offline_maps/           # Cached map tiles
├── kv/                         # Kivy language files
│   ├── main.kv                # Main layout
│   ├── observation.kv         # Observation screen
│   ├── map.kv                 # Map screen
│   └── settings.kv            # Settings screen
├── libs/                       # Reused Python modules
│   ├── vespa_finder/          # Copied from desktop app
│   │   ├── calculator.py
│   │   ├── models.py
│   │   ├── geo_utils.py
│   │   └── translations.py
│   └── utils/
│       ├── gps.py             # GPS handling
│       ├── compass.py         # Compass/magnetometer
│       ├── camera.py          # Camera integration
│       └── storage.py         # SQLite database
├── screens/                    # Screen classes
│   ├── home.py
│   ├── observation.py
│   ├── map_view.py
│   ├── history.py
│   └── settings.py
└── tests/
    ├── test_gps.py
    ├── test_compass.py
    └── test_calculation.py
```

### Data Model

```python
# SQLite Schema
CREATE TABLE observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    bearing REAL NOT NULL,
    round_trip_time REAL NOT NULL,  -- seconds
    hornet_mark TEXT,
    weather TEXT,
    temperature REAL,
    notes TEXT,
    photos TEXT,  -- JSON array of photo paths
    synced INTEGER DEFAULT 0,  -- 0 = not synced, 1 = synced
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hive_locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    observation_id INTEGER,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    distance REAL NOT NULL,
    confidence_radius REAL NOT NULL,
    method TEXT DEFAULT 'empirical',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (observation_id) REFERENCES observations(id)
);

CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

---

## 📐 Development Phases

### Phase 1: Core Kivy UI (2 months)

**Goals:**
- Set up Kivy development environment
- Create basic app structure
- Implement screen navigation
- Design UI layouts in .kv files

**Deliverables:**
- Working app skeleton
- Home, Observation, Map, Settings screens
- Bottom navigation
- Theme switching (light/dark)

**Tasks:**
1. Install Kivy, KivyMD, Buildozer
2. Create project structure
3. Design main.kv layout file
4. Implement screen manager
5. Create observation input form
6. Add basic validation
7. Test on desktop (Kivy runs on desktop too!)

---

### Phase 2: GPS & Sensor Integration (1 month)

**Goals:**
- Access Android GPS
- Read compass/magnetometer
- Display live sensor data
- Handle permissions

**Deliverables:**
- Live GPS coordinates on screen
- Digital compass with bearing
- Sensor accuracy indicators
- Permission handling

**Tasks:**
1. Use Plyer for GPS access
2. Implement GPS permission request
3. Display lat/lon in real-time
4. Access magnetometer for compass
5. Calculate bearing from sensor
6. Add calibration routine
7. Handle GPS/sensor errors gracefully

**Code Example:**
```python
from plyer import gps, compass

class ObservationScreen(Screen):
    def on_start_gps(self):
        try:
            gps.configure(on_location=self.on_location)
            gps.start(minTime=1000, minDistance=0)
        except NotImplementedError:
            # GPS not available on this platform
            self.show_error("GPS not available")

    def on_location(self, **kwargs):
        self.latitude = kwargs.get('lat')
        self.longitude = kwargs.get('lon')
        self.accuracy = kwargs.get('accuracy')
        self.update_ui()
```

---

### Phase 3: Map & Navigation (1 month)

**Goals:**
- Display interactive map
- Show observation and nest markers
- Offline map caching
- Navigate to nest location

**Deliverables:**
- WebView-based Leaflet map
- Custom markers and circles
- Zoom/pan gestures
- Offline tile storage

**Tasks:**
1. Integrate Folium maps in WebView
2. Generate HTML map from Python
3. Add markers (observation, nest)
4. Implement tile caching
5. Create navigation button
6. Launch external navigation app
7. Test offline functionality

**Code Example:**
```python
import folium
from kivy.uix.webview import WebView

def generate_map(observation, hive_location):
    m = folium.Map(
        location=[observation.latitude, observation.longitude],
        zoom_start=14
    )

    # Add markers
    folium.Marker(
        [observation.latitude, observation.longitude],
        popup="Observation Point",
        icon=folium.Icon(color='blue')
    ).add_to(m)

    folium.Marker(
        [hive_location.latitude, hive_location.longitude],
        popup="Estimated Nest",
        icon=folium.Icon(color='red')
    ).add_to(m)

    # Save to HTML
    map_path = '/sdcard/vespafinder/map.html'
    m.save(map_path)
    return map_path
```

---

### Phase 4: Camera & Media (1 month)

**Goals:**
- Camera integration for photos
- Photo gallery per observation
- GPS metadata in photos
- Voice note recording

**Deliverables:**
- Take photos with camera
- View photo gallery
- Record voice notes
- Attach media to observations

**Tasks:**
1. Use Plyer camera API
2. Save photos with GPS EXIF data
3. Create photo gallery widget
4. Implement voice recorder
5. Add audio playback
6. Compress photos for storage
7. Associate media with observations

---

### Phase 5: Testing & Optimization (1 month)

**Goals:**
- Test on real Android devices
- Optimize performance
- Reduce APK size
- Fix bugs

**Deliverables:**
- Stable release candidate
- Performance benchmarks
- Bug fixes
- APK under 50MB

**Tasks:**
1. Test on Android 8.0, 9.0, 10, 11, 12, 13, 14
2. Test on different screen sizes
3. Optimize Cython compilation
4. Remove unused dependencies
5. Compress assets
6. Profile memory usage
7. Battery consumption testing
8. Fix critical bugs
9. User acceptance testing

---

### Phase 6: Play Store Release (0.5 months)

**Goals:**
- Prepare Play Store listing
- Create promotional materials
- Submit for review
- Launch to public

**Deliverables:**
- Published app on Google Play
- App store screenshots
- Description and changelog
- Privacy policy

**Tasks:**
1. Create Google Play Developer account
2. Design app icon (512×512)
3. Take screenshots (phone, tablet, 7-inch)
4. Write app description
5. Create feature graphic
6. Set up app pricing (free)
7. Submit for review
8. Respond to review feedback
9. Publish!

---

## 📊 Success Metrics

### Technical KPIs
- **App size**: < 50 MB
- **Startup time**: < 3 seconds
- **GPS accuracy**: ± 5 meters
- **Compass accuracy**: ± 5 degrees
- **Battery drain**: < 10% per hour
- **Crash rate**: < 1%
- **App rating**: > 4.0 stars

### User Adoption
- **Downloads**: 1,000+ in first 3 months
- **Active users**: 500+ monthly
- **Retention**: 40%+ after 30 days
- **Reviews**: 100+ reviews
- **Observations**: 500+ recorded via mobile

---

## 🚧 Challenges & Solutions

### Challenge 1: GPS Accuracy in Forest
**Problem**: Trees block GPS signals
**Solution**:
- Use GLONASS + GPS + Galileo
- Average multiple readings
- Manual coordinate entry fallback
- External GPS device via Bluetooth

### Challenge 2: Battery Life
**Problem**: GPS + sensors drain battery
**Solution**:
- Optimize GPS update frequency
- Sleep sensors when not in use
- Dark theme reduces screen power
- Battery saver mode

### Challenge 3: Offline Maps
**Problem**: Map tiles require storage
**Solution**:
- Cache only needed tiles (50MB limit)
- User selects region to download
- Clear cache button
- Fallback to minimal map

### Challenge 4: App Size
**Problem**: Kivy apps can be large
**Solution**:
- Remove unused modules
- Use ProGuard/R8 for Android
- Compress assets (images, fonts)
- Use vector graphics where possible

---

## 📚 Resources

### Documentation
- **Kivy**: https://kivy.org/doc/stable/
- **KivyMD**: https://kivymd.readthedocs.io/
- **Buildozer**: https://buildozer.readthedocs.io/
- **Plyer**: https://plyer.readthedocs.io/

### Tutorials
- Kivy Crash Course: https://www.youtube.com/watch?v=F7UKmK9eQLY
- Android App with Kivy: https://realpython.com/mobile-app-kivy-python/

### Community
- Kivy Discord: https://chat.kivy.org/
- Kivy Forum: https://groups.google.com/g/kivy-users
- Stack Overflow: [kivy] tag

---

## ✅ Next Steps

1. **Research Phase** (Current)
   - Review Kivy documentation
   - Test Kivy on desktop
   - Prototype basic UI
   - Verify sensor APIs available

2. **Prototype** (Next)
   - Create minimal Kivy app
   - Test GPS on Android device
   - Implement compass
   - Build first APK

3. **MVP Development**
   - Follow Phase 1-6 timeline
   - Regular testing on devices
   - Community feedback
   - Iterate based on testing

4. **Launch**
   - Beta testing program
   - Play Store submission
   - Marketing campaign
   - User support setup

---

**Target Timeline**: 6.5 months from start to Play Store release
**Estimated Effort**: 800-1000 development hours
**Team Size**: 1-2 developers (mobile focus)

---

> "Bringing professional hornet nest location tools to every beekeeper's pocket!" 📱🐝
