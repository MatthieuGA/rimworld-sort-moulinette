"""
Mod folder utilities for reading package IDs from About.xml files.
"""

import os
from typing import List
from utils import get_package_id_from_about_xml
from config import get_config


def get_package_id_from_mod_folder(mods_directory: str, mod_id: str) -> str:
    """
    Get package ID from a mod folder's About.xml file.
    
    Args:
        mods_directory: Path to directory containing mod folders
        mod_id: Steam Workshop mod ID (numeric)
        
    Returns:
        Package ID if found, otherwise 'steam.workshop.{id}' format
    """
    about_xml_path = os.path.join(mods_directory, mod_id, "About", "About.xml")
    
    package_id = get_package_id_from_about_xml(about_xml_path)
    
    if package_id:
        return package_id
    else:
        # Fallback to workshop ID format
        return f"steam.workshop.{mod_id}"


def convert_workshop_ids_to_package_ids(mod_ids: List[str], mods_directory: str) -> List[str]:
    """
    Convert Steam Workshop numeric IDs to RimWorld package IDs by reading About.xml files.
    
    Args:
        mod_ids: List of Steam Workshop mod IDs (numeric)
        mods_directory: Path to the directory containing mod folders
        
    Returns:
        List of package IDs
    """
    package_ids = ["ludeon.rimworld"]  # Base game always first
    missing_mods = []
    
    print(f"\nReading package IDs from mod folders in: {mods_directory}")
    
    for mod_id in mod_ids:
        package_id = get_package_id_from_mod_folder(mods_directory, mod_id)
        
        if package_id.startswith("steam.workshop."):
            missing_mods.append(mod_id)
        
        if package_id != "ludeon.rimworld":
            package_ids.append(package_id)
    
    # Print summary
    config = get_config()
    found_count = len(package_ids) - 1 - len(missing_mods)  # Subtract base game
    
    if missing_mods:
        print(f"\n⚠ Warning: Could not find About.xml for {len(missing_mods)} mod(s).")
        print(f"   Using 'steam.workshop.{{id}}' format for these mods.")
        
        max_lines = config.max_warning_lines
        if max_lines == 0 or len(missing_mods) <= max_lines:
            for mod_id in missing_mods:
                print(f"   - {mod_id}")
        else:
            print(f"   (showing first {max_lines} of {len(missing_mods)})")
            for mod_id in missing_mods[:max_lines]:
                print(f"   - {mod_id}")
    
    print(f"\n✓ Successfully found {found_count} package IDs")
    if missing_mods:
        print(f"✓ Using fallback format for {len(missing_mods)} mods")
    
    return package_ids
