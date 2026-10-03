#!/usr/bin/python3
"""
RimWorld Modlist Manager

Main entry point with interactive menu for managing RimWorld modlists.
"""

import argparse
import os
import re
import sys
import subprocess
from steam_workshop import extract_collection_id, fetch_collection_details
from config import get_config
from utils import write_workshop_ids_file


def get_database_dir() -> str:
    """Get the database directory from config."""
    return get_config().database_dir


def sanitize_filename(filename: str) -> str:
    """
    Remove invalid characters from filename.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid filename characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    return sanitized.strip()


def get_rwpackageid_path(name: str) -> str:
    """
    Get the full path for a .rwpackageId file in the database directory.
    Automatically adds .rwpackageId extension if not present.
    
    Args:
        name: Base name for the file (without or with .rwpackageId extension)
        
    Returns:
        Full path to the .rwpackageId file
    """
    database_dir = get_database_dir()
    
    # Ensure database directory exists
    os.makedirs(database_dir, exist_ok=True)
    
    # Add extension if not present
    if not name.endswith('.rwpackageId'):
        name = f"{name}.rwpackageId"
    
    return os.path.join(database_dir, name)


def read_workshop_ids_file(filepath: str) -> list:
    """
    Read Workshop IDs from a .rwpackageId file.
    
    Args:
        filepath: Path to the .rwpackageId file
        
    Returns:
        List of Workshop ID strings
    """
    workshop_ids = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                workshop_ids.append(line)
    
    return workshop_ids


def list_rwpackageid_files() -> list:
    """
    List all .rwpackageId files in the database directory.
    
    Returns:
        List of .rwpackageId filenames (without path)
    """
    database_dir = get_database_dir()
    
    if not os.path.exists(database_dir):
        return []
    
    files = []
    for filename in os.listdir(database_dir):
        if filename.endswith('.rwpackageId'):
            files.append(filename)
    
    return sorted(files)


def select_rwpackageid_file(prompt: str = "Select a .rwpackageId file") -> str:
    """
    Interactively select a .rwpackageId file from the database.
    
    Args:
        prompt: Custom prompt message
        
    Returns:
        Path to the selected .rwpackageId file, or None if cancelled
    """
    config = get_config()
    database_dir = get_database_dir()
    files = list_rwpackageid_files()
    
    if not files:
        print(f"Error: No .rwpackageId files found in {database_dir}/")
        return None
    
    # Limit files if configured (0 = no limit)
    max_files = config.max_files_listed
    if max_files > 0 and len(files) > max_files:
        files = files[:max_files]
        print(f"Note: Showing first {max_files} files (configured limit)")
    
    print(f"\n{prompt}:")
    print("=" * 60)
    for i, filename in enumerate(files, 1):
        print(f"  {i}. {filename}")
    print("=" * 60)
    
    while True:
        try:
            choice = input(f"\nSelect a file (1-{len(files)}) or 'q' to cancel: ").strip()
            
            if choice.lower() == 'q':
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(files):
                selected_file = files[index]
                return os.path.join(database_dir, selected_file)
            else:
                print(f"Invalid selection. Please enter a number between 1 and {len(files)}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to cancel")
        except KeyboardInterrupt:
            print("\nCancelled.")
            return None


def create_from_collection():
    """Interactive workflow to create a .rwpackageId from a Steam collection."""
    print("\n=== Create ID List from Steam Collection ===\n")
    
    # Get collection URL or ID
    collection_input = input("Enter Steam Workshop collection URL or ID: ").strip()
    if not collection_input:
        print("Cancelled.")
        return
    
    # Extract and validate collection ID
    collection_id = extract_collection_id(collection_input)
    if not collection_id:
        print(f"Error: Invalid collection URL or ID: {collection_input}")
        return
    
    print(f"\nFetching collection {collection_id} from Steam Workshop...")
    
    output_name = None
    output_path = None
    
    try:
        # Fetch collection details
        collection_title, workshop_ids = fetch_collection_details(collection_id)
        print(f"✓ Found collection: {collection_title}")
        print(f"✓ Contains {len(workshop_ids)} mod(s)")
        
        # Get output name
        default_name = sanitize_filename(collection_title)
        print(f"\nDefault output name: {default_name}")
        custom_name = input("Enter custom name (or press Enter to use default): ").strip()
        
        output_name = custom_name if custom_name else default_name
        output_path = get_rwpackageid_path(output_name)
        
        # Write Workshop IDs to file
        print(f"\nWriting Workshop IDs to file...")
        write_workshop_ids_file(output_path, workshop_ids, collection_title)
        
        print(f"\n✓ Complete! Workshop IDs file created: {output_path}")
        
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"Error: {e}")


def convert_to_xml():
    """Interactive workflow to convert a .rwpackageId to XML."""
    print("\n=== Convert ID List to RimSort List ===\n")
    
    # Run moulinette.py in interactive mode
    try:
        subprocess.run([sys.executable, "moulinette.py"], check=True)
    except subprocess.CalledProcessError:
        print("\nError running moulinette.py")
    except FileNotFoundError:
        print("\nError: moulinette.py not found")


def convert_from_xml():
    """Interactive workflow to convert a RimSort list XML back to a .rwpackageId."""
    print("\n=== Convert RimSort List to ID List ===\n")

    # Run moulinette.py in reverse interactive mode
    try:
        subprocess.run([sys.executable, "moulinette.py", "--reverse"], check=True)
    except subprocess.CalledProcessError:
        print("\nError running moulinette.py")
    except FileNotFoundError:
        print("\nError: moulinette.py not found")


def merge_id_lists():
    """Interactive workflow to merge two .rwpackageId files."""
    print("\n=== Merge ID Lists ===\n")
    
    config = get_config()
    
    output_name = None
    output_path = None
    
    # Select first file
    file1 = select_rwpackageid_file("Select first .rwpackageId file")
    if not file1:
        print("Cancelled.")
        return
    
    print(f"Selected: {os.path.basename(file1)}")
    
    # Select second file
    file2 = select_rwpackageid_file("Select second .rwpackageId file")
    if not file2:
        print("Cancelled.")
        return
    
    print(f"Selected: {os.path.basename(file2)}")
    
    try:
        # Read both files
        ids1 = read_workshop_ids_file(file1)
        ids2 = read_workshop_ids_file(file2)
        
        print(f"\nFirst file contains {len(ids1)} ID(s)")
        print(f"Second file contains {len(ids2)} ID(s)")
        
        # Merge and remove duplicates while preserving order
        seen = set()
        merged_ids = []
        for workshop_id in ids1 + ids2:
            if workshop_id not in seen:
                seen.add(workshop_id)
                merged_ids.append(workshop_id)
        
        duplicates = len(ids1) + len(ids2) - len(merged_ids)
        print(f"✓ Merged list contains {len(merged_ids)} unique ID(s)")
        if duplicates > 0:
            print(f"  (Removed {duplicates} duplicate(s))")
        
        # Get output name
        default_name = config.default_merged_name
        custom_name = input(f"\nEnter output name (default: {default_name}): ").strip()
        output_name = custom_name if custom_name else default_name
        output_path = get_rwpackageid_path(output_name)
        
        # Write merged IDs
        write_workshop_ids_file(output_path, merged_ids, "Merged ID List")
        
        print(f"\n✓ Complete! Merged file created: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")


def subtract_id_lists():
    """Interactive workflow to remove IDs from one list based on another."""
    print("\n=== Remove IDs from List ===\n")
    
    config = get_config()
    
    output_name = None
    output_path = None
    
    # Select base file (the one to keep)
    print("First, select the BASE list (the list you want to keep and modify):")
    base_file = select_rwpackageid_file("Select BASE list")
    if not base_file:
        print("Cancelled.")
        return
    
    print(f"✓ Base list selected: {os.path.basename(base_file)}")
    
    # Select removal file (the IDs to remove)
    print("\nNow, select the REMOVAL list (IDs in this list will be removed from the base):")
    removal_file = select_rwpackageid_file("Select REMOVAL list")
    if not removal_file:
        print("Cancelled.")
        return
    
    print(f"✓ Removal list selected: {os.path.basename(removal_file)}")
    
    try:
        # Read both files
        base_ids = read_workshop_ids_file(base_file)
        removal_ids = read_workshop_ids_file(removal_file)
        
        print(f"\nBase list contains {len(base_ids)} ID(s)")
        print(f"Removal list contains {len(removal_ids)} ID(s)")
        
        # Create a set of IDs to remove for O(1) lookup
        removal_set = set(removal_ids)
        
        # Filter out IDs that are in the removal set
        filtered_ids = [workshop_id for workshop_id in base_ids if workshop_id not in removal_set]
        
        removed_count = len(base_ids) - len(filtered_ids)
        
        print(f"\n✓ Result will contain {len(filtered_ids)} ID(s)")
        if removed_count > 0:
            print(f"  (Removed {removed_count} ID(s) that were in the removal list)")
        else:
            print(f"  (No IDs were removed - no matches found)")
        
        if len(filtered_ids) == 0:
            print("\n⚠ Warning: Result would be empty. Operation cancelled.")
            return
        
        # Get output name
        default_name = os.path.basename(base_file).replace('.rwpackageId', '_filtered')
        custom_name = input(f"\nEnter output name (default: {default_name}): ").strip()
        output_name = custom_name if custom_name else default_name
        output_path = get_rwpackageid_path(output_name)
        
        # Write filtered IDs
        write_workshop_ids_file(output_path, filtered_ids, f"Filtered ID List (removed {removed_count} IDs)")
        
        print(f"\n✓ Complete! Filtered file created: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")


def show_menu():
    """Display the main interactive menu."""
    print("\n" + "=" * 60)
    print("  RimWorld Modlist Manager")
    print("=" * 60)
    print("\n1. Create ID list from Steam collection")
    print("2. Convert ID list to RimSort list")
    print("3. Merge ID lists together")
    print("4. Remove IDs from list")
    print("5. Convert RimSort list to ID list")
    print("q. Quit")
    print()


def interactive_mode():
    """Run the interactive menu system."""
    while True:
        show_menu()

        try:
            choice = input("Select an option (1-5 or q): ").strip().lower()
            
            if choice == '1':
                create_from_collection()
            elif choice == '2':
                convert_to_xml()
            elif choice == '3':
                merge_id_lists()
            elif choice == '4':
                subtract_id_lists()
            elif choice == '5':
                convert_from_xml()
            elif choice == 'q':
                print("\nGoodbye!")
                return 0
            else:
                print("\nInvalid option. Please select 1, 2, 3, 4, 5, or q")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            return 0
        except Exception as e:
            print(f"\nError: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="RimWorld Modlist Manager - Create and manage modlist files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Interactive Mode (no arguments):
  Run with no arguments to access the interactive menu with options to:
  - Create ID lists from Steam collections
  - Convert ID lists to XML
  - Merge multiple ID lists
  - Remove IDs from a list
  - Convert XML back to an ID list

Command-Line Mode Examples:
  # From a collection ID with custom name
  python main.py -c 3187121098 -o mymodlist

  # From a full URL (auto-named based on collection title)
  python main.py -c "https://steamcommunity.com/sharedfiles/filedetails/?id=3187121098"

Note: Files are saved to database directory (see config.ini) with .rwpackageId extension
        """
    )

    parser.add_argument(
        '-c', '--collection',
        help='Steam Workshop collection URL or ID (command-line mode)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output name for .rwpackageId file (without extension, default: uses collection title)'
    )

    args = parser.parse_args()

    # If no arguments provided, run interactive mode
    if not args.collection:
        return interactive_mode()
    
    # Command-line mode: create from collection
    collection_id = extract_collection_id(args.collection)

    if not collection_id:
        print(f"Error: Invalid collection URL or ID: {args.collection}")
        print("Please provide a valid Steam Workshop collection URL or numeric ID")
        return 1

    print(f"Fetching collection {collection_id} from Steam Workshop...")

    output_name = None
    output_path = None

    try:
        # Fetch collection details
        collection_title, workshop_ids = fetch_collection_details(collection_id)
        print(f"✓ Found collection: {collection_title}")
        print(f"✓ Contains {len(workshop_ids)} mod(s)")

        # Determine output name
        output_name = args.output
        if not output_name:
            # Use collection title as filename
            output_name = sanitize_filename(collection_title)
        
        # Get full path in database directory
        output_path = get_rwpackageid_path(output_name)

        # Write Workshop IDs to file
        print(f"\nWriting Workshop IDs to file...")
        write_workshop_ids_file(output_path, workshop_ids, collection_title)

        print(f"\n✓ Complete! Workshop IDs file created: {output_path}")
        print(f"  Use moulinette.py to convert to modlist XML")

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
