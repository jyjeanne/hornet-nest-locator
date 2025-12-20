#!/bin/bash
#
# VespaFinder - Build Standalone Executable
#
# This script builds a standalone executable using PyInstaller.
# The resulting executable can run without Python installed.
#
# Usage:
#   ./build_exe.sh          # Build GUI executable
#   ./build_exe.sh --cli    # Build CLI executable
#   ./build_exe.sh --clean  # Clean build artifacts
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║       VespaFinder - Build Executable                         ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Parse arguments
BUILD_CLI=false
CLEAN_ONLY=false

for arg in "$@"; do
    case $arg in
        --cli)
            BUILD_CLI=true
            ;;
        --clean)
            CLEAN_ONLY=true
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --cli     Build CLI version instead of GUI"
            echo "  --clean   Clean build artifacts only"
            echo "  --help    Show this help message"
            exit 0
            ;;
    esac
done

# Clean function
clean_build() {
    echo -e "${YELLOW}Cleaning build artifacts...${NC}"
    rm -rf build/ dist/ *.spec.bak __pycache__/
    rm -rf src/vespa_finder/__pycache__/
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -delete
    echo -e "${GREEN}✓ Clean complete${NC}"
}

if [ "$CLEAN_ONLY" = true ]; then
    clean_build
    exit 0
fi

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv is not installed${NC}"
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install dev dependencies (includes PyInstaller)
echo -e "${YELLOW}Installing dependencies...${NC}"
uv sync --dev

# Clean previous builds
clean_build

# Build executable
echo ""
if [ "$BUILD_CLI" = true ]; then
    echo -e "${YELLOW}Building CLI executable...${NC}"
    uv run pyinstaller \
        --name VespaFinder-CLI \
        --onefile \
        --console \
        --paths src \
        --hidden-import vespa_finder \
        --hidden-import vespa_finder.models \
        --hidden-import vespa_finder.calculator \
        --hidden-import vespa_finder.geo_utils \
        main.py
else
    echo -e "${YELLOW}Building GUI executable...${NC}"
    uv run pyinstaller vespa_finder.spec
fi

# Check if build succeeded
if [ -d "dist" ]; then
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║       Build Complete!                                        ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}Executable location:${NC}"
    ls -lh dist/
    echo ""

    # Platform-specific instructions
    case "$(uname -s)" in
        Linux*)
            echo -e "${YELLOW}To run:${NC}"
            echo "  ./dist/VespaFinder"
            ;;
        Darwin*)
            echo -e "${YELLOW}To run:${NC}"
            echo "  open dist/VespaFinder.app"
            echo "  # or: ./dist/VespaFinder"
            ;;
        MINGW*|CYGWIN*|MSYS*)
            echo -e "${YELLOW}To run:${NC}"
            echo "  dist\\VespaFinder.exe"
            ;;
    esac
    echo ""
    echo -e "${GREEN}You can distribute the executable - no Python installation required!${NC}"
else
    echo -e "${RED}Build failed! Check the output above for errors.${NC}"
    exit 1
fi
