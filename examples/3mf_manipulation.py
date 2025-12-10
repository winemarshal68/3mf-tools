#!/Users/marshalwalkerm4mini/3d-workflows/3mf_tools/venv/bin/python
"""
Example: 3MF file manipulation - unpack, modify, repack
"""

import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

def unpack_3mf(three_mf_path, output_dir):
    """Unpack 3MF file to directory"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Unpacking {three_mf_path}...")
    with zipfile.ZipFile(three_mf_path, 'r') as zf:
        zf.extractall(output_path)

    print(f"✓ Extracted to {output_dir}")

    # List contents
    print("\nContents:")
    for item in output_path.rglob('*'):
        if item.is_file():
            print(f"  {item.relative_to(output_path)}")

    return output_path


def modify_metadata(unpacked_dir, metadata_dict):
    """Modify metadata in unpacked 3MF"""
    model_file = Path(unpacked_dir) / "3D" / "3dmodel.model"

    if not model_file.exists():
        print("Error: 3dmodel.model not found")
        return False

    print("\nModifying metadata...")

    # Parse XML
    tree = ET.parse(model_file)
    root = tree.getroot()

    # Find or create metadata section
    ns = {'model': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    metadata_elem = root.find('.//model:metadata', ns)

    if metadata_elem is None:
        metadata_elem = ET.SubElement(root, 'metadata')

    # Add/update metadata
    for key, value in metadata_dict.items():
        # Remove existing
        for meta in metadata_elem.findall(f".//model:meta[@name='{key}']", ns):
            metadata_elem.remove(meta)

        # Add new
        meta = ET.SubElement(metadata_elem, 'meta')
        meta.set('name', key)
        meta.text = value
        print(f"  {key}: {value}")

    # Save
    tree.write(model_file, encoding='utf-8', xml_declaration=True)
    print("✓ Metadata updated")

    return True


def repack_3mf(unpacked_dir, output_file):
    """Repack directory into 3MF file"""
    unpacked_path = Path(unpacked_dir)
    output_path = Path(output_file)

    print(f"\nRepacking to {output_file}...")

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in unpacked_path.rglob('*'):
            if file_path.is_file():
                arc_name = file_path.relative_to(unpacked_path)
                zf.write(file_path, arc_name)
                print(f"  Adding {arc_name}")

    print(f"✓ Created {output_file}")
    return output_path


def extract_meshes(three_mf_path, output_dir):
    """Extract all mesh files from 3MF"""
    import trimesh

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Extracting meshes from {three_mf_path}...")

    # Unpack
    temp_dir = Path("temp_extract")
    with zipfile.ZipFile(three_mf_path, 'r') as zf:
        zf.extractall(temp_dir)

    # Find 3dmodel.model
    model_file = temp_dir / "3D" / "3dmodel.model"

    if model_file.exists():
        # Parse and extract meshes
        tree = ET.parse(model_file)
        root = tree.getroot()

        ns = {'model': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
        meshes = root.findall('.//model:mesh', ns)

        for i, mesh_elem in enumerate(meshes):
            print(f"\n  Mesh {i}:")

            # Extract vertices and triangles
            vertices = []
            for vertex in mesh_elem.findall('.//model:vertex', ns):
                x = float(vertex.get('x'))
                y = float(vertex.get('y'))
                z = float(vertex.get('z'))
                vertices.append([x, y, z])

            faces = []
            for triangle in mesh_elem.findall('.//model:triangle', ns):
                v1 = int(triangle.get('v1'))
                v2 = int(triangle.get('v2'))
                v3 = int(triangle.get('v3'))
                faces.append([v1, v2, v3])

            # Create mesh
            import numpy as np
            mesh = trimesh.Trimesh(
                vertices=np.array(vertices),
                faces=np.array(faces)
            )

            # Save
            output_file = output_path / f"mesh_{i}.stl"
            mesh.export(output_file)
            print(f"    Vertices: {len(vertices)}, Faces: {len(faces)}")
            print(f"    Saved to {output_file}")

    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)

    print(f"\n✓ Extracted {len(meshes)} meshes")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Unpack:   3mf_manipulation.py unpack <input.3mf> [output_dir]")
        print("  Modify:   3mf_manipulation.py modify <unpacked_dir> <key> <value> ...")
        print("  Repack:   3mf_manipulation.py repack <unpacked_dir> <output.3mf>")
        print("  Extract:  3mf_manipulation.py extract <input.3mf> [output_dir]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "unpack":
        input_file = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else f"{Path(input_file).stem}_unpacked"
        unpack_3mf(input_file, output_dir)

    elif command == "modify":
        unpacked_dir = sys.argv[2]
        metadata = {}
        for i in range(3, len(sys.argv), 2):
            if i+1 < len(sys.argv):
                metadata[sys.argv[i]] = sys.argv[i+1]
        modify_metadata(unpacked_dir, metadata)

    elif command == "repack":
        unpacked_dir = sys.argv[2]
        output_file = sys.argv[3]
        repack_3mf(unpacked_dir, output_file)

    elif command == "extract":
        input_file = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "extracted_meshes"
        extract_meshes(input_file, output_dir)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
