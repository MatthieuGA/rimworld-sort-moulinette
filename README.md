# RimWorld Modlist Generator# RimWorld Modlist Generator# RimWorld Modlist Generator# RimWorld Modlist Generator



A two-program workflow for creating RimWorld modlist XML files from Steam Workshop collections.



## OverviewA two-program workflow for creating RimWorld modlist XML files from Steam Workshop collections.



This tool helps you create RimWorld modlist XML files from Steam Workshop collections:



1. **main.py** - Interactive menu for managing modlists:## OverviewA two-program workflow for creating RimWorld modlist XML files from Steam Workshop collections.A Python script to create RimWorld modlist XML files from Steam Workshop collections.

   - Create ID lists from Steam Workshop collections

   - Convert ID lists to XML (launches moulinette.py)

   - Merge multiple ID lists together

   This tool helps you create RimWorld modlist XML files from Steam Workshop collections:

2. **moulinette.py** - Converts `.rwpackageId` files to modlist XML by cross-referencing with local mod folders



## Requirements

1. **main.py** - Interactive menu for managing modlists:## Overview## Features

- Python 3.x

- Required packages:   - Create ID lists from Steam Workshop collections

  ```bash

  pip install requests beautifulsoup4   - Convert ID lists to XML (launches moulinette.py)

  ```

   - Merge multiple ID lists together

## Configuration

   This tool helps you create RimWorld modlist XML files from Steam Workshop collections:- ✨ Fetch mods directly from Steam Workshop collections

The tool uses a `config.ini` file to customize behavior. On first run, a default configuration file will be created automatically, or you can create one manually:

2. **moulinette.py** - Converts `.rwpackageId` files to modlist XML by cross-referencing with local mod folders

```bash

python3 -c "from config import Config; Config().create_default_config()"- 🔗 Accept collection URLs or just the collection ID

```

## Requirements

### Configuration Options

1. **main.py** - Fetches Steam Workshop collections and saves Workshop IDs to `.rwpackageId` files- 📦 Use Workshop IDs directly (no need to download mods!)

Edit `config.ini` to customize these settings:

- Python 3.x

**[Paths]**

- `database_dir` - Directory where .rwpackageId files are stored (default: `rwpackageId_database`)- Required packages:2. **moulinette.py** - Converts `.rwpackageId` files to modlist XML by cross-referencing with local mod folders- 🎯 Optional: Read actual package IDs from local About.xml files

- `default_mods_dir` - Default directory for RimWorld mods (default: `./mods`)

- `default_output_dir` - Default directory for output XML files (default: `.`)  ```bash



**[RimWorld]**  pip install requests beautifulsoup4- 💾 Generate properly formatted XML files for mod managers

- `default_version` - Default RimWorld version string (default: `1.5.4104 rev415`)

- `include_expansions` - Whether to include expansions by default (default: `true`)  ```

- `expansions` - Comma-separated list of expansion package IDs

## Requirements- 📝 Use collection title as default filename

**[Display]**

- `max_files_listed` - Maximum files to show when listing (default: `20`, use `0` for unlimited)## Quick Start

- `max_warning_lines` - Maximum warning lines for missing mods (default: `10`, use `0` for unlimited)



**[Merge]**

- `default_merged_name` - Default name for merged ID lists (default: `merged_list`)### Interactive Mode (Recommended)



Example configuration:- Python 3.x## Requirements

```ini

[Paths]Simply run main.py without arguments:

database_dir = my_modlists

default_mods_dir = /home/user/.steam/steam/steamapps/workshop/content/294100- Required packages:



[Display]```bash

max_files_listed = 0  # Show all files

max_warning_lines = 5  # Only show first 5 missing mods./main.py  ```bash- Python 3.9+

```

```

## Quick Start

  pip install requests beautifulsoup4- `requests` library

### Interactive Mode (Recommended)

You'll see a menu with three options:

Simply run main.py without arguments:

  ```- `beautifulsoup4` library

```bash

./main.py1. **Create ID list from Steam collection** - Fetch Workshop IDs from a Steam collection

