#!/Users/marshalwalkerm4mini/3d-workflows/3mf_tools/venv/bin/python
"""
Example: Boolean operations on meshes
"""

import sys

def boolean_operation(mesh_a_path, mesh_b_path, operation, output_path):
    """
    Perform boolean operations on two meshes

    Operations: union, difference, intersection
    """
    import trimesh

    print(f"Loading meshes...")
    mesh_a = trimesh.load(str(mesh_a_path))
    mesh_b = trimesh.load(str(mesh_b_path))

    print(f"Mesh A: {len(mesh_a.vertices)} vertices, {len(mesh_a.faces)} faces")
    print(f"Mesh B: {len(mesh_b.vertices)} vertices, {len(mesh_b.faces)} faces")

    print(f"\nPerforming {operation} operation...")

    if operation == "union":
        result = mesh_a.union(mesh_b)
    elif operation == "difference":
        result = mesh_a.difference(mesh_b)
    elif operation == "intersection":
        result = mesh_a.intersection(mesh_b)
    else:
        print(f"Error: Unknown operation '{operation}'")
        print("Valid operations: union, difference, intersection")
        return None

    print(f"Result: {len(result.vertices)} vertices, {len(result.faces)} faces")

    print(f"\nSaving to {output_path}...")
    result.export(str(output_path))

    print(f"✓ Boolean operation complete!")
    return output_path


def create_cube_with_hole():
    """
    Example: Create a cube with a cylindrical hole through it
    """
    import trimesh
    import numpy as np

    print("Creating cube with hole example...")

    # Create a cube
    cube = trimesh.creation.box(extents=[10, 10, 10])

    # Create a cylinder to subtract
    cylinder = trimesh.creation.cylinder(radius=2, height=12)

    # Perform difference operation
    result = cube.difference(cylinder)

    output_path = "cube_with_hole.stl"
    result.export(output_path)

    print(f"✓ Created {output_path}")
    print(f"  Vertices: {len(result.vertices)}")
    print(f"  Faces: {len(result.faces)}")

    return output_path


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--example":
        # Run example
        create_cube_with_hole()
    elif len(sys.argv) == 5:
        # Perform boolean operation
        mesh_a = sys.argv[1]
        mesh_b = sys.argv[2]
        operation = sys.argv[3]
        output = sys.argv[4]

        result = boolean_operation(mesh_a, mesh_b, operation, output)
        sys.exit(0 if result else 1)
    else:
        print("Usage:")
        print("  Example:  boolean_ops.py --example")
        print("  Custom:   boolean_ops.py <mesh_a> <mesh_b> <operation> <output>")
        print("\nOperations: union, difference, intersection")
        sys.exit(1)
