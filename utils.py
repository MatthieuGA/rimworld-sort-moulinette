"""
Utility functions for RimWorld modlist generation.
"""

import xml.etree.ElementTree as ET
import os
import re
from typing import List, Optional
from config import get_config


# Legacy constants for backward compatibility
def _get_default_version():
    return get_config().default_version

def _get_default_expansions():
    return get_config().expansions

DEFAULT_VERSION = None  # Will be dynamically retrieved
DEFAULT_EXPANSIONS = None  # Will be dynamically retrieved

BASE_GAME_PACKAGE_ID = "ludeon.rimworld"
RWPACKAGEID_EXTENSION = ".rwpackageId"

# Characters not allowed in file names on Windows (the strictest OS), plus control characters
INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
# Device names Windows refuses as file names, with or without an extension
WINDOWS_RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL"} | {f"{p}{i}" for p in ("COM", "LPT") for i in range(1, 10)}


def sanitize_filename(filename: str) -> str:
    """
    Make a name safe to use as a single file name (no folders) on any OS.

    Invalid characters such as / or \\ are replaced with underscores, so
    "Progression (2/3)" becomes "Progression (2_3)".

    Args:
        filename: Original filename

    Returns:
        Sanitized filename

    Raises:
        ValueError: If nothing usable is left (e.g. "", "..", "///")
    """
    sanitized = INVALID_FILENAME_CHARS.sub('_', filename)
    # Windows silently drops trailing dots and spaces
    sanitized = sanitized.strip().rstrip('. ')

    if not sanitized.strip('_'):
        raise ValueError(f"Invalid file name: {filename!r}")

    if sanitized.split('.')[0].upper() in WINDOWS_RESERVED_NAMES:
        sanitized = f"_{sanitized}"

    return sanitized


def get_rwpackageid_path(name: str) -> str:
    """
    Get the full path for a .rwpackageId file in the database directory.
    The name is sanitized, and the .rwpackageId extension is added if not present.

    Args:
        name: Base name for the file (without or with .rwpackageId extension)

    Returns:
        Full path to the .rwpackageId file

    Raises:
        ValueError: If the name cannot be turned into a valid file name
    """
    if name.endswith(RWPACKAGEID_EXTENSION):
        name = name[:-len(RWPACKAGEID_EXTENSION)]

    return os.path.join(get_config().database_dir, f"{sanitize_filename(name)}{RWPACKAGEID_EXTENSION}")


def get_package_id_from_about_xml(about_xml_path: str) -> Optional[str]:
    """
    Extract package ID from a mod's About.xml file.
    
    Args:
        about_xml_path: Full path to the About.xml file
        
    Returns:
        Package ID string (lowercase), or None if not found
    """
    if not os.path.isfile(about_xml_path):
        return None
    
    try:
        tree = ET.parse(about_xml_path)
        root = tree.getroot()
        package_elem = root.find("packageId")
        
        if package_elem is not None and package_elem.text:
            return package_elem.text.strip().lower()
    except ET.ParseError:
        pass
    
    return None


def create_modlist_xml(
    package_ids: List[str],
    output_path: str,
    version: str = None,
    expansions: Optional[List[str]] = None
) -> None:
    """
    Create a RimWorld modlist XML file.
    
    Args:
        package_ids: List of mod package IDs
        output_path: Path to the output XML file
        version: RimWorld version string (None = use config default)
        expansions: List of expansion package IDs to include, None to exclude all
    """
    config = get_config()
    
    # Use config defaults if not specified
    if version is None:
        version = config.default_version
    
    # Handle expansions
    if expansions is None:
        if config.include_expansions:
            expansions = config.expansions.copy()
        else:
            expansions = []
    
    # activeMods order: base game, then expansions, then mods.
    # Expansions must be active (not only known) for RimWorld/RimSort to load them.
    official_ids = [BASE_GAME_PACKAGE_ID]
    for expansion_id in expansions:
        expansion_id = expansion_id.lower()
        if expansion_id not in official_ids:
            official_ids.append(expansion_id)

    active_ids = list(official_ids)
    for package_id in package_ids:
        package_id = package_id.lower()
        if package_id not in active_ids:
            active_ids.append(package_id)

    # Create root element
    root = ET.Element("ModsConfigData")
    
    # Add version
    version_elem = ET.Element("version")
    version_elem.text = version
    root.append(version_elem)
    
    # Add activeMods
    active_mods = ET.Element("activeMods")
    for package_id in active_ids:
        li = ET.Element("li")
        li.text = package_id
        active_mods.append(li)
    root.append(active_mods)
    
    # Add knownExpansions
    known_expansions = ET.Element("knownExpansions")
    for expansion_id in expansions:
        li = ET.Element("li")
        li.text = expansion_id.lower()
        known_expansions.append(li)
    root.append(known_expansions)
    
    # Create tree and format with indentation
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    
    # Write to file
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"✓ Modlist XML saved to: {output_path}")


def read_modlist_xml(xml_path: str) -> List[str]:
    """
    Read the activeMods package IDs from a RimWorld/RimSort modlist XML file.

    Args:
        xml_path: Path to the modlist XML file

    Returns:
        List of package IDs (lowercase), in load order

    Raises:
        ValueError: If the file is not a valid modlist XML
    """
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML file: {e}")

    active_mods = root.find("activeMods")
    if active_mods is None:
        raise ValueError("No <activeMods> section found in XML file")

    return [li.text.strip().lower() for li in active_mods.findall("li") if li.text and li.text.strip()]


def is_official_package_id(package_id: str) -> bool:
    """Check if a package ID is the base game or an official expansion."""
    return package_id.lower().startswith(BASE_GAME_PACKAGE_ID)


def write_workshop_ids_file(filepath: str, workshop_ids: list, collection_title: str = None,
                            unresolved: Optional[List[str]] = None) -> None:
    """
    Write Workshop IDs to a .rwpackageId file.

    Args:
        filepath: Path to the output .rwpackageId file
        workshop_ids: List of Steam Workshop mod IDs (numeric)
        collection_title: Optional collection title for the header
        unresolved: Optional package IDs that could not be resolved to a Workshop ID,
                    written as trailing comments so they are not silently lost
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)

    with open(filepath, 'w') as f:
        f.write("# RimWorld Steam Workshop Collection\n")
        if collection_title:
            f.write(f"# Collection: {collection_title}\n")
        f.write("# One Workshop ID per line\n")
        f.write("# Lines starting with # are comments\n\n")

        for workshop_id in workshop_ids:
            f.write(f"{workshop_id}\n")

        if unresolved:
            f.write("\n# Package IDs with no matching Workshop mod (not included above):\n")
            for package_id in unresolved:
                f.write(f"# - {package_id}\n")

    print(f"✓ Workshop IDs saved to: {filepath}")
