# 🚀 Quick Start - Visual App

## ✅ FIXED: Connection Refused Issue

The app now works correctly with Gradio 6.x!

---

## Launch the Visual App (3 Easy Ways)

### Method 1: Simple Launch (Recommended)

```bash
cd ~/3d-workflows/3mf_tools
source activate.sh
python app.py
```

**What happens:**
- App starts automatically
- Browser opens to http://127.0.0.1:7860 (or next available port)
- You see the full interface with 4 tabs

---

### Method 2: Using the Launcher Script

```bash
cd ~/3d-workflows/3mf_tools
./launch_app.sh
```

This wrapper script:
- Checks dependencies
- Finds available port automatically
- Provides status messages

---

### Method 3: Quick Test First

```bash
cd ~/3d-workflows/3mf_tools
source activate.sh
python test_app.py
```

**Simple test interface** - if this works, the main app will work!

---

## 📱 Using the App

Once launched, you'll see **4 tabs**:

### 🔨 Repair Tab
1. Click "Upload STL/OBJ"
2. Select your file
3. Check "Use MeshFix" for better quality
4. Click "Repair Mesh"
5. See before/after images
6. Click "Download Repaired Mesh"

### 🔄 Convert Tab
1. Upload any mesh file
2. Choose output format (STL, OBJ, PLY, 3MF)
3. Click "Convert"
4. Download converted file

### ↔️ Transform Tab
1. Upload mesh
2. **Drag sliders** to:
   - Scale (make bigger/smaller)
   - Rotate (any axis)
   - Move (translate)
3. See live preview
4. Download transformed mesh

### ➕ Boolean Tab
1. Upload two meshes (A and B)
2. Choose operation:
   - Union (combine)
   - Difference (subtract)
   - Intersection (overlap only)
3. Download result

---

## 🔧 Troubleshooting

### Port Already in Use?

If 7860 is busy, Gradio automatically tries the next port (7861, 7862, etc.)

Check the terminal output for: `Running on local URL:  http://127.0.0.1:XXXX`

### Browser Didn't Open?

Manually visit: **http://127.0.0.1:7860**

Or check terminal for the actual URL

### App Won't Start?

```bash
# Reinstall Gradio
source venv/bin/activate
pip install --upgrade gradio
python app.py
```

### "Connection Refused" Error?

**Already fixed!** Pull latest changes:
```bash
git pull
```

The fix updates Gradio parameters for v6.x compatibility.

---

## 🎯 Quick Demo Workflow

Try this to test everything:

1. **Launch app:**
   ```bash
   cd ~/3d-workflows/3mf_tools
   source activate.sh
   python app.py
   ```

2. **Use test file:**
   - Go to Repair tab
   - Upload `test_cube.stl` (created by self_test.py)
   - Click "Repair Mesh"
   - See the before/after preview

3. **Try conversion:**
   - Go to Convert tab
   - Upload the same file
   - Choose "3mf" format
   - Download result

4. **Test transformation:**
   - Go to Transform tab
   - Upload file
   - Drag "Scale" slider to 2.0
   - See it double in size!

---

## 💡 Pro Tips

### Keep App Running

Leave the app running in one terminal window while you work.
Open new terminal for other commands.

### Share with Others (Optional)

Edit `app.py` line 368:
```python
app.launch(share=True)  # Creates public URL
```

### Integration with Workflow

After processing in app:
1. Download file
2. Move to `~/3d-design-projects/slices/`
3. Send to Bambu Lab printer via MCP

### Use Both CLI and GUI

- **GUI:** Great for individual files, visual verification
- **CLI:** Better for batch processing, automation

---

## 📊 What You'll See

### Interface Layout

```
╔══════════════════════════════════════════╗
║  3MF Tools - Visual Mesh Processing      ║
╠════════╤════════╤════════╤═══════════════╣
║ Repair │Convert│Transform│Boolean Ops   ║ ← Tabs
╠════════╧════════╧════════╧═══════════════╣
║                                          ║
║  [Upload File] [  Button  ]              ║
║                                          ║
║  ┌──────────┐  ┌──────────┐             ║
║  │ Before   │  │ After    │             ║ ← Previews
║  │  Image   │  │  Image   │             ║
║  └──────────┘  └──────────┘             ║
║                                          ║
║  📊 Statistics:                          ║
║  Vertices: 1,234                         ║
║  Watertight: ✅                          ║
║                                          ║
║  [Download Result]                       ║
║                                          ║
╚══════════════════════════════════════════╝
```

---

## ✅ Checklist

Before using, make sure:
- [x] Virtual environment created (`venv/` exists)
- [x] Gradio installed (`pip list | grep gradio`)
- [x] In correct directory (`~/3d-workflows/3mf_tools`)
- [x] Environment activated (`source activate.sh`)
- [x] App started (`python app.py`)
- [x] Browser opened to http://127.0.0.1:7860

---

## 🎉 Success Indicators

**App is working when you see:**
```
Starting test app...
Running on local URL:  http://127.0.0.1:7860

To create a public link, set `share=True` in `launch()`.
```

**In browser, you should see:**
- Clean white/gray interface
- "3MF Tools - Visual Mesh Processing" title
- Four tabs across the top
- Upload file button visible

---

## Need Help?

**Quick checks:**
```bash
# Check if app is running
lsof -i :7860

# View app logs
source venv/bin/activate
python app.py 2>&1 | tee app.log

# Test minimal version
python test_app.py
```

**Still stuck?**
1. Check [APP_GUIDE.md](APP_GUIDE.md) for detailed documentation
2. Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for solutions
3. Open an issue on GitHub

---

**You're ready to use the visual interface!** 🎨
