# 🎮 RimWorld Modlist Generator

Easily create RimWorld modlists from Steam Workshop collections with a beautiful GUI.

---

## ⚡ Quick Start (Recommended - Use the Release)

### 1. Download the Release
👉 **[Download the latest release](../../releases/latest)** - Includes a ready-to-use executable!

No installation needed - just extract and run `gui.exe` on Windows, or the bundled app on macOS/Linux.

### 2. Run the GUI
Double-click the application to launch the GUI.

### 3. Follow the On-Screen Instructions
The GUI will guide you through:
- Fetching Steam Workshop collections
- Generating modlist XML files
- Merging collections
- And more!

---

## 💻 Alternative: Run From Source (Developers)

If you prefer to run from source code:

### 1. Install Python 3.13+
Download from [python.org](https://www.python.org/downloads/)

### 2. Install Dependencies
```bash
pip install requests beautifulsoup4 dearpygui
```

### 3. Run the GUI
```bash
./gui.py
```

Or on Windows:
```cmd
python gui.py
```

---

## ✨ What It Does

- 📥 **Fetch Collections** - Download all mod IDs from Steam Workshop collections
- 🔄 **Generate XML** - Create modlist files for RimWorld
- 🔗 **Merge Lists** - Combine multiple collections
- ✂️ **Remove Mods** - Exclude specific mods from a collection
- 🎯 **No Downloads Needed** - Works instantly (no need to download all mods)
- 🖥️ **Beautiful GUI** - Easy point-and-click interface

---

## 📋 Using the GUI

The GUI has 5 tabs:

1. **📥 Create from Collection**
   - Paste a Steam Workshop collection URL or ID
   - Download all mod IDs instantly

2. **🔄 Convert to XML**
   - Select a mod list
   - Generate RimWorld-compatible XML
   - Save to your mod manager

3. **🔗 Merge Lists**
   - Combine multiple collections
   - Automatically removes duplicates

4. **✂️ Remove Mods**
   - Remove specific mods from a list
   - Perfect for excluding incompatible mods

5. **⚙️ Settings**
   - Customize paths
   - Adjust RimWorld version
   - Configure expansions

---

## 🔍 Finding Steam Collections

1. Go to [Steam Workshop - RimWorld](https://steamcommunity.com/app/294100/collections/)
2. Find a collection you like
3. Copy the collection ID from the URL:
   ```
   https://steamcommunity.com/sharedfiles/filedetails/?id=3187121098
                                                            ^^^^^^^^^^^
   This is the collection ID
   ```
4. Paste it into the GUI!

---

## FAQ

**Q: Do I need to download all the mods?**
A: Yes and no.The tool can create a ID List from simply the steam collection url, but creates modlists using the mod's `About.xml`, so you can manage ID lists without, but you need all the mods to get a working Rimsort list.

**Q: What file format does it create?**
A: RimWorld ModsConfigData XML format - compatible with RimSort.

**Q: Can I combine multiple collections?**
A: Yes! Use the "Merge Lists" tab to combine collections.

**Q: Can I remove specific mods?**
A: Yes! Use the "Remove Mods" tab.

**Q: Does this work offline?**
A: The collection fetching needs internet. Once you have a list, XML generation works offline.

**Q: Where and how are the ID list stored?**
A: In the `rwpackageId_database/` folder, in a `.rwpackageId` file (a simple text file)

---

## 🐛 Troubleshooting

**"Collection not found"**
- Make sure the collection is public (not private)
- Check that the collection URL/ID is correct
- Try copying the link directly from your browser

**"No files found"**
- You need to fetch a collection first
- Use the "Create from Collection" tab

**On Windows - "gui.exe won't run"**
- Try right-clicking → "Run as administrator"
- Make sure your antivirus allows it
- Try downloading again if corrupted

**On Mac/Linux - "Permission denied"**
- Make sure the app is executable: `chmod +x gui.py`
- Try running with Python: `python3 gui.py`

---

## 📄 License

MIT License - Free to use and modify

---

## 🤝 Issues or Feedback?

Found a bug? Have a feature request? Open an issue on GitHub!

---

**Ready to organize your mods? [Download the latest release!](../../releases/latest)** 🚀
