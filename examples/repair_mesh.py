#!/Users/marshalwalkerm4mini/3d-workflows/3mf_tools/venv/bin/python
"""
Example: Repair a broken mesh using MeshFix
"""

import sys
import subprocess
from pathlib import Path

def repair_mesh(input_file, output_file=None):
    """
    Repair mesh using MeshFix and convert to STL
    """
    import trimesh

    # Get paths
    input_path = Path(input_file)
    if output_file is None:
        output_file = input_path.stem + "_repaired.stl"

    # Step 1: Run MeshFix
    print(f"Repairing {input_file}...")
    meshfix_bin = Path(__file__).parent.parent / "bin" / "meshfix"

    result = subprocess.run(
        [str(meshfix_bin), str(input_path)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None

    # MeshFix outputs filename_fixed.off
    fixed_off = input_path.parent / f"{input_path.stem}_fixed.off"

    if not fixed_off.exists():
        print("Error: MeshFix did not produce output file")
        return None

    # Step 2: Convert OFF to STL
    print(f"Converting to STL...")
    mesh = trimesh.load(str(fixed_off))
    mesh.export(str(output_file))

    print(f"✓ Repaired mesh saved to: {output_file}")
    print(f"  Vertices: {len(mesh.vertices)}")
    print(f"  Faces: {len(mesh.faces)}")

    # Cleanup intermediate file
    fixed_off.unlink()

    return output_file


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: repair_mesh.py <input.stl> [output.stl]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    result = repair_mesh(input_file, output_file)
    sys.exit(0 if result else 1)
