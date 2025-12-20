# 🏗️ Build Process Documentation

This document describes the build and deployment process for the Hornet Nest Locator application.

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       ├── ci.yml                  # Continuous Integration (tests, linting, type checking)
│       └── build_windows.yml        # Windows build & packaging workflow
├── assets/
│   ├── icon.ico                    # Application icon
│   └── README.md                   # Assets documentation
├── src/
│   └── vespa_finder/               # Core application modules
├── tests/                          # Unit tests
├── docs/                           # Documentation
├── requirements.txt                # Python dependencies
└── gui.py                           # Main GUI entry point
```

## 🚀 GitHub Actions Workflows

### 1. Continuous Integration (CI)

**File**: `.github/workflows/ci.yml`

**Purpose**: Run tests, linting, and type checking on every push and pull request.

**Features**:
- ✅ Cross-platform testing (Ubuntu, macOS, Windows)
- ✅ Python 3.12 compatibility testing
- ✅ Code formatting checks with Ruff
- ✅ Linting with Ruff
- ✅ Type checking with mypy
- ✅ Test coverage reporting to Codecov

**Triggers**:
- Pushes to `main`, `master`, `develop` branches
- Pull requests to `main`, `master` branches

### 2. Windows Build & Package

**File**: `.github/workflows/build_windows.yml`

**Purpose**: Create standalone Windows executables and portable packages.

**Features**:
- ✅ **Automatic Builds**: Triggered on pushes, tags, and manually
- ✅ **Testing**: Runs all unit tests before building
- ✅ **Single Executable**: Creates a standalone `.exe` file
- ✅ **Portable Package**: Creates a ZIP with executable + documentation
- ✅ **Version Management**: Automatic version detection from git tags
- ✅ **Icon Support**: Embeds application icon in the executable
- ✅ **Artifact Upload**: Uploads build artifacts for download
- ✅ **GitHub Releases**: Automatically creates releases for tagged versions

**Triggers**:
- Pushes to `main`, `dev` branches
- Git tags matching `v*.*.*` pattern
- Manual triggers via GitHub UI
- Pull requests to `main`, `dev` branches

## 📦 Build Process

### 1. Unit Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=src/vespa_finder --cov-report=xml
```

### 2. Windows Executable Build

The build process uses **PyInstaller** to create a standalone Windows executable:

```bash
# Install PyInstaller
pip install pyinstaller==6.7.0

# Build executable
pyinstaller --clean --onefile --windowed \
  --name hornet-nest-locator \
  --icon=assets/icon.ico \
  --add-data "src/vespa_finder:vespa_finder" \
  --add-data "assets/*:assets" \
  --version-file=version.txt \
  --distpath=dist \
  --workpath=build \
  gui.py
```

### 3. Portable Package Creation

```bash
# Create portable directory structure
mkdir -p dist/portable
cp dist/hornet-nest-locator.exe dist/portable/
cp -r assets/ dist/portable/
cp docs/GUI_GUIDE.md dist/portable/
cp README.md dist/portable/

# Create launch script
echo "@echo off" > dist/portable/launch.bat
echo "start \"\" \"hornet-nest-locator.exe\"" >> dist/portable/launch.bat

# Create ZIP archive
# Windows: Compress-Archive -Path "dist/portable/*" -DestinationPath "dist/hornet-nest-locator-portable-windows.zip"
# Linux/macOS: zip -r dist/hornet-nest-locator-portable-windows.zip dist/portable/
```

## 📦 Output Files

### Windows Executable
- **File**: `hornet-nest-locator.exe`
- **Location**: `dist/`
- **Type**: Standalone executable
- **Size**: ~10-20 MB (depending on dependencies)
- **Features**:
  - No Python installation required
  - Includes all dependencies
  - Embedded application icon
  - Windowed GUI application

