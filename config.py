#!/usr/bin/python3
"""
Configuration loader for RimWorld Modlist Manager.

Reads settings from config.ini or uses defaults.
"""

import os
import configparser
from typing import Optional, List


class Config:
    """Configuration manager for the application."""
    
    def __init__(self, config_file: str = "config.ini"):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.parser = configparser.ConfigParser()
        
        # Set defaults
        self._set_defaults()
        
        # Load from file if it exists
        if os.path.exists(config_file):
            self.parser.read(config_file)
    
    def _set_defaults(self):
        """Set default configuration values."""
        # Paths section
        self.parser['Paths'] = {
            'database_dir': 'rwpackageId_database',
            'default_mods_dir': './mods',
            'default_output_dir': '.'
        }
        
        # RimWorld section
        self.parser['RimWorld'] = {
            'default_version': '1.5.4104 rev415',
            'include_expansions': 'true',
            'expansions': 'ludeon.rimworld,ludeon.rimworld.royalty,ludeon.rimworld.ideology,ludeon.rimworld.biotech,ludeon.rimworld.anomaly,ludeon.rimworld.odyssey'
        }
        
        # Display section
        self.parser['Display'] = {
            'max_files_listed': '20',
            'max_warning_lines': '10'
        }
        
        # Merge section
        self.parser['Merge'] = {
            'default_merged_name': 'merged_list'
        }
    
    def save(self):
        """Save current configuration to file."""
        with open(self.config_file, 'w') as f:
            self.parser.write(f)
        print(f"✓ Configuration saved to {self.config_file}")
    
    def create_default_config(self):
        """Create a default config.ini file with comments."""
        config_content = """# RimWorld Modlist Manager Configuration File
# 
# This file controls various settings for the modlist manager.
# Edit the values below to customize behavior.

[Paths]
# Directory where .rwpackageId files are stored
database_dir = rwpackageId_database

# Default directory for RimWorld mods (used if not specified)
default_mods_dir = ./mods

# Default directory for output XML files
default_output_dir = .

[RimWorld]
# Default RimWorld version string for XML files
default_version = 1.5.4104 rev415

# Whether to include expansions by default (true/false)
include_expansions = true

# Comma-separated list of expansion package IDs
expansions = ludeon.rimworld,ludeon.rimworld.royalty,ludeon.rimworld.ideology,ludeon.rimworld.biotech,ludeon.rimworld.anomaly,ludeon.rimworld.odyssey

[Display]
# Maximum number of files to show when listing (0 = unlimited)
max_files_listed = 20

# Maximum number of warning lines to show (for missing mods)
max_warning_lines = 10

[Merge]
# Default name for merged ID lists
default_merged_name = merged_list
"""
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        # Re-read the file
        self.parser.read(self.config_file)
        print(f"✓ Created default configuration file: {self.config_file}")
    
    # Paths
    @property
    def database_dir(self) -> str:
        """Get the database directory path."""
        return self.parser.get('Paths', 'database_dir', fallback='rwpackageId_database')
    
    @property
    def default_mods_dir(self) -> str:
        """Get the default mods directory path."""
        return self.parser.get('Paths', 'default_mods_dir', fallback='./mods')
    
    @property
    def default_output_dir(self) -> str:
        """Get the default output directory path."""
        return self.parser.get('Paths', 'default_output_dir', fallback='.')
    
    # RimWorld
    @property
    def default_version(self) -> str:
        """Get the default RimWorld version."""
        return self.parser.get('RimWorld', 'default_version', fallback='1.5.4104 rev415')
    
    @property
    def include_expansions(self) -> bool:
        """Get whether to include expansions by default."""
        return self.parser.getboolean('RimWorld', 'include_expansions', fallback=True)
    
    @property
    def expansions(self) -> List[str]:
        """Get the list of expansion package IDs."""
        expansions_str = self.parser.get('RimWorld', 'expansions', 
                                        fallback='ludeon.rimworld,ludeon.rimworld.royalty,ludeon.rimworld.ideology,ludeon.rimworld.biotech,ludeon.rimworld.anomaly,ludeon.rimworld.odyssey')
        return [exp.strip() for exp in expansions_str.split(',') if exp.strip()]
    
    # Display
    @property
    def max_files_listed(self) -> int:
        """Get the maximum number of files to list (0 = unlimited)."""
        return self.parser.getint('Display', 'max_files_listed', fallback=20)
    
    @property
    def max_warning_lines(self) -> int:
        """Get the maximum number of warning lines to show."""
        return self.parser.getint('Display', 'max_warning_lines', fallback=10)
    
    # Merge
    @property
    def default_merged_name(self) -> str:
        """Get the default name for merged lists."""
        return self.parser.get('Merge', 'default_merged_name', fallback='merged_list')


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config():
    """Reload the configuration from file."""
    global _config
    _config = Config()
    return _config
