# Installation Guide

## Quick Install (macOS)

```bash
# Clone repository
git clone https://github.com/winemarshal68/3mf-tools.git
cd 3mf-tools

# Run automated installation
./install.sh
```

## Prerequisites

- **macOS** (tested on macOS Sequoia 15.1)
- **Homebrew** - [Install here](https://brew.sh)
- **Git**
- **Python 3.13+**
- **CMake** (installed during setup if missing)

## Manual Installation

### 1. Create Python Virtual Environment

```bash
python3.13 -m venv venv
source venv/bin/activate
```

### 2. Install Python Dependencies

```bash
pip install trimesh numpy scipy meshio networkx lxml
```

### 3. Build MeshFix

```bash
git clone https://github.com/MarcoAttene/MeshFix-V2.1.git meshfix_source
cd meshfix_source
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5
make -j4
cp ../bin64/MeshFix ../../bin/meshfix
cd ../..
```

### 4. Build lib3mf

```bash
git clone https://github.com/3MFConsortium/lib3mf.git
cd lib3mf
git submodule update --init --recursive
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DLIB3MF_TESTS=OFF
make -j4
cd ../..
```

### 5. Clone 3MFresh

```bash
git clone https://github.com/brossow/3MFresh.git
```

### 6. Test Installation

```bash
python self_test.py
```

## Platform-Specific Notes

### macOS

The installation script uses Homebrew for system dependencies:
- CMake for building C++ components
- Python 3.13 (via Homebrew)

### Linux (Experimental)

Should work with minimal changes:
1. Replace `brew install` with `apt-get install` or equivalent
2. Adjust library paths in activation script

### Windows (Not Tested)

Consider using WSL2 (Windows Subsystem for Linux) for best compatibility.

## Troubleshooting

### Python Version Issues

If you have Python 3.14+:
```bash
# Use Python 3.13 explicitly
python3.13 -m venv venv
```

### CMake Not Found

```bash
brew install cmake
```

### Build Failures

Ensure you have Xcode Command Line Tools:
```bash
xcode-select --install
```

### Permission Errors

Make sure scripts are executable:
```bash
chmod +x activate.sh self_test.py mcp_server/server.py examples/*.py
```

## Verification

After installation, verify all components:

```bash
source activate.sh
python self_test.py
```

Expected output:
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

## Uninstall

To remove the installation:

```bash
# Remove virtual environment
rm -rf venv

# Remove built binaries
rm -rf bin/meshfix bin/curaengine

# Remove source repositories (optional)
rm -rf meshfix_source lib3mf 3MFresh CuraEngine
```

## Next Steps

- Read [README.md](README.md) for usage examples
- Check [examples/](examples/) for sample scripts
- Review [MCP API documentation](README.md#-mcp-tools-reference)
