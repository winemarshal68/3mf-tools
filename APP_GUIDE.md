# 🎨 Visual Web App - No Coding Required!

## Quick Start

### 1. Launch the App

```bash
cd ~/3d-workflows/3mf_tools
source activate.sh
python app.py
```

The app will open in your web browser at: **http://127.0.0.1:7860**

### 2. Use the Interface

The app has **4 tabs**, each with visual previews:

#### 🔨 Repair Tab
1. Upload a broken STL file
2. Choose repair method (MeshFix or Quick)
3. Click "Repair Mesh"
4. See **before/after** images side-by-side
5. Download the repaired file

#### 🔄 Convert Tab
1. Upload any mesh file
2. Select output format (STL, OBJ, 3MF, etc.)
3. Click "Convert"
4. Preview the mesh
5. Download converted file

#### ↔️ Transform Tab
1. Upload a mesh
2. Use **sliders** to:
   - Scale (0.1x to 10x)
   - Rotate (X, Y, Z axes)
   - Translate (move in 3D space)
3. See live before/after preview
4. Download transformed mesh

#### ➕ Boolean Tab
1. Upload two meshes (A and B)
2. Choose operation:
   - **Union** - Combine meshes
   - **Difference** - Subtract B from A
   - **Intersection** - Keep only overlapping parts
3. See all three meshes previewed
4. Download result

---

## Features

### ✅ No Coding Required
- Everything is point-and-click
- Drag & drop files
- Visual sliders for adjustments
- Instant previews

### 📸 Visual Feedback
- Before/after comparisons
- 3D mesh previews
- Statistics (vertices, faces, volume)
- Quality indicators (watertight status)

### 🚀 Fast & Local
- Runs on your computer
- No internet required (except first install)
- Private - your files never leave your machine
- Multi-core processing

### 📊 Detailed Stats
For each mesh, see:
- Vertex/face/edge counts
- Watertight status
- Volume and surface area
- Bounding box dimensions
- Physical size in mm

---

## Advanced Features

### Share with Others (Optional)

Edit `app.py` and change:
```python
app.launch(share=True)  # Creates public URL
```

Now anyone can access your tool temporarily via a Gradio link!

### Custom Port

```python
app.launch(server_port=8080)  # Use different port
```

### Auto-Open Browser

The app automatically opens your default browser. If not:
- Manually visit: http://127.0.0.1:7860

---

## Integration with Your Workflow

### Save to CAD-MASTER Directories

After processing in the app:
1. Download the file
2. Move to your project structure:
   - `~/3d-design-projects/stl/` - Source files
   - `~/3d-design-projects/slices/` - Processed files ready to print

### Send to Bambu Lab Printer

After converting to 3MF in the app:
1. Download the .3mf file
2. Use Bambu Lab MCP to send directly to P1S/P2S
3. Or use Bambu Studio to slice and print

---

## Keyboard Shortcuts

- **Ctrl+C** in terminal - Stop the app
- **Ctrl+Shift+R** in browser - Refresh if stuck
- **Cmd+Tab** (Mac) - Switch between terminal and browser

---

## Troubleshooting

### App Won't Start

```bash
# Reinstall Gradio
source venv/bin/activate
pip install --upgrade gradio
python app.py
```

### Port Already in Use

```bash
# Use different port
python app.py --server-port 7861
```

### Preview Images Not Loading

- Large meshes may take a few seconds to render
- Try with a simpler mesh first
- Check terminal for error messages

### MeshFix Not Working

- Ensure MeshFix is built: `ls -la bin/meshfix`
- Use "Quick Repair" option instead
- See main README for MeshFix troubleshooting

---

## What You Can Do (No Code!)

### Example Workflows

**Fix a Downloaded STL:**
1. Download broken STL from Thingiverse
2. Open app → Repair tab
3. Upload file, click "Repair"
4. See quality improvement in preview
5. Download fixed file
6. Print!

**Scale a Model:**
1. Open app → Transform tab
2. Upload model
3. Move "Scale" slider (e.g., 2.0 for 200% size)
4. See updated preview
5. Download scaled model

**Combine Two Parts:**
1. Open app → Boolean tab
2. Upload base part and insert
3. Choose "Union"
4. Preview the combination
5. Download merged model

**Batch Convert Directory:**
1. Use Convert tab
2. Upload each file one by one
3. Convert to 3MF
4. Download all
5. Ready for Bambu Lab!

---

## Future Enhancements (Easy to Add)

Want more features? These are simple additions:

### Batch Processing Tab
- Upload multiple files at once
- Process all in parallel
- Download as ZIP

### Printer Integration Tab
- Connect to Bambu Lab MCP directly
- Send files to printer from app
- Monitor print status

### Settings Tab
- Save favorite parameters
- Custom output directories
- Material profiles

### Preview Enhancements
- Rotate 3D preview with mouse
- Measurement tools
- Cross-section views

---

## Why This Approach?

### ✅ Pros
- **No coding** - Just Python app, runs itself
- **Visual** - See everything before downloading
- **Fast** - Local processing, instant feedback
- **Safe** - Your files stay on your computer
- **Flexible** - Easy to add new features
- **Professional** - Clean, modern interface

### Alternatives Compared

| Feature | Gradio App | Command Line | Desktop App | Web Service |
|---------|------------|--------------|-------------|-------------|
| Visual Preview | ✅ | ❌ | ✅ | ✅ |
| No Coding | ✅ | ❌ | ⚠️ | ✅ |
| Works Offline | ✅ | ✅ | ✅ | ❌ |
| Easy Setup | ✅ | ✅ | ⚠️ | ✅ |
| Customizable | ✅ | ⚠️ | ⚠️ | ❌ |
| File Privacy | ✅ | ✅ | ✅ | ❌ |

---

## Getting Help

**App won't start?**
```bash
python app.py 2>&1 | tee app.log
# Check app.log for errors
```

**Need to add a feature?**
- The app code is in `app.py`
- Each tab is its own function
- Gradio documentation: https://gradio.app/docs

**Want a different design?**
- Gradio themes: `gr.themes.Soft()`, `gr.themes.Monochrome()`, `gr.themes.Glass()`
- Change in `app.py` line with `gr.Blocks(theme=...)`

---

## Next Steps

1. **Try it now:** `python app.py`
2. **Process a file** through each tab
3. **Integrate with CAD-MASTER** - Save outputs to your project dirs
4. **Connect to printers** - Use processed files with Bambu Lab MCP

**Your 3D printing workflow is now point-and-click!** 🎉
