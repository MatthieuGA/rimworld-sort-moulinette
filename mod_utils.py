"""
Mod folder utilities for reading package IDs from About.xml files.
"""

import os
from typing import Dict, List, Optional, Tuple
from utils import get_package_id_from_about_xml, is_official_package_id
from config import get_config

WORKSHOP_FALLBACK_PREFIX = "steam.workshop."
# RimWorld appends this to a packageId when the same mod is also installed locally
STEAM_DUPLICATE_SUFFIX = "_steam"


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


def get_workshop_id_from_mod_folder(mod_folder_path: str) -> Optional[str]:
    """
    Get the Steam Workshop ID of a mod folder.

    Workshop folders are named after their numeric ID; otherwise fall back
    to About/PublishedFileId.txt (present in most published mods).

    Args:
        mod_folder_path: Path to a single mod folder

    Returns:
        Workshop ID string, or None if it cannot be determined
    """
    folder_name = os.path.basename(os.path.normpath(mod_folder_path))
    if folder_name.isdigit():
        return folder_name

    published_id_path = os.path.join(mod_folder_path, "About", "PublishedFileId.txt")
    if os.path.isfile(published_id_path):
        try:
            with open(published_id_path, 'r') as f:
                published_id = f.read().strip()
            if published_id.isdigit():
                return published_id
        except OSError:
            pass

    return None


def build_package_id_index(mods_directory: str) -> Dict[str, str]:
    """
    Map package IDs to Workshop IDs by scanning every mod folder's About.xml.

    Args:
        mods_directory: Path to the directory containing mod folders

    Returns:
        Dict of package ID (lowercase) -> Workshop ID
    """
    index = {}

    for entry in sorted(os.listdir(mods_directory)):
        mod_folder_path = os.path.join(mods_directory, entry)
        if not os.path.isdir(mod_folder_path):
            continue

        package_id = get_package_id_from_about_xml(os.path.join(mod_folder_path, "About", "About.xml"))
        if not package_id or package_id in index:
            continue

        workshop_id = get_workshop_id_from_mod_folder(mod_folder_path)
        if workshop_id:
            index[package_id] = workshop_id

    return index


def convert_package_ids_to_workshop_ids(package_ids: List[str], mods_directory: str) -> Tuple[List[str], List[str]]:
    """
    Convert RimWorld package IDs back to Steam Workshop numeric IDs.

    The base game and official expansions are skipped (they are not Workshop mods).

    Args:
        package_ids: List of package IDs (e.g. from a modlist XML's activeMods)
        mods_directory: Path to the directory containing mod folders

    Returns:
        Tuple of (Workshop IDs in load order, package IDs that could not be resolved)
    """
    print(f"\nIndexing mod folders in: {mods_directory}")
    index = build_package_id_index(mods_directory)
    print(f"✓ Indexed {len(index)} mod(s)")

    workshop_ids = []
    unresolved = []
    skipped_official = 0

    for package_id in package_ids:
        package_id = package_id.lower()

        if is_official_package_id(package_id):
            skipped_official += 1
            continue

        workshop_id = index.get(package_id)
        if workshop_id is None and package_id.endswith(STEAM_DUPLICATE_SUFFIX):
            workshop_id = index.get(package_id[:-len(STEAM_DUPLICATE_SUFFIX)])
        if workshop_id is None and package_id.startswith(WORKSHOP_FALLBACK_PREFIX):
            suffix = package_id[len(WORKSHOP_FALLBACK_PREFIX):]
            if suffix.isdigit():
                workshop_id = suffix

        if workshop_id is None:
            unresolved.append(package_id)
        elif workshop_id not in workshop_ids:
            workshop_ids.append(workshop_id)

    # Print summary
    config = get_config()

    if skipped_official:
        print(f"\n✓ Skipped {skipped_official} base game/expansion entries")

    if unresolved:
        print(f"\n⚠ Warning: Could not find a Workshop mod for {len(unresolved)} package ID(s).")
        print(f"   They will be listed as comments in the output file.")

        max_lines = config.max_warning_lines
        if max_lines == 0 or len(unresolved) <= max_lines:
            for package_id in unresolved:
                print(f"   - {package_id}")
        else:
            print(f"   (showing first {max_lines} of {len(unresolved)})")
            for package_id in unresolved[:max_lines]:
                print(f"   - {package_id}")

    print(f"\n✓ Resolved {len(workshop_ids)} Workshop ID(s)")

    return workshop_ids, unresolved
