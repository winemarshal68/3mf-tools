# 3MF Tools - 3D Mesh Processing & Slicing Automation

> **Complete automation toolchain for 3D mesh processing, 3MF manipulation, and slicing operations exposed via MCP (Model Context Protocol)**

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 What is This?

This toolchain provides a complete set of tools for programmatically working with 3D models, meshes, and 3MF files. All operations are exposed through an MCP (Model Context Protocol) server, making them accessible to AI assistants, automation scripts, and workflows.

**Key Capabilities:**
- ✅ Mesh repair and validation (using MeshFix)
- ✅ Boolean operations (union, difference, intersection)
- ✅ Mesh transformations (scale, rotate, translate)
- ✅ Format conversion (STL, OBJ, PLY, 3MF, etc.)
- ✅ 3MF file manipulation (unpack, modify, repack)
- ⚙️ Slicing integration (CuraEngine, Bambu Lab)
- 🤖 MCP server for AI/automation workflows

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd 3mf_tools
./install.sh  # See installation section below
```

### 2. Activate Environment

```bash
source activate.sh
```

### 3. Test Installation

```bash
python self_test.py
```

### 4. Start MCP Server

```bash
python mcp_server/server.py
```

## 📦 What's Installed

### Core Tools

| Tool | Status | Description |
|------|--------|-------------|
| **MeshFix** | ✅ Built | Industry-standard mesh repair tool |
| **lib3mf** | ✅ Built | Official 3MF Consortium library |
| **3MFresh** | ✅ Ready | 3MF processing scripts |
| **Python Environment** | ✅ Ready | Virtual environment with all dependencies |
| **MCP Server** | ✅ Ready | Tool server for automation |

### Python Packages

- **trimesh** - Mesh loading, processing, and export
- **numpy** - Numerical operations
- **scipy** - Scientific computing
- **meshio** - Multi-format mesh I/O
- **networkx** - Mesh topology operations
- **lxml** - XML/3MF parsing

### Optional Components

- **CuraEngine** - Requires additional setup (see [docs/curaengine.md](docs/curaengine.md))
- **Bambu Lab CLI** - Placeholder for custom integration
- **pymeshlab** - Not compatible with Python 3.13+ (optional)

## 📖 Usage

### Command Line Tools

#### Repair a Mesh
```bash
# Activate environment first
source activate.sh

# Repair mesh (outputs .off format)
meshfix input.stl

# Convert to STL
python -c "import trimesh; trimesh.load('input_fixed.off').export('output.stl')"
```

#### Convert Formats
```bash
python -c "import trimesh; trimesh.load('model.stl').export('model.3mf')"
```

### Python Scripting

```python
#!/Users/marshalwalkerm4mini/3d-workflows/3mf_tools/venv/bin/python
import trimesh

# Load and process mesh
mesh = trimesh.load('input.stl')
mesh.fix_normals()
mesh.apply_scale(2.0)

