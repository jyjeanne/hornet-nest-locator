# Hornet Nest Locator - GUI User Guide

## 🎨 Beautiful Graphical Interface

A modern, user-friendly GUI for locating hornet nests with professional Vespawatchers methodology.

---

## 🚀 Quick Start

### Launch the GUI

```bash
cd /home/jeremy/hornet-nest-locator
uv run python gui.py
```

Or use the launcher:
```bash
./launch_gui.sh
```

---

## 📋 Interface Overview

### Left Panel: Data Entry Form

**1. GPS LOCATION**
- Enter your observation point coordinates
- Click "Get GPS from maps.google.com" for help
- Right-click on Google Maps → "What's here?"

**2. FLIGHT DIRECTION** 
- Enter compass bearing (0-360°)
- 0° = North, 90° = East, 180° = South, 270° = West
- Visual compass rose displayed for reference

**3. ROUND TRIP TIME**
- Minutes and seconds
- ⚠️ Measure multiple times until consistent!

**4. OPTIONAL FIELDS**
- Hornet mark color (for tracking individuals)
- Speed (m/s) for method comparison
- Notes (weather, confidence, etc.)

### Right Panel: Results Display

- Real-time calculation results
- GPS coordinates for navigation
- Google Maps link
- Professional methodology information
- Safety warnings and equipment checklist

---

## 🎯 How to Use

### Step 1: Enter Your Location
```
Latitude:  48.8584
Longitude: 2.2945
```

### Step 2: Enter Flight Direction
```
Bearing: 45  (Northeast)
```

### Step 3: Enter Round Trip Time
```
Minutes: 6
Seconds: 30
```

### Step 4: Click "CALCULATE HIVE LOCATION"

The app will:
- ✅ Calculate using professional empirical method (100m/min)
- ✅ Display estimated hive coordinates
- ✅ Show distance and bearing
- ✅ Calculate confidence radius
- ✅ Generate interactive map

### Step 5: View the Map

Click "🗺️ View Map" to open interactive browser map showing:
- 🔵 Your observation point (blue marker)
- 🔴 Estimated hive location (red marker)
- ⭕ Red confidence circle (search zone)
- ➡️ Flight direction arrow
- 📏 Distance measurements

---

## 🗺️ Map Features

The generated map includes:

1. **Your Position** (Blue Marker)
   - Shows exact observation point
   - Displays all observation data in popup

2. **Estimated Hive** (Red Marker)
   - Calculated location
   - Distance and bearing info
   - Google Maps link

3. **Search Zone** (Red Circle)
   - Confidence radius visualization
   - Area to search for nest
   - Adjusts based on uncertainty

4. **Flight Path** (Red Dashed Line)
   - Shows direction from you to hive
   - Estimated flight trajectory

5. **Interactive Controls**
   - Zoom in/out
   - Pan around
   - Click markers for details
   - Switch map layers

---

## 🎨 GUI Features

### Professional Design
- ✅ Clean, modern interface
- ✅ Color-coded information
- ✅ Clear section organization
- ✅ Easy-to-read fonts
- ✅ Intuitive layout

### Smart Input Validation
- Checks latitude range (-90 to 90)
- Checks longitude range (-180 to 180)
- Validates bearing (0-360°)
- Ensures positive time values
- Clear error messages

### Helpful Guides
- Compass rose diagram
- GPS coordinate help
- Formula explanation
- Equipment checklist
- Safety warnings

---

## 🔧 Action Buttons

### 🎯 CALCULATE HIVE LOCATION
- Main action button
- Performs calculation
- Generates map
- Updates results panel

### 🗺️ View Map
- Opens interactive map in browser
- Shows observation point and search zone
- Includes all markers and circles

### 💾 Save Report
- Saves results to text file
- Includes all calculations
- Timestamped filename
- Easy to share

### 🔄 Clear
- Resets input fields
- Keeps GPS coordinates
- Ready for new observation

---

## 📊 Results Display

### Empirical Method (Recommended)
```
Formula: 100 meters = 1 minute round trip

Calculated distance: 650 meters (0.65 km)

ESTIMATED HIVE LOCATION:
  Coordinates: 48.862533°N, 2.300783°E
  Bearing from you: NE (45.0°)
  Confidence: ±120 meters

GPS COORDINATES:
  48.862533, 2.300783
```

### Optional: Method Comparison
If speed is entered, shows comparison between:
- Empirical method (Vespawatchers standard)
- Theoretical method (speed × time ÷ 2)
- Difference between methods

---

## 💡 Professional Tips (Built-in)

### Equipment Checklist
✓ Binoculars (8×42) - MOST IMPORTANT  
✓ Wick pot with sugar bait  
✓ Color markers (white recommended)  
✓ Butterfly net  
✓ Compass  
✓ Stopwatch  

### Search Strategy
✓ Don't just look in trees!  
✓ Check ground, sheds, roofs, hedges  
✓ Scan with binoculars  
✓ Walk in circles around area  

### Safety Warnings
✓ Never approach nest alone  
✓ Use protective equipment  
✓ Contact professional pest control  
✓ Report to vespawatch.be / waarneming.nl  

