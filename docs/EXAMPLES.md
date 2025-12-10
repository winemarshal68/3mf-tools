# Usage Examples

Practical examples for common 3D mesh processing workflows.

## Table of Contents

- [Basic Operations](#basic-operations)
- [Mesh Repair Workflows](#mesh-repair-workflows)
- [Format Conversion](#format-conversion)
- [Boolean Operations](#boolean-operations)
- [3MF Manipulation](#3mf-manipulation)
- [Batch Processing](#batch-processing)
- [Advanced Workflows](#advanced-workflows)

---

## Basic Operations

### Load and Inspect a Mesh

```python
#!/usr/bin/env python
import trimesh

# Load mesh
mesh = trimesh.load('model.stl')

# Print statistics
print(f"Vertices: {len(mesh.vertices)}")
print(f"Faces: {len(mesh.faces)}")
print(f"Watertight: {mesh.is_watertight}")
print(f"Volume: {mesh.volume:.2f} mm³")
print(f"Surface Area: {mesh.area:.2f} mm²")
print(f"Bounds: {mesh.bounds}")
```

### Check Mesh Quality

```python
import trimesh

mesh = trimesh.load('model.stl')

# Check for issues
print(f"Is watertight: {mesh.is_watertight}")
print(f"Is convex: {mesh.is_convex}")
print(f"Euler number: {mesh.euler_number}")

# Get broken faces
broken = mesh.facets_area < 1e-10
print(f"Degenerate faces: {broken.sum()}")

# Check for duplicate vertices
print(f"Duplicate vertices: {len(mesh.vertices) - len(mesh.unique_vertices)}")
```

---

## Mesh Repair Workflows

### Basic Repair

```bash
#!/bin/bash
# Activate environment
source activate.sh

# Repair mesh
./examples/repair_mesh.py broken_model.stl fixed_model.stl
```

### Repair with Quality Check

```python
#!/usr/bin/env python
import trimesh
import subprocess

def repair_and_verify(input_file, output_file):
    # Load original
    original = trimesh.load(input_file)
    print(f"Original - Watertight: {original.is_watertight}")

    # Repair with MeshFix
    meshfix_bin = "bin/meshfix"
    subprocess.run([meshfix_bin, input_file], check=True)

    # Convert .off to .stl
    fixed_off = input_file.replace('.stl', '_fixed.off')
    fixed = trimesh.load(fixed_off)
    fixed.export(output_file)

    # Verify
    repaired = trimesh.load(output_file)
    print(f"Repaired - Watertight: {repaired.is_watertight}")
    print(f"Volume change: {abs(repaired.volume - original.volume):.2f} mm³")

    return repaired.is_watertight

# Usage
repair_and_verify('broken.stl', 'fixed.stl')
```

### Aggressive Repair Pipeline

```python
import trimesh

def aggressive_repair(input_file, output_file):
    """Multi-stage repair for severely broken meshes"""

    # Stage 1: Load and basic cleanup
    mesh = trimesh.load(input_file)
    mesh.remove_duplicate_faces()
    mesh.remove_degenerate_faces()
    mesh.remove_unreferenced_vertices()

    # Stage 2: Fill holes
    mesh.fill_holes()

    # Stage 3: Fix normals
    mesh.fix_normals()

    # Stage 4: Run MeshFix
    temp_file = "temp_stage3.stl"
    mesh.export(temp_file)
    subprocess.run(["bin/meshfix", temp_file], check=True)

    # Stage 5: Load fixed mesh
    fixed = trimesh.load(temp_file.replace('.stl', '_fixed.off'))

    # Stage 6: Final cleanup
    fixed.merge_vertices()
    fixed.remove_duplicate_faces()

    # Export
    fixed.export(output_file)
    print(f"✓ Repaired: {output_file}")
    print(f"  Watertight: {fixed.is_watertight}")

    return fixed

# Usage
aggressive_repair('severely_broken.stl', 'fully_repaired.stl')
```

---

## Format Conversion

### Batch Convert Directory

```python
#!/usr/bin/env python
import trimesh
from pathlib import Path

def batch_convert(input_dir, output_format):
    """Convert all meshes to specified format"""

    input_path = Path(input_dir)
    output_dir = input_path / f"converted_{output_format}"
    output_dir.mkdir(exist_ok=True)

    # Supported input formats
    extensions = ['.stl', '.obj', '.ply', '.off', '.3mf']

    for ext in extensions:
        for mesh_file in input_path.glob(f"*{ext}"):
            try:
                print(f"Converting {mesh_file.name}...")
                mesh = trimesh.load(mesh_file)

                output_file = output_dir / f"{mesh_file.stem}.{output_format}"
                mesh.export(output_file)

                print(f"  ✓ {output_file.name}")
            except Exception as e:
                print(f"  ✗ Error: {e}")

# Usage
batch_convert("models", "3mf")
```

### Convert with Optimization

```python
import trimesh

def convert_optimized(input_file, output_file, simplify=False):
    """Convert with optional mesh simplification"""

    mesh = trimesh.load(input_file)
    print(f"Original: {len(mesh.faces)} faces")

    if simplify:
        # Simplify to 50% face count
        target_faces = len(mesh.faces) // 2
        mesh = mesh.simplify_quadratic_decimation(target_faces)
        print(f"Simplified: {len(mesh.faces)} faces")

    # Remove redundant vertices
    mesh.merge_vertices()

    # Export
    mesh.export(output_file)
    print(f"✓ Saved: {output_file}")

# Usage
convert_optimized('high_poly.stl', 'low_poly.3mf', simplify=True)
```

---

## Boolean Operations

### Create Parametric Hole

```python
import trimesh
import numpy as np

def create_box_with_holes(width, height, depth, hole_radius, num_holes):
    """Create a box with multiple cylindrical holes"""

    # Create box
    box = trimesh.creation.box(extents=[width, height, depth])

    # Create holes along X axis
    for i in range(num_holes):
        x_pos = (i - num_holes/2 + 0.5) * (width / num_holes)

        # Create cylinder
        cylinder = trimesh.creation.cylinder(
            radius=hole_radius,
            height=depth * 1.2  # Slightly longer to ensure clean cut
        )

        # Rotate to align with X axis
        rotation = trimesh.transformations.rotation_matrix(
            np.pi/2, [0, 1, 0]
        )
        cylinder.apply_transform(rotation)

        # Position cylinder
        cylinder.apply_translation([x_pos, 0, 0])

        # Subtract from box
        box = box.difference(cylinder)

    return box

# Create and save
result = create_box_with_holes(
    width=100, height=20, depth=50,
    hole_radius=5, num_holes=5
)
result.export('box_with_holes.stl')
```

### Join Multiple Parts

```python
import trimesh

def assemble_parts(part_files, positions, output_file):
    """Assemble multiple parts into single mesh"""

    combined = None

    for part_file, position in zip(part_files, positions):
        # Load part
        part = trimesh.load(part_file)

        # Move to position
        part.apply_translation(position)

        # Combine
        if combined is None:
            combined = part
        else:
            combined = combined.union(part)

    # Export
    combined.export(output_file)
    print(f"✓ Assembled {len(part_files)} parts")
    print(f"  Output: {output_file}")

    return combined

# Usage
assemble_parts(
    ['base.stl', 'lid.stl', 'handle.stl'],
    [[0, 0, 0], [0, 0, 50], [25, 0, 25]],
    'assembled.stl'
)
```

### Create Threaded Insert

```python
import trimesh
import numpy as np

def create_threaded_hole(outer_radius, inner_radius, height, threads):
    """Create a cylinder with threaded inner hole"""

    # Outer cylinder
    outer = trimesh.creation.cylinder(radius=outer_radius, height=height)

    # Inner cylinder (hole)
    inner = trimesh.creation.cylinder(radius=inner_radius, height=height * 1.1)

    # Create threads (simplified as rings)
    thread_height = height / (threads * 2)
    for i in range(threads):
        z_pos = (i - threads/2) * (height / threads)

        thread = trimesh.creation.cylinder(
            radius=inner_radius + 0.5,
            height=thread_height
        )
        thread.apply_translation([0, 0, z_pos])
        inner = inner.union(thread)

    # Subtract inner from outer
    result = outer.difference(inner)

    return result

# Create
insert = create_threaded_hole(
    outer_radius=10, inner_radius=5,
    height=20, threads=10
)
insert.export('threaded_insert.stl')
```

---

## 3MF Manipulation

### Extract and Modify Metadata

```python
import zipfile
import xml.etree.ElementTree as ET

def modify_3mf_metadata(input_3mf, output_3mf, new_metadata):
    """Extract, modify, and repack 3MF with new metadata"""

    # Unpack
    with zipfile.ZipFile(input_3mf, 'r') as zf:
        zf.extractall('temp_3mf')

    # Modify metadata
    model_file = 'temp_3mf/3D/3dmodel.model'
    tree = ET.parse(model_file)
    root = tree.getroot()

    # Add/update metadata elements
    metadata_elem = root.find('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}metadata')
    if metadata_elem is None:
        metadata_elem = ET.SubElement(root, 'metadata')

    for key, value in new_metadata.items():
        meta = ET.SubElement(metadata_elem, 'meta')
        meta.set('name', key)
        meta.text = value

    tree.write(model_file)

    # Repack
    with zipfile.ZipFile(output_3mf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root_dir, dirs, files in os.walk('temp_3mf'):
            for file in files:
                file_path = os.path.join(root_dir, file)
                arc_name = os.path.relpath(file_path, 'temp_3mf')
                zf.write(file_path, arc_name)

    print(f"✓ Updated 3MF: {output_3mf}")

# Usage
modify_3mf_metadata(
    'model.3mf',
    'updated.3mf',
    {'Title': 'Updated Model', 'Designer': 'John Doe', 'Date': '2025-12-10'}
)
```

### Combine Multiple STLs into 3MF

```python
import trimesh

def create_multi_part_3mf(stl_files, output_3mf):
    """Combine multiple STLs into a single 3MF"""

    scene = trimesh.Scene()

    for i, stl_file in enumerate(stl_files):
        mesh = trimesh.load(stl_file)
        scene.add_geometry(mesh, node_name=f"part_{i}")

    scene.export(output_3mf)
    print(f"✓ Created 3MF with {len(stl_files)} parts")

# Usage
create_multi_part_3mf(
    ['part1.stl', 'part2.stl', 'part3.stl'],
    'assembly.3mf'
)
```

---

## Batch Processing

### Process Entire Directory

```bash
#!/bin/bash
# Repair all STL files in a directory

source activate.sh

for file in models/*.stl; do
    echo "Processing $file..."
    ./examples/repair_mesh.py "$file" "repaired/$(basename $file)"
done

echo "✓ Batch repair complete"
```

### Parallel Processing

```python
import trimesh
from pathlib import Path
from multiprocessing import Pool

def process_mesh(input_file):
    """Process single mesh"""
    try:
        mesh = trimesh.load(input_file)
        mesh.fix_normals()

        output_file = f"processed/{input_file.name}"
        mesh.export(output_file)

        return f"✓ {input_file.name}"
    except Exception as e:
        return f"✗ {input_file.name}: {e}"

def batch_process_parallel(input_dir, num_workers=4):
    """Process meshes in parallel"""

    Path("processed").mkdir(exist_ok=True)

    # Get all mesh files
    mesh_files = list(Path(input_dir).glob("*.stl"))

    # Process in parallel
    with Pool(num_workers) as pool:
        results = pool.map(process_mesh, mesh_files)

    # Print results
    for result in results:
        print(result)

# Usage
batch_process_parallel("models", num_workers=4)
```

---

## Advanced Workflows

### Automated QA Pipeline

```python
def qa_pipeline(input_file, output_file):
    """Complete QA and repair pipeline"""

    print(f"QA Pipeline: {input_file}")

    # Stage 1: Load and analyze
    print("  [1/5] Loading...")
    mesh = trimesh.load(input_file)

    issues = []
    if not mesh.is_watertight:
        issues.append("not watertight")
    if len(mesh.vertices) != len(mesh.unique_vertices):
        issues.append("duplicate vertices")
    if mesh.faces.shape[0] > 1000000:
        issues.append("high poly count")

    print(f"  Issues found: {len(issues)}")

    # Stage 2: Repair if needed
    if "not watertight" in issues:
        print("  [2/5] Repairing...")
        # Run MeshFix
        temp_file = "temp_qa.stl"
        mesh.export(temp_file)
        subprocess.run(["bin/meshfix", temp_file], check=True)
        mesh = trimesh.load(temp_file.replace('.stl', '_fixed.off'))

    # Stage 3: Optimize
    print("  [3/5] Optimizing...")
    mesh.merge_vertices()
    mesh.remove_duplicate_faces()

    # Stage 4: Validate
    print("  [4/5] Validating...")
    assert mesh.is_watertight, "Mesh still not watertight!"

    # Stage 5: Export
    print("  [5/5] Exporting...")
    mesh.export(output_file)

    print(f"✓ QA Complete: {output_file}")
    print(f"  Vertices: {len(mesh.vertices)}")
    print(f"  Faces: {len(mesh.faces)}")
    print(f"  Volume: {mesh.volume:.2f} mm³")

# Usage
qa_pipeline("raw_model.stl", "qa_approved.stl")
```

---

## More Examples

Check the [examples/](../examples/) directory for:
- `repair_mesh.py` - Mesh repair script
- `convert_formats.py` - Format conversion with batch mode
- `boolean_ops.py` - Boolean operations demo

## Need Help?

- Check [API.md](API.md) for complete API reference
- See [README.md](../README.md) for tool documentation
- Run `./examples/script.py --help` for usage information