```

2. **Convert ID list to RimSort list** - Convert a .rwpackageId file to XML

You'll see a menu with three options:

3. **Merge ID lists together** - Combine multiple .rwpackageId files (removes duplicates)

1. **Create ID list from Steam collection** - Fetch Workshop IDs from a Steam collection

2. **Convert ID list to RimSort list** - Convert a .rwpackageId file to XML## Quick Start### Installation

3. **Merge ID lists together** - Combine multiple .rwpackageId files (removes duplicates)

### Command-Line Mode

### Command-Line Mode



```bash

# Fetch a collection with custom name```bash

./main.py -c 3187121098 -o mymodlist

# Fetch a collection with custom name### 1. Fetch a Collection```bash

# Or auto-name from collection title

./main.py -c 3187121098./main.py -c 3187121098 -o mymodlist

```

pip install requests beautifulsoup4

Files are automatically saved to the database directory (configured in `config.ini`).

# Or auto-name from collection title

## Program Details

./main.py -c 3187121098```bash```

### main.py - Modlist Manager (Interactive Menu)

```

The main entry point with an interactive menu system.

# Fetch a collection and save with custom name

**Interactive Mode:**

```bashFiles are automatically saved to `rwpackageId_database/` with `.rwpackageId` extension.

./main.py

```./main.py -c 3187121098 -o mymodlistOr on most Linux systems, these may already be installed via your package manager.



Menu options:## Program Details

1. **Create ID list from Steam collection** - Fetches Workshop IDs and saves to database

2. **Convert ID list to RimSort list** - Launches moulinette.py to convert to XML

3. **Merge ID lists together** - Combines multiple .rwpackageId files, removing duplicates

### main.py - Modlist Manager (Interactive Menu)

**Command-Line Mode:**

```bash# Or auto-name from collection title## Usage

./main.py -c <collection_id_or_url> [-o <output_name>]

```The main entry point with an interactive menu system.



**Arguments:**./main.py -c 3187121098

- `-c, --collection` - Steam Workshop collection URL or ID

- `-o, --output` - Output name (without extension, optional - defaults to collection title)**Interactive Mode:**



**Examples:**```bash```### Quick Start

```bash

# Interactive mode./main.py

./main.py

```

# Command-line: From collection ID with custom name

./main.py -c 3187121098 -o progression_pack



# Command-line: From full URL (auto-named)Menu options:Files are automatically saved to `rwpackageId_database/` with `.rwpackageId` extension.**Simplest way - from collection ID:**

./main.py -c "https://steamcommunity.com/sharedfiles/filedetails/?id=3187121098"

```1. **Create ID list from Steam collection** - Fetches Workshop IDs and saves to database



**Output:**2. **Convert ID list to RimSort list** - Launches moulinette.py to convert to XML

- Creates `.rwpackageId` file in database directory (see `config.ini`)

- File contains numeric Workshop IDs, one per line3. **Merge ID lists together** - Combines multiple .rwpackageId files, removing duplicates

- Comments (lines starting with `#`) are supported

### 2. Convert to XML```bash

### moulinette.py - XML Generator

**Command-Line Mode:**

Converts `.rwpackageId` files to RimWorld modlist XML.

```bash./main.py -c 3187121098

**Interactive Mode:**

```bash./main.py -c <collection_id_or_url> [-o <output_name>]

./moulinette.py

``````#### Interactive Mode (Recommended)```



**Command-Line Mode:**

```bash

./moulinette.py -i <input> -d <mods_dir> [-o <output>] [-v <version>] [--no-expansions]**Arguments:**```bash

```

- `-c, --collection` - Steam Workshop collection URL or ID

**Arguments:**

- `-i, --input` - Input `.rwpackageId` file name or path (omit for interactive mode)- `-o, --output` - Output name (without extension, optional - defaults to collection title)./moulinette.pyThis will:

- `-d, --mods-dir` - Path to directory containing mod folders (required in CLI mode)

- `-o, --output` - Output XML file name or path (optional - defaults to input name)

- `-v, --version` - RimWorld version string (optional - uses `config.ini` default)

- `--no-expansions` - Exclude expansions from knownExpansions list**Examples:**```1. Fetch all 900+ mods from the collection



**Examples:**```bash

```bash

# Interactive mode# Interactive mode2. Create a modlist XML with all mods using `steam.workshop.{id}` format

./moulinette.py

./main.py

# Command-line with database lookup

./moulinette.py -i mymodlist -d ./modsThe interactive mode will:3. Save it with the collection's title as the filename



