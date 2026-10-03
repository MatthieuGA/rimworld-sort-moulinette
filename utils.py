"""
Utility functions for RimWorld modlist generation.
"""

import xml.etree.ElementTree as ET
import os
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
