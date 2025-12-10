#!/Users/marshalwalkerm4mini/3d-workflows/3mf_tools/venv/bin/python
"""
3MF Tools Web UI - No coding required!

A visual interface for mesh processing with live previews.
"""

import gradio as gr
import trimesh
import numpy as np
from pathlib import Path
import tempfile
import subprocess
from PIL import Image
import io

# Tool directories
TOOLS_DIR = Path(__file__).parent
BIN_DIR = TOOLS_DIR / "bin"

def generate_preview(mesh, resolution=(800, 600)):
    """Generate a preview image of the mesh"""
    try:
        scene = mesh.scene()

        # Set up nice camera angle
        scene.camera.resolution = resolution
        scene.camera.fov = (60, 45)

        # Render to PNG bytes
        png_bytes = scene.save_image(resolution=resolution)

        # Convert to PIL Image
        image = Image.open(io.BytesIO(png_bytes))
        return image
    except Exception as e:
        # Return error image
        img = Image.new('RGB', resolution, color='red')
        return img


def mesh_stats(mesh):
    """Get mesh statistics as formatted text"""
    stats = f"""
📊 **Mesh Statistics**

**Geometry:**
- Vertices: {len(mesh.vertices):,}
- Faces: {len(mesh.faces):,}
- Edges: {len(mesh.edges):,}

**Quality:**
- Watertight: {"✅ Yes" if mesh.is_watertight else "❌ No"}
- Volume: {mesh.volume:.2f} mm³
- Surface Area: {mesh.area:.2f} mm²

**Bounds:**
- X: {mesh.bounds[0][0]:.2f} to {mesh.bounds[1][0]:.2f} mm
- Y: {mesh.bounds[0][1]:.2f} to {mesh.bounds[1][1]:.2f} mm
- Z: {mesh.bounds[0][2]:.2f} to {mesh.bounds[1][2]:.2f} mm

**Size:** {mesh.bounds[1][0] - mesh.bounds[0][0]:.1f} × {mesh.bounds[1][1] - mesh.bounds[0][1]:.1f} × {mesh.bounds[1][2] - mesh.bounds[0][2]:.1f} mm
"""
    return stats


def repair_mesh_ui(input_file, use_meshfix=True):
    """Repair mesh with preview"""
    if input_file is None:
        return None, None, "Please upload a file first"

    try:
        # Load mesh
        mesh = trimesh.load(input_file.name)
        original_stats = mesh_stats(mesh)
        before_image = generate_preview(mesh)

        # Repair
        if use_meshfix:
            # Use MeshFix for heavy repair
            meshfix_bin = BIN_DIR / "meshfix"
            temp_out = tempfile.NamedTemporaryFile(suffix='.off', delete=False)

            result = subprocess.run(
                [str(meshfix_bin), input_file.name],
                capture_output=True,
                timeout=60
            )

            # Load repaired mesh (MeshFix outputs .off)
            off_file = input_file.name.replace('.stl', '_fixed.off')
            if Path(off_file).exists():
                mesh = trimesh.load(off_file)
                Path(off_file).unlink()  # Clean up
        else:
            # Quick repair
            mesh.remove_duplicate_faces()
            mesh.remove_degenerate_faces()
            mesh.fix_normals()
            mesh.fill_holes()
            mesh.merge_vertices()

        # Generate preview
        after_image = generate_preview(mesh)
        repaired_stats = mesh_stats(mesh)

        # Save repaired mesh
        output_file = tempfile.NamedTemporaryFile(suffix='.stl', delete=False)
        mesh.export(output_file.name)

        return (
            before_image,
            after_image,
            f"## Original\n{original_stats}\n\n## Repaired\n{repaired_stats}",
            output_file.name
        )

    except Exception as e:
        return None, None, f"❌ Error: {str(e)}", None


def convert_format_ui(input_file, output_format):
    """Convert mesh format with preview"""
    if input_file is None:
        return None, None, "Please upload a file first"

    try:
        mesh = trimesh.load(input_file.name)
        preview = generate_preview(mesh)
        stats = mesh_stats(mesh)

        # Convert
        output_file = tempfile.NamedTemporaryFile(suffix=f'.{output_format}', delete=False)
        mesh.export(output_file.name)

        return preview, stats, output_file.name

    except Exception as e:
        return None, f"❌ Error: {str(e)}", None