# Command-line with full path and custom output# Command-line: From collection ID with custom name

./moulinette.py -i /path/to/file.rwpackageId -d ./mods -o custom.xml

./main.py -c 3187121098 -o progression_pack- Show you all available `.rwpackageId` files (up to 20)4. **No need to have mods downloaded!**

# With custom version

./moulinette.py -i mymodlist -d ./mods -v "1.4.3641 rev649"



# Without expansions# Command-line: From full URL (auto-named)- Let you select which one to convert

./moulinette.py -i mymodlist -d ./mods --no-expansions

```./main.py -c "https://steamcommunity.com/sharedfiles/filedetails/?id=3187121098"



## File Formats```- Ask if you want to use the default output name or specify a custom one### Command Line Examples



### .rwpackageId Format



Plain text file containing Steam Workshop IDs:**Output:**- Ask for the mods directory path



```- Creates `.rwpackageId` file in `rwpackageId_database/` directory

# RimWorld Steam Workshop Collection

# Collection: The Progression Modpack | (1.5)- File contains numeric Workshop IDs, one per line**From a Steam Workshop collection URL:**

# One Workshop ID per line

# Lines starting with # are comments- Comments (lines starting with `#`) are supported



1508850027#### Command-Line Mode

2009463077

2017538067### moulinette.py - XML Generator

```

```bash```bash

### XML Output Format

Converts `.rwpackageId` files to RimWorld modlist XML.

RimWorld ModsConfigData XML format:

# Use file from database with auto-naming./main.py -c "https://steamcommunity.com/sharedfiles/filedetails/?id=3187121098"

```xml

<?xml version='1.0' encoding='utf-8'?>**Interactive Mode:**

<ModsConfigData>

  <version>1.5.4104 rev415</version>```bash./moulinette.py -i mymodlist -d ./mods```

  <activeMods>

    <li>ludeon.rimworld</li>./moulinette.py

    <li>jaxe.rimhud</li>

    <li>brrainz.harmony</li>```

    <li>steam.workshop.2017538067</li>

    ...

  </activeMods>

  <knownExpansions>**Command-Line Mode:**# With custom output name**With custom output path:**

    <li>ludeon.rimworld</li>

    <li>ludeon.rimworld.royalty</li>```bash

    <li>ludeon.rimworld.ideology</li>

    <li>ludeon.rimworld.biotech</li>./moulinette.py -i <input> -d <mods_dir> [-o <output>] [-v <version>] [--no-expansions]./moulinette.py -i mymodlist -d ./mods -o output.xml

    <li>ludeon.rimworld.anomaly</li>

    <li>ludeon.rimworld.odyssey</li>```

  </knownExpansions>

</ModsConfigData>``````bash

```

**Arguments:**

## How Package ID Conversion Works

- `-i, --input` - Input `.rwpackageId` file name or path (omit for interactive mode)./main.py -c 3187121098 -o "My Awesome Modlist.xml"

The moulinette reads `About/About.xml` files from your local mod folders to get the actual package IDs:

- `-d, --mods-dir` - Path to directory containing mod folders (required in CLI mode)

1. For Workshop ID `1508850027`, it looks in `<mods_dir>/1508850027/About/About.xml`

2. Extracts the `<packageId>` tag (e.g., `jaxe.rimhud`)- `-o, --output` - Output XML file name or path (optional - defaults to input name)## Program Details```

3. Falls back to `steam.workshop.{id}` format if About.xml is not found

- `-v, --version` - RimWorld version string (default: 1.5.4104 rev415)

This means you need to have mods downloaded locally for the best results. Mods without local About.xml files will still work but will use the generic `steam.workshop.{id}` format.

- `--no-expansions` - Exclude expansions from knownExpansions list

## Directory Structure



```

rimworld-sort-moulinette/**Examples:**### main.py - Collection Fetcher**Use local About.xml files (requires mods to be downloaded):**

├── rwpackageId_database/          # Database directory (configurable in config.ini)

│   ├── mymodlist.rwpackageId```bash

│   └── progression.rwpackageId

├── mods/                          # Your RimWorld mods folder# Interactive mode

│   ├── 1508850027/                # Workshop ID folders

│   │   └── About/./moulinette.py

│   │       └── About.xml          # Contains packageId

