#!/bin/bash
# Complete Design → Print Workflow
# Integrates with your CAD-MASTER system and MCP tools

set -e

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Complete 3D Printing Workflow${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Configuration
CAD_DIR="$HOME/3d-design-projects/cad"
STL_DIR="$HOME/3d-design-projects/stl"
SLICES_DIR="$HOME/3d-design-projects/slices"
TOOLS_DIR="$HOME/3d-workflows/3mf_tools"

# Check if file provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <stl_file> [output_name]"
    echo ""
    echo "Examples:"
    echo "  $0 ~/3d-design-projects/stl/part_v1.stl"
    echo "  $0 design.stl custom_name"
    echo ""
    echo "This script will:"
    echo "  1. Repair the mesh with MeshFix"
    echo "  2. Convert to 3MF format"
    echo "  3. Save to slices directory"
    echo "  4. Report file location for printing"
    exit 1
fi

INPUT_FILE="$1"
BASENAME=$(basename "$INPUT_FILE" .stl)

if [ $# -eq 2 ]; then
    OUTPUT_NAME="$2"
else
    OUTPUT_NAME="$BASENAME"
fi

OUTPUT_FILE="$SLICES_DIR/${OUTPUT_NAME}.3mf"

# Validate input
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${YELLOW}Error: Input file not found: $INPUT_FILE${NC}"
    exit 1
fi

# Create output directory
mkdir -p "$SLICES_DIR"

echo -e "${GREEN}Step 1/3: Repairing mesh with MeshFix...${NC}"
cd "$TOOLS_DIR"
source venv/bin/activate

TEMP_REPAIRED="/tmp/${BASENAME}_repaired.stl"
./examples/repair_mesh.py "$INPUT_FILE" "$TEMP_REPAIRED"

if [ ! -f "$TEMP_REPAIRED" ]; then
    echo -e "${YELLOW}Warning: Repair may have failed, using original${NC}"
    TEMP_REPAIRED="$INPUT_FILE"
fi

echo ""
echo -e "${GREEN}Step 2/3: Converting to 3MF format...${NC}"
python -c "import trimesh; trimesh.load('$TEMP_REPAIRED').export('$OUTPUT_FILE')"

# Clean up temp file if we created one
if [ "$TEMP_REPAIRED" != "$INPUT_FILE" ]; then
    rm -f "$TEMP_REPAIRED"
fi

echo ""
echo -e "${GREEN}Step 3/3: Validating output...${NC}"
python -c "import trimesh; m = trimesh.load('$OUTPUT_FILE'); print(f'Vertices: {len(m.vertices)}, Faces: {len(m.faces)}, Watertight: {m.is_watertight}')"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Workflow Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Output file: ${GREEN}$OUTPUT_FILE${NC}"
echo ""
echo "Next steps:"
echo "  1. Send to Bambu Lab printer via MCP"
echo "  2. Or slice with: CuraEngine/Bambu Studio"
echo ""
echo "File location in CAD-MASTER system:"
echo "  ${SLICES_DIR}/${OUTPUT_NAME}.3mf"
