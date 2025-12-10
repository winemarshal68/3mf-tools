#!/Users/marshalwalkerm4mini/3d-workflows/3mf_tools/venv/bin/python
"""
MCP Tool Server for 3MF/Mesh/Slicer Automation Toolchain
Exposes mesh, 3MF, and slicer operations via MCP protocol
"""

import json
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
TOOLS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(TOOLS_DIR))

class MeshTools:
    """Mesh manipulation tools - low output, file-based operations"""

    @staticmethod
    def load(path: str) -> dict:
        """Load mesh from file"""
        try:
            import trimesh
            mesh = trimesh.load(path)
            return {"status": "success", "vertices": len(mesh.vertices), "faces": len(mesh.faces)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def save(mesh_data: str, output_path: str) -> dict:
        """Save mesh to file (mesh_data is path to existing mesh)"""
        try:
            import trimesh
            mesh = trimesh.load(mesh_data)
            mesh.export(output_path)
            return {"status": "success", "path": output_path}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def repair(input_path: str, output_path: str = None) -> dict:
        """Repair mesh using MeshFix"""
        import subprocess
        if not output_path:
            output_path = input_path.replace('.stl', '_repaired.stl')

        meshfix_bin = TOOLS_DIR / "bin" / "meshfix"
        if not meshfix_bin.exists():
            return {"status": "error", "message": "MeshFix binary not found"}

        try:
            result = subprocess.run(
                [str(meshfix_bin), input_path, "-o", output_path],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                return {"status": "success", "path": output_path}
            else:
                return {"status": "error", "message": result.stderr}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def boolean(operation: str, mesh_a_path: str, mesh_b_path: str, output_path: str) -> dict:
        """Perform boolean operation on two meshes"""
        try:
            import trimesh
            mesh_a = trimesh.load(mesh_a_path)
            mesh_b = trimesh.load(mesh_b_path)

            if operation == "union":
                result = mesh_a.union(mesh_b)
            elif operation == "difference":
                result = mesh_a.difference(mesh_b)
            elif operation == "intersection":
                result = mesh_a.intersection(mesh_b)
            else:
                return {"status": "error", "message": f"Unknown operation: {operation}"}

            result.export(output_path)
            return {"status": "success", "path": output_path}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def transform(mesh_path: str, output_path: str, scale=None, rotate=None, translate=None) -> dict:
        """Transform mesh (scale/rotate/translate)"""
        try:
            import trimesh
            import numpy as np

            mesh = trimesh.load(mesh_path)

            if scale:
                mesh.apply_scale(scale)
            if rotate:
                mesh.apply_transform(trimesh.transformations.rotation_matrix(*rotate))
            if translate:
                mesh.apply_translation(translate)

            mesh.export(output_path)
            return {"status": "success", "path": output_path}
        except Exception as e:
            return {"status": "error", "message": str(e)}


class ThreeMFTools:
    """3MF file manipulation tools"""

    @staticmethod
    def unpack(three_mf_path: str, output_dir: str = None) -> dict:
        """Unpack 3MF file to directory"""
        import zipfile
        if not output_dir:
            output_dir = three_mf_path.replace('.3mf', '_unpacked')

        try:
            os.makedirs(output_dir, exist_ok=True)
            with zipfile.ZipFile(three_mf_path, 'r') as zf:
                zf.extractall(output_dir)
            return {"status": "success", "path": output_dir}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def modify_metadata(three_mf_path: str, metadata: dict) -> dict:
        """Modify 3MF metadata (stub - needs lib3mf integration)"""
        return {"status": "stub", "message": "Metadata modification requires lib3mf Python bindings"}

    @staticmethod
    def replace_mesh(three_mf_path: str, mesh_index: int, new_mesh_path: str) -> dict:
        """Replace mesh in 3MF file (stub)"""
        return {"status": "stub", "message": "Mesh replacement requires lib3mf Python bindings"}

    @staticmethod
    def repack(unpacked_dir: str, output_file: str) -> dict:
        """Repack directory to 3MF file"""
        import zipfile
        try:
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(unpacked_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, unpacked_dir)
                        zf.write(file_path, arc_name)
            return {"status": "success", "path": output_file}
        except Exception as e:
            return {"status": "error", "message": str(e)}


class SlicerTools:
    """Slicer integration tools"""

    @staticmethod
    def slice_with_cura(model_path: str, profile_path: str, output_gcode: str) -> dict:
        """Slice model using CuraEngine"""
        import subprocess

        cura_bin = TOOLS_DIR / "bin" / "curaengine"
        if not cura_bin.exists():
            return {"status": "error", "message": "CuraEngine binary not found"}

        try:
            result = subprocess.run(
                [str(cura_bin), "slice", "-j", profile_path, "-o", output_gcode, "-l", model_path],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                return {"status": "success", "path": output_gcode}
            else:
                return {"status": "error", "message": result.stderr}
        except Exception as e:
            return {"status": "error", "message": str(e)}


# MCP Server Interface
def handle_tool_call(tool_name: str, arguments: dict) -> dict:
    """Route tool calls to appropriate handlers"""

    # Parse tool namespace
    parts = tool_name.split('.')
    if len(parts) != 2:
        return {"error": f"Invalid tool name format: {tool_name}"}

    namespace, method = parts

    # Route to appropriate tool class
    if namespace == "mesh":
        if hasattr(MeshTools, method):
            return getattr(MeshTools, method)(**arguments)
    elif namespace == "threeMF":
        if hasattr(ThreeMFTools, method):
            return getattr(ThreeMFTools, method)(**arguments)
    elif namespace == "slicer":
        if hasattr(SlicerTools, method):
            return getattr(SlicerTools, method)(**arguments)

    return {"error": f"Unknown tool: {tool_name}"}


def main():
    """MCP server main loop"""
    print("3MF Tools MCP Server started", file=sys.stderr)

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line)
            tool_name = request.get("tool")
            arguments = request.get("arguments", {})

            result = handle_tool_call(tool_name, arguments)
            print(json.dumps(result))
            sys.stdout.flush()

        except Exception as e:
            error_response = {"error": str(e)}
            print(json.dumps(error_response))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