│   └── 2009463077/Fetches Steam Workshop collections and extracts Workshop IDs.```bash

│       └── About/

│           └── About.xml# Command-line with database lookup

├── config.ini                     # Configuration file (auto-created)

├── main.py                        # Interactive menu & collection fetcher./moulinette.py -i mymodlist -d ./mods./main.py -c 3187121098 --use-local-mods -w "./mods"

├── moulinette.py                  # XML generator

├── steam_workshop.py              # Steam Workshop utilities

├── mod_utils.py                   # Mod conversion utilities

├── utils.py                       # Shared utilities# Command-line with full path and custom output**Usage:**```

└── config.py                      # Configuration loader

```./moulinette.py -i /path/to/file.rwpackageId -d ./mods -o custom.xml



## Common Workflows```bash



### Simple Interactive Workflow (Recommended)# With custom version

```bash

# Run main.py./moulinette.py -i mymodlist -d ./mods -v "1.4.3641 rev649"## Program Details

./main.py



# Select option 1: Create ID list from Steam collection

# Enter collection ID: 3187121098# Without expansions### main.py - Modlist Manager (Interactive Menu)

# Enter name or use default

./moulinette.py -i mymodlist -d ./mods --no-expansions

# Select option 2: Convert ID list to RimSort list

# (This launches moulinette.py interactively)```The main entry point with an interactive menu system.

# Select the file you just created

# Keep default name or enter custom

# Enter mods directory path

## File Formats**Interactive Mode:**

# Select q to quit

``````bash



### Merging Multiple Collections### .rwpackageId Format./main.py

```bash

./main.py```



# Select option 1 to fetch first collectionPlain text file containing Steam Workshop IDs:

# Enter collection ID for first pack

# Name it: pack1Menu options:



# Select option 1 again to fetch second collection  ```1. **Create ID list from Steam collection** - Fetches Workshop IDs and saves to database

# Enter collection ID for second pack

# Name it: pack2# RimWorld Steam Workshop Collection2. **Convert ID list to RimSort list** - Launches moulinette.py to convert to XML



# Select option 3: Merge ID lists together# Collection: The Progression Modpack | (1.5)3. **Merge ID lists together** - Combines multiple .rwpackageId files, removing duplicates

# Select pack1

# Select pack2# One Workshop ID per line

# Name merged file: combined_pack

# Lines starting with # are comments**Command-Line Mode:**

# Select option 2 to convert to XML

# Select combined_pack```bash

```

1508850027./main.py -c <collection_id_or_url> [-o <output_name>]

### Command-Line Workflow

```bash2009463077```

# 1. Fetch collection

./main.py -c 3187121098 -o mypack2017538067



# 2. Convert to XML```**Arguments:**

./moulinette.py -i mypack -d ~/path/to/mods

```- `-c, --collection` - Steam Workshop collection URL or ID



### Multiple Collections (Command-Line)### XML Output Format- `-o, --output` - Output name (without extension, optional - defaults to collection title)

```bash

# Fetch multiple collections

./main.py -c 3187121098 -o progression

./main.py -c 2222222222 -o survivalRimWorld ModsConfigData XML format:**Examples:**

./main.py -c 3333333333 -o magic

```bash

# Use interactive mode to convert any of them

./moulinette.py```xml# Interactive mode

```

<?xml version='1.0' encoding='utf-8'?>./main.py

## Troubleshooting

<ModsConfigData>

### "No .rwpackageId files found"

- Run `main.py` and select option 1 to create collection files  <version>1.5.4104 rev415</version># Command-line: From collection ID with custom name

- Check that the database directory exists (configured in `config.ini`)

  <activeMods>./main.py -c 3187121098 -o progression_pack

### "Could not find About.xml for X mods"

- This is normal if you don't have all mods downloaded locally    <li>ludeon.rimworld</li>

- The tool will use `steam.workshop.{id}` format as fallback

- To get actual package IDs, download the mods to your mods directory    <li>jaxe.rimhud</li># Command-line: From full URL (auto-named)

- Adjust `max_warning_lines` in `config.ini` to control how many warnings are shown

    <li>brrainz.harmony</li>./main.py -c "https://steamcommunity.com/sharedfiles/filedetails/?id=3187121098"

### "Input file not found"

- Make sure the file exists in the database directory or provide full path    <li>steam.workshop.2017538067</li>```