def transform_mesh_ui(input_file, scale, rotate_x, rotate_y, rotate_z, translate_x, translate_y, translate_z):
    """Transform mesh with live preview"""
    if input_file is None:
        return None, None, "Please upload a file first"

    try:
        mesh = trimesh.load(input_file.name)
        original_preview = generate_preview(mesh)

        # Apply transformations
        if scale != 1.0:
            mesh.apply_scale(scale)

        if rotate_x != 0:
            mesh.apply_transform(trimesh.transformations.rotation_matrix(
                np.radians(rotate_x), [1, 0, 0]
            ))
        if rotate_y != 0:
            mesh.apply_transform(trimesh.transformations.rotation_matrix(
                np.radians(rotate_y), [0, 1, 0]
            ))
        if rotate_z != 0:
            mesh.apply_transform(trimesh.transformations.rotation_matrix(
                np.radians(rotate_z), [0, 0, 1]
            ))

        if translate_x != 0 or translate_y != 0 or translate_z != 0:
            mesh.apply_translation([translate_x, translate_y, translate_z])

        transformed_preview = generate_preview(mesh)
        stats = mesh_stats(mesh)

        # Save
        output_file = tempfile.NamedTemporaryFile(suffix='.stl', delete=False)
        mesh.export(output_file.name)

        return original_preview, transformed_preview, stats, output_file.name

    except Exception as e:
        return None, None, f"❌ Error: {str(e)}", None


def boolean_operation_ui(mesh_a_file, mesh_b_file, operation):
    """Boolean operations with preview"""
    if mesh_a_file is None or mesh_b_file is None:
        return None, None, None, "Please upload both files"

    try:
        mesh_a = trimesh.load(mesh_a_file.name)
        mesh_b = trimesh.load(mesh_b_file.name)

        preview_a = generate_preview(mesh_a)
        preview_b = generate_preview(mesh_b)

        # Perform boolean
        if operation == "Union":
            result = mesh_a.union(mesh_b)
        elif operation == "Difference":
            result = mesh_a.difference(mesh_b)
        elif operation == "Intersection":
            result = mesh_a.intersection(mesh_b)

        result_preview = generate_preview(result)
        stats = mesh_stats(result)

        # Save
        output_file = tempfile.NamedTemporaryFile(suffix='.stl', delete=False)
        result.export(output_file.name)

        return preview_a, preview_b, result_preview, stats, output_file.name

    except Exception as e:
        return None, None, None, f"❌ Error: {str(e)}", None


