#!/Users/marshalwalkerm4mini/3d-workflows/3mf_tools/venv/bin/python
"""
Example: Convert between different 3D mesh formats
"""

import sys
from pathlib import Path

def convert_mesh(input_file, output_file):
    """
    Convert mesh between formats
    Supports: STL, OBJ, PLY, OFF, 3MF, and more
    """
    import trimesh

    print(f"Loading {input_file}...")
    mesh = trimesh.load(str(input_file))

    print(f"Mesh stats:")
    print(f"  Vertices: {len(mesh.vertices)}")
    print(f"  Faces: {len(mesh.faces)}")
    print(f"  Watertight: {mesh.is_watertight}")

    print(f"\nExporting to {output_file}...")
    mesh.export(str(output_file))

    print(f"✓ Conversion complete!")
    return output_file


def batch_convert(input_dir, output_format):
    """
    Convert all meshes in a directory to a specific format
    """
    import trimesh
    from pathlib import Path

    input_path = Path(input_dir)
    output_dir = input_path / f"converted_{output_format}"
    output_dir.mkdir(exist_ok=True)

    # Find all mesh files
    mesh_extensions = ['.stl', '.obj', '.ply', '.off', '.3mf']
    mesh_files = []
    for ext in mesh_extensions:
        mesh_files.extend(input_path.glob(f"*{ext}"))

    print(f"Found {len(mesh_files)} mesh files")

    for mesh_file in mesh_files:
        output_file = output_dir / f"{mesh_file.stem}.{output_format}"
        print(f"Converting {mesh_file.name}...")

        try:
            mesh = trimesh.load(str(mesh_file))
            mesh.export(str(output_file))
            print(f"  ✓ Saved to {output_file}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print(f"\n✓ Batch conversion complete!")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Single file: convert_formats.py <input> <output>")
        print("  Batch:       convert_formats.py --batch <dir> <format>")
        print("\nSupported formats: stl, obj, ply, off, 3mf")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        batch_convert(sys.argv[2], sys.argv[3])
    else:
        convert_mesh(sys.argv[1], sys.argv[2])

    sys.exit(0)