- The `.rwpackageId` extension is added automatically in CLI mode

- Check `database_dir` setting in `config.ini`    ...



### Changing default settings  </activeMods>**Output:**

- Edit `config.ini` to customize:

  - Database directory location  <knownExpansions>- Creates `.rwpackageId` file in `rwpackageId_database/` directory

  - Default mods directory

  - Number of files shown in listings (0 = unlimited)    <li>ludeon.rimworld</li>- File contains numeric Workshop IDs, one per line

  - Number of warning lines (0 = show all)

  - Default RimWorld version and expansions    <li>ludeon.rimworld.royalty</li>- Comments (lines starting with `#`) are supportedWith `--use-local-mods`, the script will:



### Interactive menu not working with piped input    <li>ludeon.rimworld.ideology</li>

- The interactive menu is designed for real user interaction

- For automation, use command-line mode instead:    <li>ludeon.rimworld.biotech</li>```- Read actual package IDs from About.xml files (e.g., `jaxe.rimhud`, `brrainz.harmony`)

  ```bash

  ./main.py -c 3187121098 -o mylist    <li>ludeon.rimworld.anomaly</li>

  ./moulinette.py -i mylist -d ./mods -o output.xml

  ```    <li>ludeon.rimworld.odyssey</li>- Fall back to `steam.workshop.{id}` for mods not found locally



## Features Summary  </knownExpansions>



### main.py Interactive Menu</ModsConfigData>**Arguments:**- Useful if your mod manager needs real package IDs

- ✅ Create ID lists from Steam Workshop collections

- ✅ Launch moulinette.py to convert to XML```

- ✅ Merge multiple ID lists with duplicate removal

- ✅ Command-line mode for automation- `-c, --collection` - Steam Workshop collection URL or ID (required)



### moulinette.py## How Package ID Conversion Works

- ✅ Convert Workshop IDs to package IDs using local mods

- ✅ Fallback to `steam.workshop.{id}` format- `-o, --output` - Output name (without extension, optional - defaults to collection title)**With custom RimWorld version:**

- ✅ Interactive and command-line modes

- ✅ Custom RimWorld version supportThe moulinette reads `About/About.xml` files from your local mod folders to get the actual package IDs:

- ✅ Optional expansion management



### Configuration System

- ✅ Customizable database directory1. For Workshop ID `1508850027`, it looks in `<mods_dir>/1508850027/About/About.xml`

- ✅ Configurable default mods path

- ✅ Adjustable file listing limits2. Extracts the `<packageId>` tag (e.g., `jaxe.rimhud`)**Examples:**```bash

- ✅ Customizable warning display

- ✅ Default RimWorld version and expansions3. Falls back to `steam.workshop.{id}` format if About.xml is not found

- ✅ Auto-created config.ini on first run

```bash./main.py -c 3187121098 -v "1.4.3641 rev649"

## License

This means you need to have mods downloaded locally for the best results. Mods without local About.xml files will still work but will use the generic `steam.workshop.{id}` format.

MIT License - See LICENSE file for details

# From collection ID with custom name```

## Directory Structure

./main.py -c 3187121098 -o progression_pack

```

rimworld-sort-moulinette/### Interactive Mode

├── rwpackageId_database/          # Auto-created database directory

│   ├── mymodlist.rwpackageId# From full URL (auto-named)

│   └── progression.rwpackageId

├── mods/                          # Your RimWorld mods folder./main.py -c "https://steamcommunity.com/sharedfiles/filedetails/?id=3187121098"Simply run without arguments:

│   ├── 1508850027/                # Workshop ID folders

│   │   └── About/```

│   │       └── About.xml          # Contains packageId

│   └── 2009463077/```bash

│       └── About/

│           └── About.xml**Output:**./main.py

├── main.py                        # Interactive menu & collection fetcher

├── moulinette.py                  # XML generator- Creates `.rwpackageId` file in `rwpackageId_database/` directory```

├── steam_workshop.py              # Steam Workshop utilities

├── mod_utils.py                   # Mod conversion utilities- File contains numeric Workshop IDs, one per line

└── utils.py                       # Shared utilities

```- Comments (lines starting with `#`) are supportedYou'll be prompted to enter a collection URL or ID.



## Common Workflows