### Portable Package
- **File**: `hornet-nest-locator-portable-windows.zip`
- **Location**: `dist/`
- **Contents**:
  - `hornet-nest-locator.exe` (main executable)
  - `launch.bat` (convenience launch script)
  - `assets/` (application assets)
  - `GUI_GUIDE.md` (user guide)
  - `README.md` (project documentation)
- **Usage**: Extract and run `launch.bat` or `hornet-nest-locator.exe`

## 🔧 Requirements

### Build Dependencies

```bash
# Install build tools
pip install pyinstaller==6.7.0

# Install runtime dependencies
pip install -r requirements.txt
```

### Runtime Dependencies

See `requirements.txt` for the complete list of Python dependencies.

## 🎯 Version Management

The build system automatically detects version from:

1. **Git Tags**: If building from a tag like `v1.2.3`, uses `1.2.3`
2. **Branch Name**: For development builds, uses `0.0.0-dev`
3. **Manual Override**: Can be specified in `version.txt`

## 🚀 Deployment

### GitHub Releases

When building from git tags (e.g., `v1.2.3`), the workflow automatically:
1. Creates a GitHub Release
2. Uploads the Windows executable
3. Uploads the portable package
4. Generates release notes

### Manual Deployment

To manually trigger a build:
1. Go to GitHub Actions
2. Select "Windows Build & Package" workflow
3. Click "Run workflow"
4. Select branch and options
5. Click "Run workflow"

## 🧪 Quality Assurance

The build process includes comprehensive quality checks:

### Pre-build Checks
- ✅ Unit tests (68+ tests)
- ✅ Code formatting verification
- ✅ Linting checks
- ✅ Type checking

### Post-build Verification
- ✅ Executable existence check
- ✅ PE file validation (MZ signature)
- ✅ Portable package content verification
- ✅ File size reporting

## 📝 Build Artifacts

Build artifacts are available for 7 days and include:

1. **Windows Executable**: `hornet-nest-locator.exe`
2. **Portable Package**: `hornet-nest-locator-portable-windows.zip`

## 🔄 Continuous Deployment

The system supports continuous deployment:

- **Development Builds**: Triggered on pushes to `dev` branch
- **Production Builds**: Triggered on pushes to `main` branch
- **Release Builds**: Triggered on git tags

## 🛠️ Customization

### Custom Icon

To customize the application icon:
1. Replace `assets/icon.ico` with your own ICO file
2. Ensure it's a valid Windows ICO format
3. Recommended sizes: 16x16, 32x32, 48x48, 256x256

### Custom Version Info

Create a `version.txt` file with custom version information:

```ini
[version]
version=1.2.3
company=Your Organization
product=Hornet Nest Locator
name=hornet-nest-locator
```

## ⚠️ Troubleshooting

### Common Issues

**Issue**: Build fails with missing dependencies
**Solution**: Ensure all dependencies are listed in `requirements.txt`

**Issue**: Executable doesn't run on target machine
**Solution**: Build on the oldest supported Windows version

**Issue**: Large executable size
**Solution**: Use `--exclude-module` to exclude unnecessary modules

**Issue**: Missing assets in final executable
**Solution**: Verify `--add-data` paths in PyInstaller command

### Debugging

```bash
# Run with console (for debugging)
pyinstaller --onefile --console gui.py

# Check imported modules
pyinstaller --onefile --debug=imports gui.py

# Analyze dependencies
pyinstaller --onefile --debug=all gui.py
```

## 📚 Resources

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Windows ICO Format Specification](https://learn.microsoft.com/en-us/windows/win32/uxguide/vis-icons)

## 🤝 Contributing

To contribute to the build process:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📅 Release Process

1. **Development**: Push changes to `dev` branch
2. **Testing**: Verify builds pass on `dev`
3. **Staging**: Merge to `main` for final testing
4. **Release**: Create git tag `vX.Y.Z`
5. **Deployment**: GitHub Actions creates release automatically

---

> "Automated builds ensure consistent, reliable deployments for conservation tools."

The build system is designed to be robust, automated, and maintainable, ensuring that conservation workers always have access to the latest tools for protecting bee populations.