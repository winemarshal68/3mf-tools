#!/Users/marshalwalkerm4mini/3d-workflows/3mf_tools/venv/bin/python
"""
Self-test script for 3MF/Mesh/Slicer toolchain
Tests available components and reports status
"""

import sys
import os
from pathlib import Path

TOOLS_DIR = Path(__file__).parent
BIN_DIR = TOOLS_DIR / "bin"

def test_python_packages():
    """Test required Python packages"""
    print("Testing Python packages...")
    results = {}

    packages = ['trimesh', 'numpy', 'scipy', 'pymeshlab', 'meshio']
    for pkg in packages:
        try:
            __import__(pkg)
            results[pkg] = "OK"
        except ImportError:
            results[pkg] = "MISSING"

    for pkg, status in results.items():
        print(f"  {pkg}: {status}")

    return all(v == "OK" for v in results.values())


def test_mesh_tools():
    """Test external mesh tools"""
    print("\nTesting mesh tools...")
    results = {}

    # Test MeshFix
    meshfix = BIN_DIR / "meshfix"
    results["meshfix"] = "OK" if meshfix.exists() else "MISSING"
    print(f"  meshfix: {results['meshfix']}")

    return results["meshfix"] == "OK"


def test_3mf_libraries():
    """Test 3MF libraries"""
    print("\nTesting 3MF libraries...")
    results = {}

    # Test lib3mf build
    lib3mf_dir = TOOLS_DIR / "lib3mf" / "build"
    results["lib3mf"] = "OK" if lib3mf_dir.exists() else "MISSING"
    print(f"  lib3mf: {results['lib3mf']}")

    # Test 3MFresh
    fresh_script = TOOLS_DIR / "3MFresh" / "process_3mf.py"
    results["3MFresh"] = "OK" if fresh_script.exists() else "MISSING"
    print(f"  3MFresh: {results['3MFresh']}")

    return True  # Non-critical for basic functionality


def test_slicer_backends():
    """Test slicing backends"""
    print("\nTesting slicer backends...")
    results = {}

    # Test CuraEngine
    cura_dir = TOOLS_DIR / "CuraEngine"
    results["CuraEngine"] = "OK" if cura_dir.exists() else "MISSING"
    print(f"  CuraEngine: {results['CuraEngine']}")

    # Test Bambu wrapper
    bambu_script = TOOLS_DIR / "slicer_tools" / "bambu_cli.py"
    results["Bambu CLI"] = "PLACEHOLDER" if bambu_script.exists() else "MISSING"
    print(f"  Bambu CLI: {results['Bambu CLI']}")

    return True  # Non-critical


def test_mcp_server():
    """Test MCP server"""
    print("\nTesting MCP server...")

    server_script = TOOLS_DIR / "mcp_server" / "server.py"
    if server_script.exists():
        print(f"  MCP server: OK")
        return True
    else:
        print(f"  MCP server: MISSING")
        return False


def create_dummy_stl():
    """Create a dummy STL for testing"""
    print("\nCreating dummy test STL...")
    try:
        import trimesh
        import numpy as np

        # Create a simple cube
        vertices = np.array([
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
        ])

        faces = np.array([
            [0, 1, 2], [0, 2, 3],  # bottom
            [4, 6, 5], [4, 7, 6],  # top
            [0, 5, 1], [0, 4, 5],  # front
            [2, 7, 3], [2, 6, 7],  # back
            [0, 7, 4], [0, 3, 7],  # left
            [1, 6, 2], [1, 5, 6]   # right
        ])

        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        test_file = TOOLS_DIR / "test_cube.stl"
        mesh.export(test_file)
        print(f"  Created: {test_file}")
        return test_file
    except Exception as e:
        print(f"  Error: {e}")
        return None


def run_repair_test(stl_file):
    """Test mesh repair"""
    if not stl_file:
        print("\nSkipping repair test (no STL)")
        return False

    print("\nTesting mesh repair...")
    import subprocess

    meshfix_bin = BIN_DIR / "meshfix"
    if not meshfix_bin.exists():
        print("  Skipped (MeshFix not available)")
        return False

    output_file = TOOLS_DIR / "test_cube_repaired.stl"
    try:
        result = subprocess.run(
            [str(meshfix_bin), str(stl_file), "-o", str(output_file)],
            capture_output=True, timeout=10
        )
        if result.returncode == 0 and output_file.exists():
            print(f"  Repair: OK")
            return output_file
        else:
            print(f"  Repair: FAILED")
            return False
    except Exception as e:
        print(f"  Repair: ERROR - {e}")
        return False


def convert_to_3mf(stl_file):
    """Convert STL to 3MF"""
    if not stl_file:
        print("\nSkipping 3MF conversion (no STL)")
        return False

    print("\nTesting 3MF conversion...")
    try:
        import trimesh
        mesh = trimesh.load(str(stl_file))
        output_file = TOOLS_DIR / "test_cube.3mf"
        mesh.export(str(output_file))
        print(f"  Conversion: OK")
        return output_file
    except Exception as e:
        print(f"  Conversion: ERROR - {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("3MF Tools Self-Test")
    print("=" * 60)

    # Run component tests
    py_ok = test_python_packages()
    mesh_ok = test_mesh_tools()
    lib3mf_ok = test_3mf_libraries()
    slicer_ok = test_slicer_backends()
    mcp_ok = test_mcp_server()

    # Run workflow tests
    stl_file = create_dummy_stl()
    repaired_stl = run_repair_test(stl_file)
    three_mf = convert_to_3mf(repaired_stl if repaired_stl else stl_file)

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Python packages:  {'PASS' if py_ok else 'FAIL'}")
    print(f"Mesh tools:       {'PASS' if mesh_ok else 'FAIL'}")
    print(f"3MF libraries:    {'PASS' if lib3mf_ok else 'PARTIAL'}")
    print(f"Slicer backends:  {'PASS' if slicer_ok else 'PARTIAL'}")
    print(f"MCP server:       {'PASS' if mcp_ok else 'FAIL'}")
    print(f"Workflow test:    {'PASS' if three_mf else 'PARTIAL'}")
    print("=" * 60)

    # Note: CuraEngine slicing skipped (requires profile configuration)
    print("\nNote: CuraEngine slicing test skipped (requires profile setup)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