### Simple Interactive Workflow (Recommended)### moulinette.py - XML Generator### Legacy Mode (Direct Package IDs)

```bash

# Run main.py

./main.py

Converts `.rwpackageId` files to RimWorld modlist XML.You can also provide mod package IDs directly:

# Select option 1: Create ID list from Steam collection

# Enter collection ID: 3187121098

# Enter name or use default

**Interactive Mode:**```bash

# Select option 2: Convert ID list to RimSort list

# (This launches moulinette.py interactively)```bash./main.py -m ludeon.rimworld dawnsglow.qualcolor brrainz.harmony -o mymodlist.xml

# Select the file you just created

# Keep default name or enter custom./moulinette.py```

# Enter mods directory path

```

# Select q to quit

```Or from a text file (one package ID per line):



### Merging Multiple Collections**Command-Line Mode:**

```bash

./main.py```bash```bash



# Select option 1 to fetch first collection./moulinette.py -i <input> -d <mods_dir> [-o <output>] [-v <version>] [--no-expansions]./main.py -f mods.txt -o mymodlist.xml

# Enter collection ID for first pack

# Name it: pack1``````



# Select option 1 again to fetch second collection  

# Enter collection ID for second pack

# Name it: pack2**Arguments:**## How It Works



# Select option 3: Merge ID lists together- `-i, --input` - Input `.rwpackageId` file name or path (omit for interactive mode)

# Select pack1

# Select pack2- `-d, --mods-dir` - Path to directory containing mod folders (required in CLI mode)### Default Mode (Recommended)

# Name merged file: combined_pack

- `-o, --output` - Output XML file name or path (optional - defaults to input name)

# Select option 2 to convert to XML

# Select combined_pack- `-v, --version` - RimWorld version string (default: 1.5.4104 rev415)1. **Fetch Collection**: Downloads the Steam Workshop collection page

```

- `--no-expansions` - Exclude expansions from knownExpansions list2. **Extract Mod IDs**: Parses HTML to find all Workshop IDs

### Command-Line Workflow

```bash3. **Generate XML**: Creates modlist with `steam.workshop.{id}` entries

# 1. Fetch collection

./main.py -c 3187121098 -o mypack**Examples:**4. **No downloads needed!** Works immediately without having mods installed



# 2. Convert to XML```bash

./moulinette.py -i mypack -d ~/path/to/mods

```# Interactive mode### With `--use-local-mods` Flag



### Multiple Collections (Command-Line)./moulinette.py

```bash

# Fetch multiple collections1. **Fetch Collection**: Same as above

./main.py -c 3187121098 -o progression

./main.py -c 2222222222 -o survival# Command-line with database lookup2. **Extract Mod IDs**: Same as above

./main.py -c 3333333333 -o magic

./moulinette.py -i mymodlist -d ./mods3. **Read About.xml**: Tries to read package IDs from local mod files

# Use interactive mode to convert any of them

./moulinette.py4. **Fallback**: Uses `steam.workshop.{id}` for mods not found locally

```

# Command-line with full path and custom output5. **Generate XML**: Creates modlist with mix of package IDs and Workshop IDs

## Troubleshooting

./moulinette.py -i /path/to/file.rwpackageId -d ./mods -o custom.xml

### "No .rwpackageId files found"

- Run `main.py` and select option 1 to create collection files## Output Format

- Check that `rwpackageId_database/` directory exists

# With custom version

### "Could not find About.xml for X mods"

- This is normal if you don't have all mods downloaded locally./moulinette.py -i mymodlist -d ./mods -v "1.4.3641 rev649"The generated XML follows the RimWorld modlist format:

- The tool will use `steam.workshop.{id}` format as fallback

- To get actual package IDs, download the mods to your mods directory



### "Input file not found"# Without expansions```xml

- Make sure the file exists in `rwpackageId_database/` or provide full path

- The `.rwpackageId` extension is added automatically in CLI mode./moulinette.py -i mymodlist -d ./mods --no-expansions<?xml version='1.0' encoding='utf-8'?>



### Interactive menu not working with piped input```<ModsConfigData>

- The interactive menu is designed for real user interaction

