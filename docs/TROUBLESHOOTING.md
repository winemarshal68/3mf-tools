# Troubleshooting Guide

Common issues and solutions for 3MF Tools.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Python Environment](#python-environment)
- [Mesh Operations](#mesh-operations)
- [Build Errors](#build-errors)
- [Runtime Errors](#runtime-errors)
- [Performance Issues](#performance-issues)

---

## Installation Issues

### Homebrew Not Found

**Error:**
```
brew: command not found
```

**Solution:**
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### Python 3.13 Not Available

**Error:**
```
python3.13: command not found
```

**Solution:**
```bash
# Install Python 3.13 via Homebrew
brew install python@3.13

# Verify installation
python3.13 --version
```

---

### CMake Installation Fails

**Error:**
```
cmake: command not found
```

**Solution:**
```bash
# Install CMake
brew install cmake

# Verify
cmake --version
```

---

## Python Environment

### Virtual Environment Not Activating

**Error:**
```
source: no such file or directory: venv/bin/activate
```

**Solution:**
```bash
# Ensure venv exists
python3.13 -m venv venv

# Activate
source venv/bin/activate
```

---

### Import Errors

**Error:**
```python
ModuleNotFoundError: No module named 'trimesh'
```

**Solution:**
```bash
# Activate environment first
source activate.sh

# Or manually
source venv/bin/activate
pip install trimesh numpy scipy meshio networkx lxml
```

---

### Wrong Python Version

**Error:**
```
Python 3.14 is not supported
```

**Solution:**
```bash
# Use Python 3.13 specifically
python3.13 -m venv venv
source venv/bin/activate

# Verify
python --version  # Should show 3.13.x
```

---

## Mesh Operations

### MeshFix Outputs .OFF Instead of .STL

**Issue:**
MeshFix outputs `.off` format by default.

**Solution:**
```python
import trimesh

# Convert OFF to STL
mesh = trimesh.load('model_fixed.off')
mesh.export('model_fixed.stl')
```

Or use the repair script:
```bash
./examples/repair_mesh.py input.stl output.stl
```

---

### Mesh Not Watertight After Repair

**Issue:**
Some meshes are too broken for automatic repair.

**Solution:**
```python
# Try aggressive repair
import trimesh

mesh = trimesh.load('broken.stl')

# Step 1: Fill holes
mesh.fill_holes()

# Step 2: Fix normals
mesh.fix_normals()

# Step 3: Remove duplicates
mesh.merge_vertices()
mesh.remove_duplicate_faces()

# Step 4: Run MeshFix
mesh.export('temp.stl')
subprocess.run(['bin/meshfix', 'temp.stl'])

# Step 5: Load and verify
fixed = trimesh.load('temp_fixed.off')
print(f"Watertight: {fixed.is_watertight}")
```

---

### Boolean Operations Fail

**Error:**
```
Boolean operation failed: meshes not watertight
```

**Solution:**
1. Ensure both meshes are watertight
2. Repair meshes first
3. Check that meshes actually overlap

```python
import trimesh

# Verify meshes
mesh_a = trimesh.load('part_a.stl')
mesh_b = trimesh.load('part_b.stl')

print(f"A watertight: {mesh_a.is_watertight}")
print(f"B watertight: {mesh_b.is_watertight}")

# Check overlap
print(f"A bounds: {mesh_a.bounds}")
print(f"B bounds: {mesh_b.bounds}")

# Repair if needed
if not mesh_a.is_watertight:
    mesh_a.fill_holes()
if not mesh_b.is_watertight:
    mesh_b.fill_holes()

# Try boolean
result = mesh_a.union(mesh_b)
```

---

### Large Files Timeout

**Issue:**
Processing very large meshes (>1M faces) times out.

**Solution:**
```python
# Simplify mesh first
import trimesh

mesh = trimesh.load('huge_model.stl')
print(f"Original: {len(mesh.faces)} faces")

# Reduce to 50% face count
target = len(mesh.faces) // 2
simplified = mesh.simplify_quadratic_decimation(target)
print(f"Simplified: {len(simplified.faces)} faces")

# Process simplified mesh
simplified.export('simplified.stl')
```

---

## Build Errors

### MeshFix Build Fails

**Error:**
```
CMake Error: The source directory does not exist
```

**Solution:**
```bash
# Ensure repository is cloned
cd 3mf_tools
git clone https://github.com/MarcoAttene/MeshFix-V2.1.git meshfix_source

# Build
cd meshfix_source
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5
make -j4
```

---

### lib3mf Build Fails - Missing Submodules

**Error:**
```
CMake Error: libzip directory not found
```

**Solution:**
```bash
# Initialize submodules
cd lib3mf
git submodule update --init --recursive

# Rebuild
cd build
rm -rf *
cmake .. -DCMAKE_BUILD_TYPE=Release -DLIB3MF_TESTS=OFF
make -j4
```

---

### Compiler Errors on macOS

**Error:**
```
xcrun: error: invalid active developer path
```

**Solution:**
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Accept license
sudo xcodebuild -license accept
```

---

## Runtime Errors

### Permission Denied

**Error:**
```
Permission denied: './self_test.py'
```

**Solution:**
```bash
# Make scripts executable
chmod +x self_test.py activate.sh mcp_server/server.py examples/*.py

# Or run with python
python self_test.py
```

---

### Library Not Found

**Error:**
```
dyld: Library not loaded: @rpath/lib3mf.dylib
```

**Solution:**
```bash
# Set library path
export DYLD_LIBRARY_PATH="$PWD/lib3mf/build:$DYLD_LIBRARY_PATH"

# Or use activation script
source activate.sh
```

---

### MCP Server Not Responding

**Issue:**
Server doesn't respond to requests.

**Solution:**
```bash
# Test server manually
echo '{"tool": "mesh.load", "arguments": {"path": "test_cube.stl"}}' | \
  python mcp_server/server.py

# Check for errors
python mcp_server/server.py 2>&1 | head -20
```

---

## Performance Issues

### Slow Mesh Loading

**Issue:**
Large files take too long to load.

**Solution:**
```python
# Use process=False for STL files to skip validation
import trimesh

mesh = trimesh.load('large.stl', process=False)

# Process manually if needed
mesh.process()
```

---

### High Memory Usage

**Issue:**
Processing uses too much RAM.

**Solution:**
1. **Simplify meshes** before processing
2. **Process in batches** instead of all at once
3. **Use generators** for batch operations

```python
from pathlib import Path

# Bad: Load all at once
# meshes = [trimesh.load(f) for f in files]

# Good: Process one at a time
for mesh_file in Path('models').glob('*.stl'):
    mesh = trimesh.load(mesh_file)
    # Process
    mesh.export(f"processed/{mesh_file.name}")
    del mesh  # Free memory
```

---

### Slow Boolean Operations

**Issue:**
Boolean operations take too long.

**Solution:**
```python
# Voxelize meshes for faster boolean ops
import trimesh

mesh_a = trimesh.load('part_a.stl')
mesh_b = trimesh.load('part_b.stl')

# Convert to voxel representation
voxel_a = mesh_a.voxelized(pitch=1.0)
voxel_b = mesh_b.voxelized(pitch=1.0)

# Boolean in voxel space (faster)
result_voxel = voxel_a.union(voxel_b)

# Convert back to mesh
result = result_voxel.as_boxes()
result.export('combined.stl')
```

---

## Platform-Specific Issues

### macOS: "Cannot Verify Developer"

**Error:**
```
"meshfix" cannot be opened because the developer cannot be verified
```

**Solution:**
```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine bin/meshfix

# Or allow in System Preferences > Security & Privacy
```

---

### macOS: Python SSL Errors

**Error:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution:**
```bash
# Run certificate install
/Applications/Python\ 3.13/Install\ Certificates.command

# Or use system certificates
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org trimesh
```

---

## Getting More Help

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Run Self-Test

```bash
python self_test.py
```

### Check System Info

```bash
# Python version
python --version

# Package versions
pip list | grep -E "trimesh|numpy|scipy"

# System info
uname -a
```

### Report Issues

If you encounter a bug:

1. Run self-test: `python self_test.py`
2. Collect error messages
3. Note your system: macOS version, Python version
4. [Open an issue](https://github.com/winemarshal68/3mf-tools/issues) with:
   - Error message
   - Steps to reproduce
   - System information
   - Self-test output

---

## FAQ

### Q: Can I use Python 3.12 or 3.14?

A: Python 3.13 is recommended. 3.12 might work but pymeshlab isn't compatible. 3.14+ is untested.

### Q: Does this work on Windows?

A: Not tested. Try WSL2 (Windows Subsystem for Linux) for best compatibility.

### Q: Do I need CuraEngine to use mesh tools?

A: No. Mesh operations work without CuraEngine. Slicing requires CuraEngine or alternative slicer.

### Q: How do I update the toolchain?

```bash
cd 3mf_tools
git pull
source venv/bin/activate
pip install --upgrade trimesh numpy scipy meshio
```

### Q: Can I use this in Docker?

Yes! Create a Dockerfile:
```dockerfile
FROM python:3.13-slim
RUN apt-get update && apt-get install -y git cmake build-essential
COPY . /app
WORKDIR /app
RUN ./install.sh
CMD ["python", "mcp_server/server.py"]
```

---

**Still stuck?** Open an issue on [GitHub](https://github.com/winemarshal68/3mf-tools/issues)
