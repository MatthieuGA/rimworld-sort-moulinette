#!/usr/bin/python3
"""
RimWorld Modlist Moulinette

This script converts a .rwpackageId file (list of Workshop IDs) to a RimWorld modlist XML file
by reading package IDs from local mod folders.
"""

import argparse
import os
import sys
from utils import create_modlist_xml
from mod_utils import convert_workshop_ids_to_package_ids
from config import get_config


def get_database_dir() -> str:
    """Get the database directory from config."""
    return get_config().database_dir


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
    
    # Add extension if not present
    if not name.endswith('.rwpackageId'):
        name = f"{name}.rwpackageId"
    
    return os.path.join(database_dir, name)


def get_xml_output_path(rwpackageid_name: str, custom_name: str = None) -> str:
    """
    Get the output path for the XML file.
    
    Args:
        rwpackageid_name: Name of the .rwpackageId file (with or without extension)
        custom_name: Optional custom name for the output file
        
    Returns:
        Full path to the output XML file
    """
    if custom_name:
        # Use custom name
        base_name = custom_name
    else:
        # Use rwpackageId name (remove extension if present)
        if rwpackageid_name.endswith('.rwpackageId'):
            base_name = rwpackageid_name[:-len('.rwpackageId')]
        else:
            base_name = rwpackageid_name
    
    # Add .xml extension if not present
    if not base_name.endswith('.xml'):
        base_name = f"{base_name}.xml"
    
    return base_name


def list_rwpackageid_files(max_files: int = None) -> list:
    """
    List .rwpackageId files in the database directory.
    
    Args:
        max_files: Maximum number of files to return (None = use config, 0 = unlimited)
        
    Returns:
        List of .rwpackageId filenames (without path)
    """
    config = get_config()
    database_dir = get_database_dir()
    
    if max_files is None:
        max_files = config.max_files_listed
    
    if not os.path.exists(database_dir):
        return []
    
    files = []
    for filename in os.listdir(database_dir):
        if filename.endswith('.rwpackageId'):
            files.append(filename)
            if max_files > 0 and len(files) >= max_files:
                break
    
    return sorted(files)