- For automation, use command-line mode instead:  <version>1.5.4104 rev415</version>

  ```bash

  ./main.py -c 3187121098 -o mylist## File Formats  <activeMods>

  ./moulinette.py -i mylist -d ./mods -o output.xml

  ```    <li>ludeon.rimworld</li>



## Features Summary### .rwpackageId Format    <li>steam.workshop.1508850027</li>



### main.py Interactive Menu    <li>steam.workshop.2009463077</li>

- ✅ Create ID lists from Steam Workshop collections

- ✅ Launch moulinette.py to convert to XMLPlain text file containing Steam Workshop IDs:    <!-- ... all mods from collection ... -->

- ✅ Merge multiple ID lists with duplicate removal

- ✅ Command-line mode for automation  </activeMods>



### moulinette.py```  <knownExpansions>

- ✅ Convert Workshop IDs to package IDs using local mods

- ✅ Fallback to `steam.workshop.{id}` format# RimWorld Steam Workshop Collection    <li>ludeon.rimworld</li>

- ✅ Interactive and command-line modes

- ✅ Custom RimWorld version support# Collection: The Progression Modpack | (1.5)    <li>ludeon.rimworld.royalty</li>

- ✅ Optional expansion management

# One Workshop ID per line    <li>ludeon.rimworld.ideology</li>

## License

# Lines starting with # are comments    <li>ludeon.rimworld.biotech</li>

MIT License - See LICENSE file for details

    <li>ludeon.rimworld.anomaly</li>

1508850027    <li>ludeon.rimworld.odyssey</li>

2009463077  </knownExpansions>

2017538067</ModsConfigData>

``````



### XML Output FormatWith `--use-local-mods`, you'll get actual package IDs where available:



RimWorld ModsConfigData XML format:```xml

<activeMods>

```xml  <li>ludeon.rimworld</li>

<?xml version='1.0' encoding='utf-8'?>  <li>jaxe.rimhud</li>

<ModsConfigData>  <li>brrainz.harmony</li>

  <version>1.5.4104 rev415</version>  <li>steam.workshop.2017538067</li>

  <activeMods>  <!-- mix of package IDs and Workshop IDs -->

    <li>ludeon.rimworld</li></activeMods>

    <li>jaxe.rimhud</li>```

    <li>brrainz.harmony</li>

    <li>steam.workshop.2017538067</li>## Command Line Options

    ...

  </activeMods>```

  <knownExpansions>-c, --collection       Steam Workshop collection URL or ID

    <li>ludeon.rimworld</li>--use-local-mods       Read package IDs from local About.xml files

    <li>ludeon.rimworld.royalty</li>-w, --workshop-path    Path to workshop/mods folder (only with --use-local-mods)

    <li>ludeon.rimworld.ideology</li>-o, --output           Output XML file path (default: uses collection title)

    <li>ludeon.rimworld.biotech</li>-v, --version          RimWorld version (default: 1.5.4104 rev415)

    <li>ludeon.rimworld.anomaly</li>--no-expansions        Don't include expansions in knownExpansions

    <li>ludeon.rimworld.odyssey</li>-f, --file             Legacy: Read package IDs from text file

  </knownExpansions>-m, --mods             Legacy: Provide package IDs as arguments

</ModsConfigData>-h, --help             Show help message

``````



## How Package ID Conversion Works## Examples



The moulinette reads `About/About.xml` files from your local mod folders to get the actual package IDs:### Example 1: Quick Collection Export (No Downloads Needed)



1. For Workshop ID `1508850027`, it looks in `<mods_dir>/1508850027/About/About.xml````bash

2. Extracts the `<packageId>` tag (e.g., `jaxe.rimhud`)./main.py -c 3187121098

3. Falls back to `steam.workshop.{id}` format if About.xml is not found```



This means you need to have mods downloaded locally for the best results. Mods without local About.xml files will still work but will use the generic `steam.workshop.{id}` format.Output: `The Progression Modpack | (1.5).xml` with all 900+ mods



## Directory Structure### Example 2: With Local Package ID Resolution



``````bash

rimworld-sort-moulinette/./main.py -c 3187121098 --use-local-mods -w "~/.steam/steam/steamapps/workshop/content"

├── rwpackageId_database/          # Auto-created database directory```

│   ├── mymodlist.rwpackageId

│   └── progression.rwpackageIdThis reads actual package IDs from your downloaded mods.

├── mods/                          # Your RimWorld mods folder

