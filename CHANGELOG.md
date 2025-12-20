# Changelog

All notable changes to VespaFinder (formerly Hornet Nest Locator) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-12-19

### Changed
- **Project renamed to VespaFinder** (from Hornet Nest Locator)
- Package renamed from `hornet_hive_locator` to `vespa_finder`
- Updated all imports and references

### Added
- **68 unit tests** covering geo_utils, models, and calculator
- **Multi-observation support** in SimpleMapGenerator
- **Error handling** for map file generation
- Bilingual support highlighted in README

### Improved
- SimpleMapGenerator now displays all observations (not just the first)
- Map generators create output directories automatically
- Better error messages for file operations

### Fixed
- Inline import moved to top of calculator.py
- Broken documentation links fixed

## [0.2.0] - 2025-12-04

### Added
- **Empirical method** as primary calculation method (100m/min formula from Vespawatchers)
- Comprehensive methodology explanation in README
- Scientific research documentation (`HORNET_SPEED_RESEARCH.md`)
- French translation of README (`README_FR.md`)
- Detailed comparison between empirical and theoretical methods
- Field usage tips and safety guidelines
- Professional Vespawatchers methodology integration
- `CONTRIBUTING.md` for open-source collaboration
- MIT License
- GitHub badges and enhanced documentation
- Speed verification research (6-8 m/s validated)

### Changed
- Default calculation method switched to empirical (from theoretical)
- Speed parameter made optional (only for comparison)
- Enhanced CLI interface with professional methodology
- Improved confidence radius calculations
- Updated all documentation with research sources

### Improved
- More accurate distance calculations (empirical method)
- Better field usability (no speed measurement needed)
- Clearer safety warnings and recommendations
- Enhanced map visualization details

### Documentation
- Added detailed "How It Works" section
- Included step-by-step field process
- Added comparison examples
- Scientific references and sources
- FAQ section in French README

## [0.1.0] - 2025-12-03

### Added
- Initial release
- Basic hornet tracking functionality
- Single observation calculation
- Multiple observation triangulation
- Interactive CLI interface
- Map visualization with Folium
- Geographic calculations (haversine formula)
- Confidence radius estimation
- HTML map generation
- Text report export
- Python API for programmatic use
- Example scripts
- Comprehensive documentation

### Features
- GPS-based tracking
- Compass bearing input
- Round trip time measurement
- Speed-based distance calculation (theoretical)
- Interactive map visualization
- Google Maps integration
- Multiple observation support
- Confidence interval calculation

---

## Version Guidelines

### Version Format: MAJOR.MINOR.PATCH

- **MAJOR**: Incompatible API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Change Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerabilities

---

**Note**: Dates are in YYYY-MM-DD format