def select_rwpackageid_interactive() -> str:
    """
    Interactively select a .rwpackageId file from the database.
    
    Returns:
        Path to the selected .rwpackageId file, or None if cancelled
    """
    config = get_config()
    database_dir = get_database_dir()
    files = list_rwpackageid_files()
    
    if not files:
        print(f"Error: No .rwpackageId files found in {database_dir}/")
        print(f"  Run main.py first to create a collection file")
        return None
    
    print(f"\nAvailable .rwpackageId files in {database_dir}/:")
    print("=" * 60)
    for i, filename in enumerate(files, 1):
        print(f"  {i}. {filename}")
    print("=" * 60)
    
    while True:
        try:
            choice = input(f"\nSelect a file (1-{len(files)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                print("Cancelled.")
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(files):
                selected_file = files[index]
                return os.path.join(database_dir, selected_file)
            else:
                print(f"Invalid selection. Please enter a number between 1 and {len(files)}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit")
        except KeyboardInterrupt:
            print("\nCancelled.")
            return None


def get_output_name_interactive(rwpackageid_filename: str) -> str:
    """
    Interactively get the output filename for the XML.
    
    Args:
        rwpackageid_filename: Name of the .rwpackageId file (with extension)
        
    Returns:
        Output name (without .xml extension), or None if cancelled
    """
    # Extract base name without extension
    base_name = rwpackageid_filename
    if base_name.endswith('.rwpackageId'):
        base_name = base_name[:-len('.rwpackageId')]
    
    print(f"\nDefault output name: {base_name}.xml")
    
    while True:
        try:
            response = input("Keep default name? (y/n): ").strip().lower()
            
            if response == 'y':
                return base_name
            elif response == 'n':
                custom_name = input("Enter output name (without .xml extension): ").strip()
                if custom_name:
                    return custom_name
                else:
                    print("Name cannot be empty. Try again.")
            else:
                print("Please enter 'y' or 'n'")
        except KeyboardInterrupt:
            print("\nCancelled.")
            return None


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


def process_modlist(input_file: str, mods_dir: str, output_file: str, 
                   version: str = None, expansions: list = None) -> int:
    """
    Process a .rwpackageId file and create a modlist XML.
    
    Args:
        input_file: Path to the .rwpackageId file
        mods_dir: Path to the mods directory
        output_file: Path to the output XML file
        version: RimWorld version string (None = use config default)
        expansions: List of expansion package IDs (None = use config default)
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Validate input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file does not exist: {input_file}")
        return 1

    if not os.path.isfile(input_file):
        print(f"Error: Not a file: {input_file}")
        return 1

    # Validate mods directory exists
    if not os.path.exists(mods_dir):
        print(f"Error: Mods directory does not exist: {mods_dir}")
        return 1

    if not os.path.isdir(mods_dir):
        print(f"Error: Not a directory: {mods_dir}")
        return 1

    try:
        # Read Workshop IDs from file
        print(f"Reading Workshop IDs from: {input_file}")
        workshop_ids = read_workshop_ids_file(input_file)
        
        if not workshop_ids:
            print("Error: No Workshop IDs found in input file")
            return 1
        
        print(f"✓ Found {len(workshop_ids)} Workshop ID(s)")

        # Convert Workshop IDs to package IDs
        package_ids = convert_workshop_ids_to_package_ids(workshop_ids, mods_dir)

        # Create the XML
        print(f"\nGenerating modlist XML...")
        create_modlist_xml(
            package_ids=package_ids,
            output_path=output_file,
            version=version,
            expansions=expansions
        )

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Convert a .rwpackageId file to a RimWorld modlist XML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (no arguments)
  python moulinette.py

  # Command-line mode with file from database
  python moulinette.py -i mymodlist -d ./mods -o output.xml

  # Command-line mode with full path
  python moulinette.py -i /path/to/file.rwpackageId -d ./mods -o output.xml

  # With custom version
  python moulinette.py -i mymodlist -d ./mods -v "1.4.3641 rev649"

  # Without expansions
  python moulinette.py -i mymodlist -d ./mods --no-expansions
        """
    )

    parser.add_argument(
        '-i', '--input',
        help='Input .rwpackageId file name or path (if not provided, interactive mode)'
    )
    parser.add_argument(
        '-d', '--mods-dir',
        help='Path to directory containing mod folders (required in non-interactive mode)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output XML file name or path (if not provided, uses input name)'
    )
    parser.add_argument(
        '-v', '--version',
        help=f'RimWorld version (default: from config.ini)'
    )
    parser.add_argument(
        '--no-expansions',
        action='store_true',
        help='Do not include any expansions in knownExpansions (only base game)'
    )

    args = parser.parse_args()
    
    config = get_config()

    # Interactive mode if no input file specified
    if not args.input:
        print("=== RimWorld Modlist Moulinette - Interactive Mode ===\n")
        
        # Select input file
        input_file = select_rwpackageid_interactive()
        if not input_file:
            return 1
        
        # Get base filename for default output name
        input_filename = os.path.basename(input_file)
        
        # Get output name
        output_base_name = get_output_name_interactive(input_filename)
        if not output_base_name:
            return 1
        
        output_file = get_xml_output_path(input_filename, output_base_name)
        
        # Ask for mods directory if not provided
        if not args.mods_dir:
            default_mods_dir = config.default_mods_dir
            mods_dir_input = input(f"\nEnter mods directory path (default: {default_mods_dir}): ").strip()
            mods_dir = mods_dir_input if mods_dir_input else default_mods_dir
        else:
            mods_dir = args.mods_dir
        
        # Determine expansions
        if args.no_expansions:
            expansions = []
        else:
            expansions = None  # Use config default
        
        # Get version
        version = args.version  # None will use config default
        
        print("\n" + "=" * 60)
        print("Configuration:")
        print(f"  Input:  {input_file}")
        print(f"  Mods:   {mods_dir}")
        print(f"  Output: {output_file}")
        print(f"  Version: {version if version else config.default_version}")
        print("=" * 60 + "\n")
        
        return process_modlist(input_file, mods_dir, output_file, version, expansions)
    
    # Command-line mode
    else:
        # Validate required arguments for command-line mode
        if not args.mods_dir:
            print("Error: --mods-dir is required when using command-line mode")
            print("  Run without arguments for interactive mode")
            return 1
        
        # Determine input file path
        if os.path.exists(args.input):
            input_file = args.input
        else:
            # Try in database directory
            input_file = get_rwpackageid_path(args.input)
            if not os.path.exists(input_file):
                print(f"Error: Input file not found: {args.input}")
                print(f"  Also checked: {input_file}")
                return 1
        
        # Determine output file path
        if args.output:
            output_file = args.output
        else:
            # Use input name as base
            input_basename = os.path.basename(input_file)
            output_file = get_xml_output_path(input_basename)
        
        # Determine expansions
        if args.no_expansions:
            expansions = []
        else:
            expansions = None  # Use config default
        
        return process_modlist(input_file, args.mods_dir, output_file, args.version, expansions)


if __name__ == '__main__':
    sys.exit(main())