│   ├── 1508850027/                # Workshop ID folders### Example 3: Multiple Collections

│   │   └── About/

│   │       └── About.xml          # Contains packageId```bash

│   └── 2009463077/./main.py -c 3187121098 -o "Core Mods.xml"

│       └── About/./main.py -c 2874025449 -o "Graphics Mods.xml"

│           └── About.xml./main.py -c 1234567890 -o "Gameplay Mods.xml"

├── main.py                        # Collection fetcher```

├── moulinette.py                  # XML generator

├── steam_workshop.py              # Steam Workshop utilities### Example 4: Custom Version

├── mod_utils.py                   # Mod conversion utilities

└── utils.py                       # Shared utilities```bash

```./main.py -c 3187121098 -v "1.4.3641 rev649" -o "RimWorld 1.4 Mods.xml"

```

## Common Workflows

## Troubleshooting

### Simple Workflow

```bash**"Could not find collection title"**

# 1. Fetch collection- Verify the collection URL/ID is correct

./main.py -c 3187121098 -o mypack- Check that the collection is public (not private)

- Make sure you can view it in a web browser

# 2. Convert to XML (interactive)

./moulinette.py**Do I need to download mods first?**

# Select file, keep default name, enter mods path- **No!** By default, the script uses Workshop IDs directly

```- Only use `--use-local-mods` if you specifically need actual package IDs



### Automated Workflow**What's the difference between Workshop IDs and Package IDs?**

```bash- **Workshop ID**: Numeric Steam ID (e.g., `1508850027`)

# One command at a time- **Package ID**: Mod's internal ID (e.g., `jaxe.rimhud`)

./main.py -c 3187121098 -o mypack- Most mod managers work fine with `steam.workshop.{id}` format

./moulinette.py -i mypack -d ~/path/to/mods -o mypack.xml- Use `--use-local-mods` only if your manager requires actual package IDs

```

## License

### Multiple Collections

```bashThis is a utility script for personal use with RimWorld and Steam Workshop.

# Fetch multiple collections
./main.py -c 3187121098 -o progression
./main.py -c 2222222222 -o survival
./main.py -c 3333333333 -o magic

# Use interactive mode to convert any of them
./moulinette.py
```

## Troubleshooting

### "No .rwpackageId files found"
- Run `main.py` and select option 1 to create collection files
- Check that the database directory exists (configured in `config.ini`)

### "Could not find About.xml for X mods"
- This is normal if you don't have all mods downloaded locally
- The tool will use `steam.workshop.{id}` format as fallback
- To get actual package IDs, download the mods to your mods directory
- Adjust `max_warning_lines` in `config.ini` to control how many warnings are shown

### "Input file not found"
- Make sure the file exists in the database directory or provide full path
- The `.rwpackageId` extension is added automatically in CLI mode
- Check `database_dir` setting in `config.ini`

### Changing default settings
- Edit `config.ini` to customize:
  - Database directory location
  - Default mods directory
  - Number of files shown in listings (0 = unlimited)
  - Number of warning lines (0 = show all)
  - Default RimWorld version and expansions

### Interactive menu not working with piped input
- The interactive menu is designed for real user interaction
- For automation, use command-line mode instead:
  ```bash
  ./main.py -c 3187121098 -o mylist
  ./moulinette.py -i mylist -d ./mods -o output.xml
  ```

## License

MIT License - See LICENSE file for details

## New Feature: Remove IDs from List (Option 4)

The menu now includes a 4th option to remove IDs from one list based on another:

### Use Case
- Remove incompatible mods from your modlist
- Exclude certain mods while keeping everything else
- Subtract one collection's mods from another collection

### How It Works
1. Select option 4 from the main menu
2. Choose the **BASE list** (the list you want to keep and modify)
3. Choose the **REMOVAL list** (IDs in this list will be removed from the base)
4. The tool will remove any IDs from the base that appear in the removal list
5. Name the filtered output file

### Example
```bash
./main.py

# Select option 4: Remove IDs from list
# Select BASE list: my_full_modlist (100 mods)
# Select REMOVAL list: incompatible_mods (10 mods)
# Result: my_filtered_modlist (90 mods - removed the 10 incompatible ones)
```

**Note:** The operation is cancelled if the result would be empty (all IDs removed).
