#!/Users/marshalwalkerm4mini/3d-workflows/3mf_tools/venv/bin/python
"""
Example: Batch processing workflows
"""

import sys
from pathlib import Path
from multiprocessing import Pool, cpu_count
import trimesh

def process_single_repair(input_file):
    """Repair a single mesh"""
    try:
        mesh = trimesh.load(str(input_file))

        # Basic repair
        mesh.remove_duplicate_faces()
        mesh.remove_degenerate_faces()
        mesh.fix_normals()
        mesh.fill_holes()

        # Output
        output_file = Path("repaired") / input_file.name
        output_file.parent.mkdir(exist_ok=True)
        mesh.export(str(output_file))

        return f"✓ {input_file.name}"
    except Exception as e:
        return f"✗ {input_file.name}: {e}"


def process_single_simplify(args):
    """Simplify a single mesh"""
    input_file, target_percent = args

    try:
        mesh = trimesh.load(str(input_file))
        original_faces = len(mesh.faces)

        # Simplify
        target_faces = int(original_faces * target_percent / 100)
        simplified = mesh.simplify_quadratic_decimation(target_faces)

        # Output
        output_file = Path("simplified") / input_file.name
        output_file.parent.mkdir(exist_ok=True)
        simplified.export(str(output_file))

        reduction = ((original_faces - len(simplified.faces)) / original_faces * 100)
        return f"✓ {input_file.name}: {original_faces} → {len(simplified.faces)} faces ({reduction:.1f}% reduction)"
    except Exception as e:
        return f"✗ {input_file.name}: {e}"


def batch_repair(input_dir, parallel=True, workers=None):
    """Repair all meshes in directory"""
    input_path = Path(input_dir)
    mesh_files = list(input_path.glob("*.stl")) + list(input_path.glob("*.obj"))

    if not mesh_files:
        print(f"No mesh files found in {input_dir}")
        return

    print(f"Found {len(mesh_files)} meshes to repair")
    print(f"Mode: {'Parallel' if parallel else 'Sequential'}")
    print("")

    if parallel:
        if workers is None:
            workers = min(cpu_count(), len(mesh_files))

        print(f"Using {workers} workers")
        with Pool(workers) as pool:
            results = pool.map(process_single_repair, mesh_files)
    else:
        results = [process_single_repair(f) for f in mesh_files]

    # Print results
    print("\nResults:")
    for result in results:
        print(f"  {result}")

    success_count = sum(1 for r in results if r.startswith("✓"))
    print(f"\n✓ Complete: {success_count}/{len(mesh_files)} successful")


def batch_simplify(input_dir, target_percent=50, parallel=True, workers=None):
    """Simplify all meshes in directory"""
    input_path = Path(input_dir)
    mesh_files = list(input_path.glob("*.stl")) + list(input_path.glob("*.obj"))

    if not mesh_files:
        print(f"No mesh files found in {input_dir}")
        return

    print(f"Found {len(mesh_files)} meshes to simplify")
    print(f"Target: {target_percent}% of original faces")
    print(f"Mode: {'Parallel' if parallel else 'Sequential'}")
    print("")

    args = [(f, target_percent) for f in mesh_files]

    if parallel:
        if workers is None:
            workers = min(cpu_count(), len(mesh_files))

        print(f"Using {workers} workers")
        with Pool(workers) as pool:
            results = pool.map(process_single_simplify, args)
    else:
        results = [process_single_simplify(a) for a in args]

    # Print results
    print("\nResults:")
    for result in results:
        print(f"  {result}")

    success_count = sum(1 for r in results if r.startswith("✓"))
    print(f"\n✓ Complete: {success_count}/{len(mesh_files)} successful")