# Export to 3MF
mesh.export('output.3mf')
```

### MCP Server API

The MCP server accepts JSON requests via stdin:

```json
{"tool": "mesh.load", "arguments": {"path": "/path/to/model.stl"}}
{"tool": "mesh.repair", "arguments": {"input_path": "model.stl", "output_path": "fixed.stl"}}
{"tool": "threeMF.unpack", "arguments": {"three_mf_path": "model.3mf", "output_dir": "unpacked"}}
```

**Response format:**
```json
{"status": "success", "path": "/path/to/output.stl", "vertices": 1234, "faces": 2468}
```

## 🛠️ MCP Tools Reference

### Mesh Operations

#### `mesh.load(path)`
Load mesh and return statistics.

**Example:**
```json
{"tool": "mesh.load", "arguments": {"path": "model.stl"}}
```

**Response:**
```json
{"status": "success", "vertices": 8, "faces": 12}
```

---

#### `mesh.repair(input_path, output_path)`
Repair mesh using MeshFix.

**Example:**
```json
{"tool": "mesh.repair", "arguments": {"input_path": "broken.stl", "output_path": "fixed.stl"}}
```

---

#### `mesh.boolean(operation, mesh_a_path, mesh_b_path, output_path)`
Perform boolean operations.

**Operations:** `union`, `difference`, `intersection`

**Example:**
```json
{
  "tool": "mesh.boolean",
  "arguments": {
    "operation": "union",
    "mesh_a_path": "part1.stl",
    "mesh_b_path": "part2.stl",
    "output_path": "combined.stl"
  }
}
```

---

#### `mesh.transform(mesh_path, output_path, scale, rotate, translate)`
Transform mesh with scale, rotation, or translation.

**Example:**
```json
{
  "tool": "mesh.transform",
  "arguments": {
    "mesh_path": "input.stl",
    "output_path": "scaled.stl",
    "scale": 2.0
  }
}
```

---

### 3MF Operations

#### `threeMF.unpack(three_mf_path, output_dir)`
Extract 3MF contents to directory.

**Example:**
```json
{"tool": "threeMF.unpack", "arguments": {"three_mf_path": "model.3mf", "output_dir": "extracted"}}
```

---

#### `threeMF.repack(unpacked_dir, output_file)`
Create 3MF from directory.

**Example:**
```json
{"tool": "threeMF.repack", "arguments": {"unpacked_dir": "modified", "output_file": "new.3mf"}}
```

---

### Slicer Operations

#### `slicer.slice_with_cura(model_path, profile_path, output_gcode)`
Slice model using CuraEngine (requires setup).

**Example:**
```json
{
  "tool": "slicer.slice_with_cura",
  "arguments": {
    "model_path": "model.stl",
    "profile_path": "profile.json",
    "output_gcode": "output.gcode"
  }
}
```

## 📂 Directory Structure

```
3mf_tools/
├── bin/                    # Compiled executables
│   ├── meshfix            # MeshFix binary (built during install)
│   └── curaengine         # CuraEngine (requires setup)
├── mesh_tools/            # Mesh processing utilities
├── threeMF_tools/         # 3MF manipulation tools
├── slicer_tools/          # Slicing integration
│   └── bambu_cli.py       # Bambu Lab wrapper (placeholder)
├── mcp_server/            # MCP server implementation
│   └── server.py          # Main server
├── docs/                  # Documentation
│   ├── installation.md    # Detailed install guide
│   ├── examples.md        # Usage examples
│   └── api.md             # Full API reference
├── examples/              # Example scripts
│   ├── repair_mesh.py
│   ├── convert_formats.py
│   └── boolean_ops.py
├── venv/                  # Python virtual environment
├── activate.sh            # Environment activation script
├── install.sh             # Installation script
├── self_test.py           # Test suite
└── README.md              # This file
```

## 🔧 Installation

### Prerequisites

- macOS (tested on macOS Sequoia)
- Homebrew
- Python 3.13
- Git
- CMake (installed during setup)

### Automated Installation

```bash
./install.sh
```

This will:
1. Create Python virtual environment
2. Install Python dependencies
3. Clone and build MeshFix
4. Clone and build lib3mf
5. Clone 3MFresh
6. Set up MCP server
7. Run self-tests

### Manual Installation

See [docs/installation.md](docs/installation.md) for detailed manual setup instructions.

## 🧪 Testing

Run the comprehensive test suite:

```bash
python self_test.py
```

**Expected output:**
```
============================================================
Test Summary
============================================================
Python packages:  PASS
Mesh tools:       PASS
3MF libraries:    PASS
Slicer backends:  PASS
MCP server:       PASS
Workflow test:    PASS
============================================================
```

## 📚 Documentation

- [Installation Guide](docs/installation.md) - Detailed setup instructions
- [Usage Examples](docs/examples.md) - Common workflows and recipes
- [API Reference](docs/api.md) - Complete MCP tool documentation
- [CuraEngine Setup](docs/curaengine.md) - Configure slicing backend
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Complete CuraEngine integration
- [ ] Bambu Lab Cloud API integration
- [ ] Additional mesh repair algorithms
- [ ] Support for more 3D formats
- [ ] PyMeshLab integration (Python 3.12 compat)
- [ ] Docker container for easy deployment

## 📋 Design Principles

All MCP tools follow these principles:

1. **File-based operations** - All I/O through files, no large data in responses
2. **Status messages only** - Return paths and status codes, not mesh data
3. **Silent by default** - Only output on errors
4. **Idempotent** - Safe to run multiple times
5. **Low token usage** - Optimized for AI assistant workflows

## 🐛 Troubleshooting

**Import errors:**
```bash
# Ensure you're using the venv Python
which python
# Should show: /path/to/3mf_tools/venv/bin/python
```

**MeshFix outputs .off instead of .stl:**
```python
import trimesh
trimesh.load('file.off').export('file.stl')
```

**CuraEngine not found:**
- Use the stub for now, or see [docs/curaengine.md](docs/curaengine.md) for build instructions
- Alternative: Use OrcaSlicer or PrusaSlicer CLI

## 📄 License

This project integrates several components with different licenses:

- **This repository:** MIT License
- **MeshFix:** GPL
- **lib3mf:** BSD 2-Clause
- **CuraEngine:** AGPL
- **Python packages:** Various (see individual packages)

## 🙏 Acknowledgments

- [MeshFix](https://github.com/MarcoAttene/MeshFix-V2.1) by Marco Attene
- [lib3mf](https://github.com/3MFConsortium/lib3mf) by 3MF Consortium
- [3MFresh](https://github.com/brossow/3MFresh) by brossow
- [CuraEngine](https://github.com/Ultimaker/CuraEngine) by Ultimaker
- [trimesh](https://github.com/mikedh/trimesh) by Michael Dawson-Haggerty

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/3mf_tools/issues)
- **Documentation:** See [docs/](docs/)
- **Self-test:** Run `python self_test.py` for diagnostics

---

**Status:** Production-ready for mesh processing and 3MF operations. Slicing requires additional configuration.