---

## 🎯 Example Workflow

### Scenario: Observing at Your Beehive

1. **Setup**
   - You're at your beehive
   - GPS: 48.8584°N, 2.2945°E
   - You see hornet flying Northeast

2. **Mark Hornet**
   - Dust with flour
   - Note departure time
   - Watch with compass: 45°

3. **Time the Return**
   - Start stopwatch when it leaves
   - Stop when same hornet returns
   - Result: 6 minutes 30 seconds

4. **Enter in GUI**
   ```
   Latitude: 48.8584
   Longitude: 2.2945
   Bearing: 45
   Minutes: 6
   Seconds: 30
   ```

5. **Calculate**
   - Click "CALCULATE HIVE LOCATION"
   - Read results: ~650m Northeast
   - View map for search zone

6. **Navigate**
   - Use GPS coordinates
   - Or click Google Maps link
   - Search within red circle on map

---

## 🔍 Interpreting the Map

### Red Circle (Search Zone)
The confidence circle shows where to search:
- **Center**: Most likely location
- **Radius**: Uncertainty range (±50-300m typically)
- **Search within this area**

Note from professionals:
> "In practice, nest is often slightly further than calculated"

### Search Strategy
1. Navigate to circle center
2. Scan area with binoculars
3. Look for flying hornets (small black dots)
4. Check trees, sheds, ground, hedges
5. Walk in circles, scanning repeatedly

---

## 📱 Mobile Use

### Tips for Field Use
- Run on laptop/tablet brought to field
- Pre-install on device
- Works offline (no internet needed for calculations)
- Map generation needs internet briefly
- Save reports for offline reference

### Recommended Setup
1. Laptop/tablet with large screen
2. External mouse (easier than trackpad)
3. Power bank for extended sessions
4. Shade/canopy for screen visibility

---

## 🎨 Color Coding

- **Blue**: Your observation points
- **Red**: Estimated hive locations
- **Green**: Success/confirmation messages
- **Orange**: Warnings/important notes
- **Gray**: General information

---

## 🐛 Troubleshooting

### Map Won't Open
- Check that calculation was run first
- Ensure default browser is set
- Look in /tmp directory for HTML file

### Invalid Input Error
- Check GPS coordinates format (decimal degrees)
- Verify bearing is 0-360
- Ensure time is positive number

### Map Shows Wrong Location
- Double-check GPS coordinates
- Verify latitude/longitude order
- Check bearing direction (compass)

---

## 📖 Quick Reference

| Field | Valid Range | Example |
|-------|-------------|---------|
| Latitude | -90 to 90 | 48.8584 |
| Longitude | -180 to 180 | 2.2945 |
| Bearing | 0 to 360 | 45 |
| Time | > 0 | 6min 30sec |
| Speed | > 0 (optional) | 7 |

### Compass Directions
- N = 0° or 360°
- NE = 45°
- E = 90°
- SE = 135°
- S = 180°
- SW = 225°
- W = 270°
- NW = 315°

---

## 🎓 Educational Display

The GUI includes educational content:
- Professional methodology explanation
- Equipment importance rankings
- Search strategy tips
- Safety protocols
- Real-world case studies

Perfect for:
- Training new trackers
- Demonstrating to beekeepers
- Educational presentations
- Field workshops

---

## 💾 File Output

### Generated Files

1. **Interactive Map** (temp directory)
   - `hornet_map_YYYYMMDD_HHMMSS.html`
   - Opens in browser
   - Can be saved permanently

2. **Text Report** (current directory)
   - `hornet_report_YYYYMMDD_HHMMSS.txt`
   - Full calculation details
   - Ready to share/print

---

## 🆚 GUI vs CLI

### Use GUI When:
- ✅ Training others
- ✅ Visual presentation needed
- ✅ Map visualization important
- ✅ Prefer forms over typing
- ✅ Multiple observations planned

### Use CLI When:
- ✅ Quick single calculation
- ✅ Remote SSH session
- ✅ Scripting/automation
- ✅ Minimal interface preferred

Both use same professional methodology!

---

## 🚀 Advanced Features (Future)

Planned enhancements:
- [ ] Multiple observation tracking
- [ ] Session history
- [ ] Embedded map view (no browser)
- [ ] Photo upload capability
- [ ] GPS auto-detect from device
- [ ] Offline map tiles
- [ ] Export to KML/GPX

---

## ⌨️ Keyboard Shortcuts

- **Enter**: Calculate (when in form field)
- **Ctrl+S**: Save report
- **Ctrl+M**: View map
- **Ctrl+L**: Clear form
- **Ctrl+Q**: Quit application

---

## 🎯 Success Indicators

You know it's working when:
1. ✅ Results panel updates with calculations
2. ✅ Success message appears
3. ✅ "View Map" button opens browser
4. ✅ Map shows blue and red markers
5. ✅ Red circle visualizes search area

---

## 📞 Support

For issues:
- Check input values are valid
- Read error messages carefully
- Verify internet for map generation
- See UPDATES.md for methodology
- Review SPECIFICATION_UPDATED.md

---

**The GUI makes professional hornet tracking accessible to everyone!** 🐝
