#!/bin/bash
set -e

# 3MF Tools Installation Script
# Automated setup for macOS

echo "=========================================="
echo "3MF Tools Installation"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_section() {
    echo ""
    echo "=========================================="
    echo "$1"
    echo "=========================================="
}

# Check prerequisites
print_section "Checking Prerequisites"

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    print_error "Homebrew not found"
    echo "Install Homebrew from https://brew.sh"
    exit 1
fi
print_status "Homebrew installed"

# Check for Git
if ! command -v git &> /dev/null; then
    print_error "Git not found"
    exit 1
fi
print_status "Git installed"

# Install/update CMake
print_section "Installing System Dependencies"
if ! command -v cmake &> /dev/null; then
    echo "Installing CMake..."
    brew install cmake
    print_status "CMake installed"
else
    print_status "CMake already installed"
fi

# Check/install Python 3.13
if ! command -v python3.13 &> /dev/null; then
    echo "Installing Python 3.13..."
    brew install python@3.13
    print_status "Python 3.13 installed"
else
    print_status "Python 3.13 already installed"
fi

# Create Python virtual environment
print_section "Setting Up Python Environment"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.13 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment and install packages
echo "Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip --quiet
pip install trimesh numpy scipy meshio networkx lxml --quiet
print_status "Python packages installed"

# Build MeshFix
print_section "Building MeshFix"
if [ ! -f "bin/meshfix" ]; then
    if [ ! -d "meshfix_source" ]; then
        echo "Cloning MeshFix..."
        git clone https://github.com/MarcoAttene/MeshFix-V2.1.git meshfix_source --quiet
    fi

    echo "Building MeshFix (this may take a minute)..."
    cd meshfix_source
    mkdir -p build
    cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5 > /dev/null 2>&1
    make -j4 > /dev/null 2>&1
    cd ../..

    mkdir -p bin
    cp meshfix_source/bin64/MeshFix bin/meshfix
    chmod +x bin/meshfix
    print_status "MeshFix built successfully"
else
    print_status "MeshFix already built"
fi

# Build lib3mf
print_section "Building lib3mf"
if [ ! -d "lib3mf/build" ]; then
    if [ ! -d "lib3mf" ]; then
        echo "Cloning lib3mf..."
        git clone https://github.com/3MFConsortium/lib3mf.git --quiet
        cd lib3mf
        git submodule update --init --recursive --quiet
        cd ..
    fi

    echo "Building lib3mf (this may take a few minutes)..."
    cd lib3mf
    mkdir -p build
    cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release -DLIB3MF_TESTS=OFF > /dev/null 2>&1
    make -j4 > /dev/null 2>&1
    cd ../..
    print_status "lib3mf built successfully"
else
    print_status "lib3mf already built"
fi

# Clone 3MFresh
print_section "Setting Up 3MF Tools"
if [ ! -d "3MFresh" ]; then
    echo "Cloning 3MFresh..."
    git clone https://github.com/brossow/3MFresh.git --quiet
    print_status "3MFresh cloned"
else
    print_status "3MFresh already present"
fi

# Create stub for CuraEngine
if [ ! -f "bin/curaengine" ]; then
    cat > bin/curaengine << 'CURA_EOF'
#!/bin/bash
echo "CuraEngine not yet built - requires Ultimaker Conan repository configuration" >&2
echo "Alternative: Use OrcaSlicer or PrusaSlicer CLI for slicing operations" >&2
exit 1
CURA_EOF
    chmod +x bin/curaengine
    print_status "CuraEngine stub created"
fi

# Make scripts executable
print_section "Configuring Scripts"
chmod +x activate.sh self_test.py mcp_server/server.py examples/*.py
print_status "Scripts configured"

# Run self-test
print_section "Running Self-Test"
./self_test.py

# Print completion message
print_section "Installation Complete!"
echo ""
echo "To activate the environment:"
echo "  ${GREEN}source activate.sh${NC}"
echo ""
echo "To test the installation:"
echo "  ${GREEN}python self_test.py${NC}"
echo ""
echo "To start the MCP server:"
echo "  ${GREEN}python mcp_server/server.py${NC}"
echo ""
echo "To run examples:"
echo "  ${GREEN}./examples/repair_mesh.py --help${NC}"
echo "  ${GREEN}./examples/convert_formats.py --help${NC}"
echo "  ${GREEN}./examples/boolean_ops.py --example${NC}"
echo ""
echo "Documentation:"
echo "  README.md  - Complete documentation"
echo "  INSTALL.md - Installation guide"
echo ""
print_status "Ready to use!"
