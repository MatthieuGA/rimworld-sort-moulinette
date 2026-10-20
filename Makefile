# Makefile for RimWorld Modlist Manager
# Run: make

PYTHON = python
HATCH = $(PYTHON) -m hatch

.PHONY: all clean install build verify help

# Default target
all: build

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	$(PYTHON) -m pip install --upgrade hatch
	$(HATCH) env create
	@echo "✅ Dependencies installed"

# Build the executable
build:
	@echo "🔨 Building executable with Hatch..."
	@echo "Using: $(HATCH)"
	@$(PYTHON) --version
	@echo ""
	rm -rf build dist
	$(HATCH) run build-exe
	@echo ""
	@echo "✅ Build complete: dist/gui.exe or dist/gui"
	@ls -lh dist

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build dist __pycache__ *.pyc
	@echo "✅ Clean complete"

# Verify the executable works
verify:
	@echo "🔍 Verifying executable..."
	@echo "Checking for dearpygui..."
	@strings dist/gui | grep -q "dearpygui.dearpygui" && echo "  ✅ dearpygui bundled" || echo "  ❌ dearpygui NOT found"
	@echo "Checking for requests..."
	@strings dist/gui | grep -q "requests" && echo "  ✅ requests bundled" || echo "  ❌ requests NOT found"
	@echo "Checking for beautifulsoup4..."
	@strings dist/gui | grep -q "bs4" && echo "  ✅ beautifulsoup4 bundled" || echo "  ❌ bs4 NOT found"
	@echo ""
	@echo "Quick launch test (3 second timeout)..."
	@timeout 3 ./dist/gui 2>&1 || echo "  ✅ Executable launches"

# Help
help:
	@echo "RimWorld Modlist Manager - Build Commands"
	@echo "=========================================="
	@echo ""
	@echo "make          - Build the executable (default)"
	@echo "make install  - Install Python dependencies"
	@echo "make build    - Build the executable"
	@echo "make verify   - Verify the executable works"
	@echo "make clean    - Remove build artifacts"
	@echo "make help     - Show this help"
	@echo ""
	@echo "Output: dist/ (platform executable)"
