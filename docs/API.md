# MCP Tools API Reference

Complete reference for all MCP tools exposed by the 3MF Tools server.

## Table of Contents

- [Mesh Operations](#mesh-operations)
- [3MF Operations](#3mf-operations)
- [Slicer Operations](#slicer-operations)
- [Response Format](#response-format)
- [Error Handling](#error-handling)

## Overview

All tools accept JSON-formatted requests via stdin and return JSON responses. The server uses a simple request/response protocol optimized for low token usage.

### Request Format

```json
{
  "tool": "namespace.method",
  "arguments": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

### Response Format

```json
{
  "status": "success|error|stub",
  "path": "/path/to/output/file",
  "message": "Status message",
  ...additional fields...
}
```

---

## Mesh Operations

### `mesh.load`

Load a mesh file and return statistics.

**Parameters:**
- `path` (string, required): Path to mesh file

**Supported Formats:** STL, OBJ, PLY, OFF, 3MF, GLB, GLTF

**Returns:**
```json
{
  "status": "success",
  "vertices": 1234,
  "faces": 2468
}
```

**Example:**
```json
{"tool": "mesh.load", "arguments": {"path": "/path/to/model.stl"}}
```

**Use Cases:**
- Validate mesh file integrity
- Get quick mesh statistics
- Check file format compatibility

---

### `mesh.save`

Save a mesh to a different format.

**Parameters:**
- `mesh_data` (string, required): Path to source mesh
- `output_path` (string, required): Path to output file

**Example:**
```json
{
  "tool": "mesh.save",
  "arguments": {
    "mesh_data": "/path/to/input.obj",
    "output_path": "/path/to/output.stl"
  }
}
```

**Returns:**
```json
{
  "status": "success",
  "path": "/path/to/output.stl"
}
```

---

### `mesh.repair`

Repair mesh using MeshFix algorithm.

**Parameters:**
- `input_path` (string, required): Path to input mesh
- `output_path` (string, optional): Path to output mesh (default: `{input}_repaired.stl`)

**Algorithm:** Uses Marco Attene's MeshFix for:
- Closing holes
- Removing self-intersections
- Fixing non-manifold geometry
- Removing degenerate faces

**Example:**
```json
{
  "tool": "mesh.repair",
  "arguments": {
    "input_path": "/path/to/broken.stl",
    "output_path": "/path/to/fixed.stl"
  }
}
```

**Returns:**
```json
{
  "status": "success",
  "path": "/path/to/fixed.stl"
}
```

**Notes:**
- MeshFix outputs .off format by default, automatically converted to requested format
- Processing time scales with mesh complexity
- Very large meshes (>1M faces) may take several minutes

---

### `mesh.boolean`

Perform boolean operations on two meshes.

**Parameters:**
- `operation` (string, required): Operation type: `union`, `difference`, `intersection`
- `mesh_a_path` (string, required): Path to first mesh
- `mesh_b_path` (string, required): Path to second mesh
- `output_path` (string, required): Path to output mesh

**Operations:**
- **union**: Combine meshes (A + B)
- **difference**: Subtract B from A (A - B)
- **intersection**: Keep only overlapping volume (A ∩ B)

**Example:**
```json
{
  "tool": "mesh.boolean",
  "arguments": {
    "operation": "union",
    "mesh_a_path": "/path/to/part1.stl",
    "mesh_b_path": "/path/to/part2.stl",
    "output_path": "/path/to/combined.stl"
  }
}
```

**Returns:**
```json
{
  "status": "success",
  "path": "/path/to/combined.stl"
}
```

**Notes:**
- Meshes should be watertight for best results
- May require repair after boolean operations
- Performance depends on mesh complexity

---

### `mesh.transform`

Apply transformations to a mesh.

**Parameters:**
- `mesh_path` (string, required): Path to input mesh
- `output_path` (string, required): Path to output mesh
- `scale` (float, optional): Uniform scale factor
- `rotate` (array, optional): Rotation [angle, x, y, z]
- `translate` (array, optional): Translation [x, y, z]

**Example - Scale:**
```json
{
  "tool": "mesh.transform",
  "arguments": {
    "mesh_path": "/path/to/input.stl",
    "output_path": "/path/to/scaled.stl",
    "scale": 2.0
  }
}
```

**Example - Rotate:**
```json
{
  "tool": "mesh.transform",
  "arguments": {
    "mesh_path": "/path/to/input.stl",
    "output_path": "/path/to/rotated.stl",
    "rotate": [1.5708, 0, 0, 1]
  }
}
```

**Example - Translate:**
```json
{
  "tool": "mesh.transform",
  "arguments": {
    "mesh_path": "/path/to/input.stl",
    "output_path": "/path/to/moved.stl",
    "translate": [10, 0, 5]
  }
}
```

**Returns:**
```json
{
  "status": "success",
  "path": "/path/to/output.stl"
}
```

---

## 3MF Operations

### `threeMF.unpack`

Extract contents of a 3MF file to a directory.

**Parameters:**
- `three_mf_path` (string, required): Path to .3mf file
- `output_dir` (string, optional): Output directory (default: `{filename}_unpacked`)

**Example:**
```json
{
  "tool": "threeMF.unpack",
  "arguments": {
    "three_mf_path": "/path/to/model.3mf",
    "output_dir": "/path/to/extracted"
  }
}
```

**Returns:**
```json
{
  "status": "success",
  "path": "/path/to/extracted"
}
```

**Extracted Structure:**
```
extracted/
├── [Content_Types].xml
├── _rels/
│   └── .rels
├── 3D/
│   └── 3dmodel.model
└── Metadata/
    └── thumbnail.png
```

**Use Cases:**
- Inspect 3MF internal structure
- Extract embedded meshes
- Modify metadata or relationships
- Extract thumbnails

---

### `threeMF.repack`

Create a 3MF file from a directory.

**Parameters:**
- `unpacked_dir` (string, required): Directory with 3MF contents
- `output_file` (string, required): Path to output .3mf file

**Example:**
```json
{
  "tool": "threeMF.repack",
  "arguments": {
    "unpacked_dir": "/path/to/modified",
    "output_file": "/path/to/new.3mf"
  }
}
```

**Returns:**
```json
{
  "status": "success",
  "path": "/path/to/new.3mf"
}
```

**Workflow:**
```bash
# 1. Unpack
threeMF.unpack → /extracted/

# 2. Modify files in /extracted/

# 3. Repack
threeMF.repack → new.3mf
```

---

### `threeMF.modify_metadata`

Modify 3MF metadata (requires lib3mf Python bindings).

**Status:** Stub - requires lib3mf Python bindings

**Parameters:**
- `three_mf_path` (string, required): Path to .3mf file
- `metadata` (object, required): Metadata key-value pairs

**Example:**
```json
{
  "tool": "threeMF.modify_metadata",
  "arguments": {
    "three_mf_path": "/path/to/model.3mf",
    "metadata": {
      "Title": "Updated Model",
      "Designer": "John Doe"
    }
  }
}
```

---

### `threeMF.replace_mesh`

Replace a mesh within a 3MF file.

**Status:** Stub - requires lib3mf Python bindings

**Parameters:**
- `three_mf_path` (string, required): Path to .3mf file
- `mesh_index` (int, required): Index of mesh to replace
- `new_mesh_path` (string, required): Path to replacement mesh

**Example:**
```json
{
  "tool": "threeMF.replace_mesh",
  "arguments": {
    "three_mf_path": "/path/to/model.3mf",
    "mesh_index": 0,
    "new_mesh_path": "/path/to/new_part.stl"
  }
}
```

---

## Slicer Operations

### `slicer.slice_with_cura`

Slice a 3D model using CuraEngine.

**Status:** Requires CuraEngine build

**Parameters:**
- `model_path` (string, required): Path to mesh file
- `profile_path` (string, required): Path to Cura profile JSON
- `output_gcode` (string, required): Path to output G-code

**Example:**
```json
{
  "tool": "slicer.slice_with_cura",
  "arguments": {
    "model_path": "/path/to/model.stl",
    "profile_path": "/path/to/profile.json",
    "output_gcode": "/path/to/output.gcode"
  }
}
```

**Returns:**
```json
{
  "status": "success",
  "path": "/path/to/output.gcode"
}
```

**Setup Required:**
1. Build CuraEngine (see [CuraEngine.md](CuraEngine.md))
2. Create or export Cura profile
3. Configure slicer settings

---

## Response Format

All tools return consistent response structures.

### Success Response

```json
{
  "status": "success",
  "path": "/path/to/output",
  ...additional data...
}
```

### Error Response

```json
{
  "status": "error",
  "message": "Error description"
}
```

### Stub Response

For features not yet implemented:

```json
{
  "status": "stub",
  "message": "Feature description and requirements"
}
```

---

## Error Handling

### Common Errors

**File Not Found:**
```json
{
  "status": "error",
  "message": "No such file or directory: '/path/to/file.stl'"
}
```

**Invalid Format:**
```json
{
  "status": "error",
  "message": "Unable to load mesh from file"
}
```

**Operation Failed:**
```json
{
  "status": "error",
  "message": "Boolean operation failed: meshes not watertight"
}
```

### Best Practices

1. **Validate inputs** - Check file existence before calling
2. **Handle timeouts** - Large operations may take time
3. **Check status** - Always verify `"status": "success"`
4. **Parse errors** - Log error messages for debugging

---

## Usage Examples

### Python Client

```python
import json
import subprocess

def call_mcp_tool(tool, arguments):
    request = json.dumps({"tool": tool, "arguments": arguments})

    proc = subprocess.Popen(
        ['python', 'mcp_server/server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    output, _ = proc.communicate(request + '\n')
    return json.loads(output)

# Example: Load mesh
result = call_mcp_tool("mesh.load", {"path": "model.stl"})
print(f"Vertices: {result['vertices']}, Faces: {result['faces']}")
```

### Bash Client

```bash
echo '{"tool": "mesh.load", "arguments": {"path": "model.stl"}}' | \
  python mcp_server/server.py
```

---

## Performance Notes

| Operation | Typical Time | Factors |
|-----------|-------------|---------|
| `mesh.load` | < 1s | File size |
| `mesh.repair` | 1-60s | Complexity, defects |
| `mesh.boolean` | 2-30s | Mesh size, operation |
| `mesh.transform` | < 1s | Mesh size |
| `threeMF.unpack` | < 1s | File size |
| `threeMF.repack` | < 1s | Number of files |

**Tips for Performance:**
- Pre-validate files before calling expensive operations
- Use batch processing for multiple operations
- Cache loaded meshes when possible
- Monitor timeout thresholds for large files

---

## Version Information

**API Version:** 1.0
**MCP Protocol:** JSON over stdin/stdout
**Server:** Python 3.13+
**Last Updated:** December 2025
