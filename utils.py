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
    
    # Ensure ludeon.rimworld is first in activeMods
    if "ludeon.rimworld" not in package_ids:
        package_ids.insert(0, "ludeon.rimworld")
    elif package_ids[0] != "ludeon.rimworld":
        package_ids.remove("ludeon.rimworld")
        package_ids.insert(0, "ludeon.rimworld")
    
    # Create root element
    root = ET.Element("ModsConfigData")
    
    # Add version
    version_elem = ET.Element("version")
    version_elem.text = version
    root.append(version_elem)
    
    # Add activeMods
    active_mods = ET.Element("activeMods")
    for package_id in package_ids:
        li = ET.Element("li")
        li.text = package_id.lower()
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