# Create Gradio Interface
with gr.Blocks(title="3MF Tools - Visual Mesh Processing", theme=gr.themes.Soft()) as app:

    gr.Markdown("""
    # 🔧 3MF Tools - Visual Mesh Processing

    No coding required! Upload, preview, process, and download your 3D meshes.
    """)

    with gr.Tabs():
        # Tab 1: Mesh Repair
        with gr.Tab("🔨 Repair"):
            gr.Markdown("## Repair broken meshes with visual comparison")

            with gr.Row():
                with gr.Column():
                    repair_input = gr.File(label="Upload STL/OBJ", file_types=['.stl', '.obj', '.ply'])
                    use_meshfix = gr.Checkbox(label="Use MeshFix (slower, better quality)", value=True)
                    repair_btn = gr.Button("Repair Mesh", variant="primary")

                with gr.Column():
                    repair_stats = gr.Markdown()
                    repair_output = gr.File(label="Download Repaired Mesh")

            with gr.Row():
                repair_before = gr.Image(label="Before")
                repair_after = gr.Image(label="After")

            repair_btn.click(
                repair_mesh_ui,
                inputs=[repair_input, use_meshfix],
                outputs=[repair_before, repair_after, repair_stats, repair_output]
            )

        # Tab 2: Format Conversion
        with gr.Tab("🔄 Convert"):
            gr.Markdown("## Convert between mesh formats")

            with gr.Row():
                with gr.Column():
                    convert_input = gr.File(label="Upload Mesh", file_types=['.stl', '.obj', '.ply', '.off'])
                    convert_format = gr.Dropdown(
                        choices=["stl", "obj", "ply", "off", "3mf"],
                        label="Output Format",
                        value="3mf"
                    )
                    convert_btn = gr.Button("Convert", variant="primary")

                with gr.Column():
                    convert_preview = gr.Image(label="Preview")
                    convert_stats = gr.Markdown()
                    convert_output = gr.File(label="Download Converted")

            convert_btn.click(
                convert_format_ui,
                inputs=[convert_input, convert_format],
                outputs=[convert_preview, convert_stats, convert_output]
            )

        # Tab 3: Transform
        with gr.Tab("↔️ Transform"):
            gr.Markdown("## Scale, rotate, and move meshes")

            with gr.Row():
                with gr.Column():
                    transform_input = gr.File(label="Upload Mesh", file_types=['.stl', '.obj', '.ply'])

                    gr.Markdown("### Scale")
                    scale_slider = gr.Slider(0.1, 10.0, value=1.0, label="Scale Factor")

                    gr.Markdown("### Rotation (degrees)")
                    rotate_x = gr.Slider(-180, 180, value=0, label="Rotate X")
                    rotate_y = gr.Slider(-180, 180, value=0, label="Rotate Y")
                    rotate_z = gr.Slider(-180, 180, value=0, label="Rotate Z")

                    gr.Markdown("### Translation (mm)")
                    translate_x = gr.Slider(-100, 100, value=0, label="Move X")
                    translate_y = gr.Slider(-100, 100, value=0, label="Move Y")
                    translate_z = gr.Slider(-100, 100, value=0, label="Move Z")

                    transform_btn = gr.Button("Apply Transform", variant="primary")

                with gr.Column():
                    transform_stats = gr.Markdown()
                    transform_output = gr.File(label="Download Transformed")

            with gr.Row():
                transform_before = gr.Image(label="Original")
                transform_after = gr.Image(label="Transformed")

            transform_btn.click(
                transform_mesh_ui,
                inputs=[transform_input, scale_slider, rotate_x, rotate_y, rotate_z,
                       translate_x, translate_y, translate_z],
                outputs=[transform_before, transform_after, transform_stats, transform_output]
            )

        # Tab 4: Boolean Operations
        with gr.Tab("➕ Boolean"):
            gr.Markdown("## Combine or subtract meshes")

            with gr.Row():
                with gr.Column():
                    boolean_a = gr.File(label="Mesh A", file_types=['.stl', '.obj'])
                    boolean_b = gr.File(label="Mesh B", file_types=['.stl', '.obj'])
                    boolean_op = gr.Radio(
                        choices=["Union", "Difference", "Intersection"],
                        label="Operation",
                        value="Union"
                    )
                    boolean_btn = gr.Button("Perform Boolean", variant="primary")

                with gr.Column():
                    boolean_stats = gr.Markdown()
                    boolean_output = gr.File(label="Download Result")

            with gr.Row():
                boolean_preview_a = gr.Image(label="Mesh A")
                boolean_preview_b = gr.Image(label="Mesh B")
                boolean_preview_result = gr.Image(label="Result")

            boolean_btn.click(
                boolean_operation_ui,
                inputs=[boolean_a, boolean_b, boolean_op],
                outputs=[boolean_preview_a, boolean_preview_b, boolean_preview_result,
                        boolean_stats, boolean_output]
            )

    gr.Markdown("""
    ---
    ### 💡 Tips
    - All processing happens locally on your computer
    - Preview images are rendered automatically
    - Download processed files using the buttons
    - Integrates with your Bambu Lab printers via MCP

    **Next Steps:** Use Bambu Lab MCP to send processed files directly to your P1S/P2S printers!
    """)

if __name__ == "__main__":
    # Install gradio if not present
    try:
        import gradio
    except ImportError:
        import subprocess
        subprocess.run(["pip", "install", "gradio"], check=True)
        import gradio as gr

    # Launch app
    # Note: Gradio 6.x automatically handles port selection
    app.launch(
        share=False,  # Set to True to get public URL
        inbrowser=True  # Open browser automatically
    )
