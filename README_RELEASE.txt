RimWorld Modlist Manager - Release v1.0.0
=========================================

QUICK START
-----------
1. Run gui-windows.exe
2. First time: Rename "config.ini.example" to "config.ini" and edit paths
3. Use the GUI to fetch Steam Workshop collections and generate modlists

WHAT'S INCLUDED
---------------
- gui-windows.exe          : The main application (Windows executable)
- config.ini.example       : Configuration template (rename to config.ini)
- rwpackageId_database/    : Folder where collection lists are stored
- README_RELEASE.txt       : This file

FIRST TIME SETUP
----------------
The application will auto-create config.ini on first run if it doesn't exist.
Edit config.ini to:
  - Set your RimWorld mods folder path
  - Customize default settings
  - Configure RimWorld version

HOW TO USE
----------
1. Open gui-windows.exe
2. Go to "Create from Collection" tab
3. Paste a Steam Workshop collection URL or ID
4. Click "Fetch Collection" - creates a .rwpackageId file
5. Go to "Convert to XML" tab
6. Select your collection list
7. Click "Generate XML" - creates modlist for RimWorld

TABS OVERVIEW
-------------
- Create from Collection : Download mod lists from Steam Workshop
- Convert to XML        : Generate RimWorld-compatible modlist XML
- Merge Lists           : Combine multiple collections
- Remove Mods           : Exclude specific mods from a list
- Settings              : Configure paths and preferences

TROUBLESHOOTING
---------------
- No files found? Create a collection first in "Create from Collection" tab
- Can't find mods? Set your RimWorld mods folder in config.ini
- Need help? Check GitHub Issues or documentation

PROJECT
-------
GitHub: https://github.com/MatthieuGA/rimworld-sort-moulinette
License: MIT

Enjoy organizing your RimWorld mods!