def batch_convert(input_dir, output_format, parallel=True):
    """Convert all meshes to specified format"""
    input_path = Path(input_dir)
    output_dir = Path(f"converted_{output_format}")
    output_dir.mkdir(exist_ok=True)

    # Find all mesh files
    extensions = ['.stl', '.obj', '.ply', '.off', '.3mf']
    mesh_files = []
    for ext in extensions:
        mesh_files.extend(input_path.glob(f"*{ext}"))

    if not mesh_files:
        print(f"No mesh files found in {input_dir}")
        return

    print(f"Converting {len(mesh_files)} files to {output_format}")

    def convert_file(input_file):
        try:
            mesh = trimesh.load(str(input_file))
            output_file = output_dir / f"{input_file.stem}.{output_format}"
            mesh.export(str(output_file))
            return f"✓ {input_file.name}"
        except Exception as e:
            return f"✗ {input_file.name}: {e}"

    if parallel:
        with Pool(cpu_count()) as pool:
            results = pool.map(convert_file, mesh_files)
    else:
        results = [convert_file(f) for f in mesh_files]

    # Print results
    for result in results:
        print(f"  {result}")

    success_count = sum(1 for r in results if r.startswith("✓"))
    print(f"\n✓ Complete: {success_count}/{len(mesh_files)} converted")


def batch_validate(input_dir):
    """Validate all meshes and report issues"""
    input_path = Path(input_dir)
    mesh_files = list(input_path.glob("*.stl")) + list(input_path.glob("*.obj"))

    if not mesh_files:
        print(f"No mesh files found in {input_dir}")
        return

    print(f"Validating {len(mesh_files)} meshes\n")

    issues = []

    for mesh_file in mesh_files:
        try:
            mesh = trimesh.load(str(mesh_file))

            file_issues = []
            if not mesh.is_watertight:
                file_issues.append("not watertight")
            if len(mesh.vertices) != len(mesh.unique_vertices):
                dupes = len(mesh.vertices) - len(mesh.unique_vertices)
                file_issues.append(f"{dupes} duplicate vertices")
            if not mesh.is_winding_consistent:
                file_issues.append("inconsistent winding")

            if file_issues:
                print(f"✗ {mesh_file.name}")
                for issue in file_issues:
                    print(f"    - {issue}")
                issues.append((mesh_file.name, file_issues))
            else:
                print(f"✓ {mesh_file.name}")

        except Exception as e:
            print(f"✗ {mesh_file.name}: {e}")
            issues.append((mesh_file.name, [str(e)]))

    print(f"\n{'='*50}")
    print(f"Summary: {len(mesh_files) - len(issues)}/{len(mesh_files)} valid")

    if issues:
        print(f"\nFiles with issues:")
        for filename, file_issues in issues:
            print(f"  {filename}: {', '.join(file_issues)}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Repair:    batch_process.py repair <input_dir> [--parallel] [--workers N]")
        print("  Simplify:  batch_process.py simplify <input_dir> [--percent N] [--parallel]")
        print("  Convert:   batch_process.py convert <input_dir> <format> [--parallel]")
        print("  Validate:  batch_process.py validate <input_dir>")
        print("\nFormats: stl, obj, ply, off, 3mf")
        sys.exit(1)

    command = sys.argv[1]
    input_dir = sys.argv[2]

    # Parse options
    parallel = "--parallel" in sys.argv or "-p" in sys.argv
    workers = None
    if "--workers" in sys.argv:
        idx = sys.argv.index("--workers")
        workers = int(sys.argv[idx + 1])

    if command == "repair":
        batch_repair(input_dir, parallel, workers)

    elif command == "simplify":
        percent = 50
        if "--percent" in sys.argv:
            idx = sys.argv.index("--percent")
            percent = int(sys.argv[idx + 1])
        batch_simplify(input_dir, percent, parallel, workers)

    elif command == "convert":
        if len(sys.argv) < 4:
            print("Error: Output format required")
            sys.exit(1)
        output_format = sys.argv[3]
        batch_convert(input_dir, output_format, parallel)

    elif command == "validate":
        batch_validate(input_dir)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
