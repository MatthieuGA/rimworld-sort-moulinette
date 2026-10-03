#!/usr/bin/python3
"""
RimSort Modlist Manager - GUI Application

A graphical interface for managing RimSort modlists using DearPyGui.
"""

import dearpygui.dearpygui as dpg
import os
import sys
import threading
from typing import Optional, List

# Native OS file dialogs (tkinter may be missing on some Linux Python builds)
try:
    import tkinter
    from tkinter import filedialog
except ImportError:
    tkinter = None

# Import our existing modules
from config import get_config
from steam_workshop import extract_collection_id, fetch_collection_details
from mod_utils import convert_workshop_ids_to_package_ids, convert_package_ids_to_workshop_ids
from utils import create_modlist_xml, read_modlist_xml, write_workshop_ids_file
from moulinette import get_rwpackageid_output_name
import main as main_module  # Renamed to avoid conflict with main() function


def native_dialog(dialog_name: str, **options) -> Optional[str]:
    """
    Open a native OS file dialog through tkinter.

    Args:
        dialog_name: Name of the tkinter.filedialog function (e.g. 'askdirectory')
        **options: Options passed to the dialog (title, initialdir, filetypes...)

    Returns:
        Selected path, "" if cancelled, or None if native dialogs are unavailable
    """
    if tkinter is None:
        return None

    try:
        root = tkinter.Tk()
    except tkinter.TclError:
        return None

    try:
        # Hidden root window, kept on top so the dialog doesn't open behind the app
        root.withdraw()
        root.attributes("-topmost", True)
        return getattr(filedialog, dialog_name)(parent=root, **options) or ""
    finally:
        root.destroy()


class RimWorldModlistGUI:
    """Main GUI application class."""

    def __init__(self):
        """Initialize the GUI application."""
        self.config = get_config()
        self.current_operation = None
        self.selected_base_file = None
        self.selected_removal_file = None

        # Create DearPyGui context
        dpg.create_context()

        # Setup GUI
        self._setup_theme()
        self._create_main_window()

        # Setup viewport
        dpg.create_viewport(
            title="RimWSort Modlist Manager",
            width=1000,
            height=850,
            min_width=800,
            min_height=700
        )
        dpg.setup_dearpygui()

    def _setup_theme(self):
        """Setup custom theme for the application."""
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (15, 15, 15))
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (20, 20, 20))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (30, 30, 30))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (70, 100, 150))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (90, 120, 170))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (60, 90, 140))
                dpg.add_theme_color(dpg.mvThemeCol_Header, (70, 100, 150))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (90, 120, 170))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 4)

        dpg.bind_theme(global_theme)

    def _create_main_window(self):
        """Create the main application window."""
        with dpg.window(label="RimWorld Modlist Manager", tag="main_window",
                       no_close=True, no_collapse=True):

            # Title
            dpg.add_text("RimWorld Modlist Manager", tag="title")
            with dpg.theme() as title_theme:
                with dpg.theme_component(dpg.mvText):
                    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 10)
            dpg.bind_item_theme("title", title_theme)

            dpg.add_separator()
            dpg.add_spacer(height=10)

            # Main tabs
            with dpg.tab_bar():
                # Tab 1: Create from Collection
                with dpg.tab(label="📥 Create from Collection"):
                    self._create_collection_tab()

                # Tab 2: Convert to XML
                with dpg.tab(label="🔄 Convert to XML"):
                    self._create_convert_tab()

                # Tab 3: XML back to ID list
                with dpg.tab(label="↩️ XML to ID List"):
                    self._create_reverse_tab()

                # Tab 4: Merge Lists
                with dpg.tab(label="🔗 Merge Lists"):
                    self._create_merge_tab()

                # Tab 5: Remove IDs
                with dpg.tab(label="✂️ Remove IDs"):
                    self._create_remove_tab()

                # Tab 6: Settings
                with dpg.tab(label="⚙️ Settings"):
                    self._create_settings_tab()

            dpg.add_spacer(height=10)
            dpg.add_separator()

            # Status bar at bottom
            with dpg.group(horizontal=True):
                dpg.add_text("Status:", color=(150, 150, 150))
                dpg.add_text("Ready", tag="status_text", color=(100, 200, 100))

    def _create_collection_tab(self):
        """Create the 'Create from Collection' tab."""
        dpg.add_text("Fetch Workshop IDs from a Steam Workshop collection")
        dpg.add_spacer(height=10)

        with dpg.group():
            dpg.add_text("Collection URL or ID:")
            dpg.add_input_text(
                tag="collection_input",
                hint="Enter Steam Workshop collection URL or ID",
                width=600
            )

            dpg.add_spacer(height=10)
            dpg.add_text("Output Name:")
            dpg.add_input_text(
                tag="collection_output_name",
                hint="Leave empty to use collection title",
                width=600
            )

            dpg.add_spacer(height=10)
            dpg.add_button(
                label="Fetch Collection",
                callback=self._fetch_collection,
                width=200,
                height=30
            )

            dpg.add_spacer(height=20)
            dpg.add_separator()
            dpg.add_spacer(height=10)

            # Results area
            dpg.add_text("Results:", color=(150, 150, 150))
            dpg.add_child_window(
                tag="collection_results",
                width=-1,
                height=300,
                border=True
            )

    def _create_convert_tab(self):
        """Create the 'Convert to XML' tab."""
        dpg.add_text("Convert a .rwpackageId file to RimWorld modlist XML")
        dpg.add_spacer(height=10)

        with dpg.group():
            dpg.add_text("Select .rwpackageId file:")
            dpg.add_listbox(
                tag="convert_file_list",
                items=[],
                num_items=10,
                width=600,
                callback=self._on_convert_file_selected
            )
            dpg.add_button(
                label="Refresh List",
                callback=self._refresh_convert_list,
                width=150
            )

            dpg.add_spacer(height=10)
            dpg.add_text("Mods Directory:")
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    tag="mods_dir_input",
                    default_value=self.config.default_mods_dir,
                    width=500
                )
                dpg.add_button(
                    label="Browse",
                    callback=self._browse_mods_dir,
                    user_data=("mods_dir_input", "mods_dir_dialog")
                )
                dpg.add_button(
                    label="Save as Default",
                    callback=self._save_mods_dir_as_default,
                    user_data="mods_dir_input"
                )

            dpg.add_spacer(height=10)
            dpg.add_text("Output XML Name:")
            dpg.add_input_text(
                tag="convert_output_name",
                hint="Leave empty to use input name",
                width=600
            )

            dpg.add_spacer(height=10)
            dpg.add_button(
                label="Convert to XML",
                callback=self._convert_to_xml,
                width=200,
                height=30
            )

            dpg.add_spacer(height=20)
            dpg.add_separator()
            dpg.add_spacer(height=10)

            # Progress area
            dpg.add_text("Progress:", color=(150, 150, 150))
            dpg.add_child_window(
                tag="convert_progress",
                width=-1,
                height=200,
                border=True
            )

        # Fallback file dialog for mods directory (when native dialogs are unavailable)
        with dpg.file_dialog(
            directory_selector=True,
            show=False,
            callback=self._on_mods_dir_selected,
            user_data="mods_dir_input",
            tag="mods_dir_dialog",
            width=700,
            height=400
        ):
            dpg.add_file_extension(".*")

        # Refresh the list initially
        self._refresh_convert_list()

    def _create_reverse_tab(self):
        """Create the 'XML to ID List' tab."""
        dpg.add_text("Convert a RimWorld modlist XML back to a .rwpackageId file")
        dpg.add_spacer(height=10)

        with dpg.group():
            dpg.add_text("Modlist XML File:")
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    tag="reverse_xml_input",
                    hint="Path to a RimSort/RimWorld modlist XML",
                    width=500
                )
                dpg.add_button(
                    label="Browse",
                    callback=self._browse_reverse_xml
                )

            dpg.add_spacer(height=10)
            dpg.add_text("Mods Directory:")
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    tag="reverse_mods_dir_input",
                    default_value=self.config.default_mods_dir,
                    width=500
                )
                dpg.add_button(
                    label="Browse",
                    callback=self._browse_mods_dir,
                    user_data=("reverse_mods_dir_input", "reverse_mods_dir_dialog")
                )
                dpg.add_button(
                    label="Save as Default",
                    callback=self._save_mods_dir_as_default,
                    user_data="reverse_mods_dir_input"
                )

            dpg.add_spacer(height=10)
            dpg.add_text("Output ID List Name:")
            dpg.add_input_text(
                tag="reverse_output_name",
                hint="Leave empty to use XML name",
                width=600
            )

            dpg.add_spacer(height=10)
            dpg.add_button(
                label="Convert to ID List",
                callback=self._convert_from_xml,
                width=200,
                height=30
            )

            dpg.add_spacer(height=20)
            dpg.add_separator()
            dpg.add_spacer(height=10)

            # Progress area
            dpg.add_text("Progress:", color=(150, 150, 150))
            dpg.add_child_window(
                tag="reverse_progress",
                width=-1,
                height=200,
                border=True
            )

        # Fallback file dialogs (when native dialogs are unavailable)
        with dpg.file_dialog(
            show=False,
            callback=self._on_reverse_xml_selected,
            tag="reverse_xml_dialog",
            width=700,
            height=400
        ):
            dpg.add_file_extension(".xml")
            dpg.add_file_extension(".*")

        with dpg.file_dialog(
            directory_selector=True,
            show=False,
            callback=self._on_mods_dir_selected,
            user_data="reverse_mods_dir_input",
            tag="reverse_mods_dir_dialog",
            width=700,
            height=400
        ):
            dpg.add_file_extension(".*")

    def _create_merge_tab(self):
        """Create the 'Merge Lists' tab."""
        dpg.add_text("Merge two .rwpackageId files (removes duplicates)")
        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            # Left column - First file
            with dpg.child_window(width=400, height=400, border=True):
                dpg.add_text("First List:", color=(100, 200, 255))
                dpg.add_listbox(
                    tag="merge_file1_list",
                    items=[],
                    num_items=15,
                    width=-1
                )

            dpg.add_spacer(width=20)

            # Right column - Second file
            with dpg.child_window(width=400, height=400, border=True):
                dpg.add_text("Second List:", color=(255, 200, 100))
                dpg.add_listbox(
                    tag="merge_file2_list",
                    items=[],
                    num_items=15,
                    width=-1
                )

        dpg.add_spacer(height=10)
        dpg.add_button(
            label="Refresh Lists",
            callback=self._refresh_merge_lists,
            width=150
        )

        dpg.add_spacer(height=10)
        dpg.add_text("Output Name:")
        dpg.add_input_text(
            tag="merge_output_name",
            default_value=self.config.default_merged_name,
            width=600
        )

        dpg.add_spacer(height=10)
        dpg.add_button(
            label="Merge Lists",
            callback=self._merge_lists,
            width=200,
            height=30
        )

        dpg.add_spacer(height=10)
        dpg.add_text("", tag="merge_result", color=(100, 255, 100))

        # Refresh the lists initially
        self._refresh_merge_lists()

    def _create_remove_tab(self):
        """Create the 'Remove IDs' tab."""
        dpg.add_text("Remove IDs from one list based on another list")
        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            # Left column - Base list
            with dpg.child_window(width=400, height=400, border=True):
                dpg.add_text("BASE List (to keep):", color=(100, 255, 100))
                dpg.add_listbox(
                    tag="remove_base_list",
                    items=[],
                    num_items=15,
                    width=-1
                )

            dpg.add_spacer(width=20)

            # Right column - Removal list
            with dpg.child_window(width=400, height=400, border=True):
                dpg.add_text("REMOVAL List (to subtract):", color=(255, 100, 100))
                dpg.add_listbox(
                    tag="remove_removal_list",
                    items=[],
                    num_items=15,
                    width=-1
                )

        dpg.add_spacer(height=10)
        dpg.add_button(
            label="Refresh Lists",
            callback=self._refresh_remove_lists,
            width=150
        )

        dpg.add_spacer(height=10)
        dpg.add_text("Output Name:")
        dpg.add_input_text(
            tag="remove_output_name",
            hint="Name for filtered list",
            width=600
        )

        dpg.add_spacer(height=10)
        dpg.add_button(
            label="Remove IDs from Base",
            callback=self._remove_ids,
            width=200,
            height=30
        )

        dpg.add_spacer(height=10)
        dpg.add_text("", tag="remove_result", color=(100, 255, 100))

        # Refresh the lists initially
        self._refresh_remove_lists()

    def _create_settings_tab(self):
        """Create the Settings tab."""
        dpg.add_text("Application Settings")
        dpg.add_spacer(height=10)

        with dpg.child_window(width=-1, height=-50, border=True):
            dpg.add_text("Paths", color=(100, 200, 255))
            dpg.add_separator()
            dpg.add_spacer(height=5)

            dpg.add_text("Database Directory:")
            dpg.add_input_text(
                tag="setting_database_dir",
                default_value=self.config.database_dir,
                width=600
            )

            dpg.add_spacer(height=5)
            dpg.add_text("Default Mods Directory:")
            dpg.add_input_text(
                tag="setting_mods_dir",
                default_value=self.config.default_mods_dir,
                width=600
            )

            dpg.add_spacer(height=15)
            dpg.add_text("Display", color=(100, 200, 255))
            dpg.add_separator()
            dpg.add_spacer(height=5)

            dpg.add_text("Max Files Listed (0 = unlimited):")
            dpg.add_input_int(
                tag="setting_max_files",
                default_value=self.config.max_files_listed,
                width=200
            )

            dpg.add_spacer(height=5)
            dpg.add_text("Max Warning Lines (0 = unlimited):")
            dpg.add_input_int(
                tag="setting_max_warnings",
                default_value=self.config.max_warning_lines,
                width=200
            )

            dpg.add_spacer(height=15)
            dpg.add_text("RimWorld", color=(100, 200, 255))
            dpg.add_separator()
            dpg.add_spacer(height=5)

            dpg.add_text("Default Version:")
            dpg.add_input_text(
                tag="setting_version",
                default_value=self.config.default_version,
                width=400
            )

            dpg.add_spacer(height=5)
            dpg.add_checkbox(
                label="Include Expansions by Default",
                tag="setting_include_expansions",
                default_value=self.config.include_expansions
            )

        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Save Settings",
                callback=self._save_settings,
                width=150
            )
            dpg.add_button(
                label="Reset to Defaults",
                callback=self._reset_settings,
                width=150
            )

    # Callback methods

    def _update_status(self, message: str, color=(100, 200, 100)):
        """Update the status bar."""
        dpg.set_value("status_text", message)
        dpg.configure_item("status_text", color=color)

    def _append_to_window(self, tag: str, text: str, color=(255, 255, 255)):
        """Append text to a child window."""
        dpg.add_text(text, parent=tag, color=color)
        # Auto-scroll to bottom
        dpg.set_y_scroll(tag, -1)

    def _clear_window(self, tag: str):
        """Clear all items from a child window."""
        dpg.delete_item(tag, children_only=True)

    def _fetch_collection(self):
        """Fetch a Steam Workshop collection."""
        collection_input = dpg.get_value("collection_input")
        output_name = dpg.get_value("collection_output_name")

        if not collection_input:
            self._update_status("Please enter a collection URL or ID", (255, 100, 100))
            return

        # Clear previous results
        self._clear_window("collection_results")
        self._update_status("Fetching collection...", (255, 200, 100))

        def fetch_thread():
            nonlocal output_name
            try:
                # Extract collection ID
                collection_id = extract_collection_id(collection_input)
                if not collection_id:
                    self._append_to_window(
                        "collection_results",
                        f"❌ Invalid collection URL or ID: {collection_input}",
                        (255, 100, 100)
                    )
                    self._update_status("Error: Invalid collection", (255, 100, 100))
                    return

                self._append_to_window(
                    "collection_results",
                    f"Fetching collection {collection_id}...",
                    (255, 200, 100)
                )

                # Fetch collection details
                collection_title, workshop_ids = fetch_collection_details(collection_id)

                self._append_to_window(
                    "collection_results",
                    f"✓ Found collection: {collection_title}",
                    (100, 255, 100)
                )
                self._append_to_window(
                    "collection_results",
                    f"✓ Contains {len(workshop_ids)} mod(s)",
                    (100, 255, 100)
                )

                # Determine output name
                if not output_name:
                    output_name = main_module.sanitize_filename(collection_title)

                # Save to file
                output_path = main_module.get_rwpackageid_path(output_name)
                main_module.write_workshop_ids_file(output_path, workshop_ids, collection_title)

                self._append_to_window(
                    "collection_results",
                    f"✓ Saved to: {output_path}",
                    (100, 255, 100)
                )

                self._update_status("Collection fetched successfully!", (100, 255, 100))

                # Refresh convert list
                self._refresh_convert_list()

            except Exception as e:
                self._append_to_window(
                    "collection_results",
                    f"❌ Error: {str(e)}",
                    (255, 100, 100)
                )
                self._update_status(f"Error: {str(e)}", (255, 100, 100))

        # Run in thread to not block UI
        thread = threading.Thread(target=fetch_thread, daemon=True)
        thread.start()

    def _refresh_convert_list(self):
        """Refresh the list of .rwpackageId files."""
        files = main_module.list_rwpackageid_files()
        dpg.configure_item("convert_file_list", items=files if files else ["No files found"])

    def _on_convert_file_selected(self):
        """Handle file selection in convert tab."""
        selected = dpg.get_value("convert_file_list")
        if selected and selected != "No files found":
            # Auto-fill output name
            output_name = selected.replace('.rwpackageId', '.xml')
            dpg.set_value("convert_output_name", output_name)

    def _browse_mods_dir(self, sender, app_data, user_data):
        """Pick a mods directory (user_data is (input tag, fallback dialog tag))."""
        input_tag, fallback_dialog_tag = user_data
        current = dpg.get_value(input_tag)

        path = native_dialog(
            "askdirectory",
            title="Select Mods Directory",
            initialdir=current if os.path.isdir(current) else None,
            mustexist=True
        )
        if path is None:
            dpg.show_item(fallback_dialog_tag)
        elif path:
            dpg.set_value(input_tag, os.path.normpath(path))

    def _on_mods_dir_selected(self, sender, app_data, user_data):
        """Handle mods directory selection (user_data is the input to fill)."""
        selections = app_data.get('selections', {})
        if selections:
            path = list(selections.values())[0]
            dpg.set_value(user_data, path)

    def _convert_to_xml(self):
        """Convert selected .rwpackageId to XML."""
        selected_file = dpg.get_value("convert_file_list")
        mods_dir = dpg.get_value("mods_dir_input")
        output_name = dpg.get_value("convert_output_name")

        if not selected_file or selected_file == "No files found":
            self._update_status("Please select a file to convert", (255, 100, 100))
            return

        if not os.path.exists(mods_dir):
            self._update_status("Mods directory does not exist", (255, 100, 100))
            return

        # Clear previous progress
        self._clear_window("convert_progress")
        self._update_status("Converting to XML...", (255, 200, 100))

        def convert_thread():
            nonlocal output_name
            try:
                # Get full path
                input_file = os.path.join(self.config.database_dir, selected_file)

                self._append_to_window(
                    "convert_progress",
                    f"Reading Workshop IDs from: {selected_file}",
                    (200, 200, 200)
                )

                # Read Workshop IDs
                workshop_ids = main_module.read_workshop_ids_file(input_file)
                self._append_to_window(
                    "convert_progress",
                    f"✓ Found {len(workshop_ids)} Workshop ID(s)",
                    (100, 255, 100)
                )

                # Convert to package IDs
                self._append_to_window(
                    "convert_progress",
                    f"Reading package IDs from: {mods_dir}",
                    (200, 200, 200)
                )

                package_ids = convert_workshop_ids_to_package_ids(workshop_ids, mods_dir)

                self._append_to_window(
                    "convert_progress",
                    f"✓ Converted to package IDs",
                    (100, 255, 100)
                )

                # Determine output name
                if not output_name:
                    output_name = selected_file.replace('.rwpackageId', '.xml')
                elif not output_name.endswith('.xml'):
                    output_name = f"{output_name}.xml"

                # Create XML
                self._append_to_window(
                    "convert_progress",
                    "Generating XML...",
                    (200, 200, 200)
                )

                create_modlist_xml(
                    package_ids=package_ids,
                    output_path=output_name,
                    version=None,  # Use config default
                    expansions=None  # Use config default
                )

                self._append_to_window(
                    "convert_progress",
                    f"✓ Modlist XML saved to: {output_name}",
                    (100, 255, 100)
                )

                self._update_status("Conversion completed successfully!", (100, 255, 100))

            except Exception as e:
                self._append_to_window(
                    "convert_progress",
                    f"❌ Error: {str(e)}",
                    (255, 100, 100)
                )
                self._update_status(f"Error: {str(e)}", (255, 100, 100))

        # Run in thread to not block UI
        thread = threading.Thread(target=convert_thread, daemon=True)
        thread.start()

    def _save_mods_dir_as_default(self, sender, app_data, user_data):
        """Save a mods directory input (user_data is its tag) as default_mods_dir in config.ini."""
        mods_dir = dpg.get_value(user_data).strip()

        if not os.path.isdir(mods_dir):
            self._update_status("Mods directory does not exist", (255, 100, 100))
            return

        try:
            self.config.parser['Paths']['default_mods_dir'] = mods_dir
            self.config.save()

            # Keep the Settings tab in sync so "Save Settings" doesn't revert it
            dpg.set_value("setting_mods_dir", mods_dir)

            self._update_status(f"Default mods directory saved: {mods_dir}", (100, 255, 100))

        except Exception as e:
            self._update_status(f"Error saving settings: {str(e)}", (255, 100, 100))

    def _browse_reverse_xml(self):
        """Pick a modlist XML in reverse tab."""
        current_dir = os.path.dirname(dpg.get_value("reverse_xml_input").strip().strip('"'))

        path = native_dialog(
            "askopenfilename",
            title="Select Modlist XML",
            initialdir=current_dir if os.path.isdir(current_dir) else self.config.default_output_dir,
            filetypes=[("Modlist XML", "*.xml"), ("All files", "*.*")]
        )
        if path is None:
            dpg.show_item("reverse_xml_dialog")
        elif path:
            self._set_reverse_xml(os.path.normpath(path))

    def _on_reverse_xml_selected(self, sender, app_data):
        """Handle modlist XML selection in reverse tab (fallback dialog)."""
        selections = app_data.get('selections', {})
        path = list(selections.values())[0] if selections else app_data.get('file_path_name')
        if path:
            self._set_reverse_xml(path)

    def _set_reverse_xml(self, path: str):
        """Fill the reverse tab XML input and auto-fill the output name."""
        dpg.set_value("reverse_xml_input", path)
        dpg.set_value("reverse_output_name", get_rwpackageid_output_name(path))

    def _convert_from_xml(self):
        """Convert a modlist XML back to a .rwpackageId file."""
        xml_path = dpg.get_value("reverse_xml_input").strip().strip('"')
        mods_dir = dpg.get_value("reverse_mods_dir_input")
        output_name = dpg.get_value("reverse_output_name")

        if not xml_path or not os.path.isfile(xml_path):
            self._update_status("Please select an existing modlist XML file", (255, 100, 100))
            return

        if not os.path.isdir(mods_dir):
            self._update_status("Mods directory does not exist", (255, 100, 100))
            return

        # Clear previous progress
        self._clear_window("reverse_progress")
        self._update_status("Converting to ID list...", (255, 200, 100))

        def reverse_thread():
            nonlocal output_name
            try:
                self._append_to_window(
                    "reverse_progress",
                    f"Reading package IDs from: {os.path.basename(xml_path)}",
                    (200, 200, 200)
                )

                package_ids = read_modlist_xml(xml_path)
                self._append_to_window(
                    "reverse_progress",
                    f"✓ Found {len(package_ids)} package ID(s)",
                    (100, 255, 100)
                )

                # Convert to Workshop IDs
                self._append_to_window(
                    "reverse_progress",
                    f"Indexing mod folders in: {mods_dir}",
                    (200, 200, 200)
                )

                workshop_ids, unresolved = convert_package_ids_to_workshop_ids(package_ids, mods_dir)

                self._append_to_window(
                    "reverse_progress",
                    f"✓ Resolved {len(workshop_ids)} Workshop ID(s)",
                    (100, 255, 100)
                )

                if unresolved:
                    self._append_to_window(
                        "reverse_progress",
                        f"⚠ {len(unresolved)} package ID(s) not found in mods directory "
                        f"(kept as comments in the output file):",
                        (255, 200, 100)
                    )
                    max_lines = self.config.max_warning_lines
                    shown = unresolved if max_lines == 0 else unresolved[:max_lines]
                    for package_id in shown:
                        self._append_to_window("reverse_progress", f"   - {package_id}", (255, 200, 100))
                    if len(shown) < len(unresolved):
                        self._append_to_window(
                            "reverse_progress",
                            f"   ... and {len(unresolved) - len(shown)} more",
                            (255, 200, 100)
                        )

                if not workshop_ids:
                    self._append_to_window(
                        "reverse_progress",
                        "❌ No Workshop IDs could be resolved, nothing saved",
                        (255, 100, 100)
                    )
                    self._update_status("Error: No Workshop IDs resolved", (255, 100, 100))
                    return

                # Determine output name
                if not output_name:
                    output_name = get_rwpackageid_output_name(xml_path)

                # Save
                output_path = main_module.get_rwpackageid_path(output_name)
                write_workshop_ids_file(
                    output_path,
                    workshop_ids,
                    f"Imported from {os.path.basename(xml_path)}",
                    unresolved
                )

                self._append_to_window(
                    "reverse_progress",
                    f"✓ Saved to: {output_path}",
                    (100, 255, 100)
                )

                self._update_status("Conversion completed successfully!", (100, 255, 100))

                # Make the new ID list available in the other tabs
                self._refresh_convert_list()
                self._refresh_merge_lists()
                self._refresh_remove_lists()

            except Exception as e:
                self._append_to_window(
                    "reverse_progress",
                    f"❌ Error: {str(e)}",
                    (255, 100, 100)
                )
                self._update_status(f"Error: {str(e)}", (255, 100, 100))

        # Run in thread to not block UI
        thread = threading.Thread(target=reverse_thread, daemon=True)
        thread.start()

    def _refresh_merge_lists(self):
        """Refresh the merge file lists."""
        files = main_module.list_rwpackageid_files()
        items = files if files else ["No files found"]
        dpg.configure_item("merge_file1_list", items=items)
        dpg.configure_item("merge_file2_list", items=items)

    def _merge_lists(self):
        """Merge two selected lists."""
        file1 = dpg.get_value("merge_file1_list")
        file2 = dpg.get_value("merge_file2_list")
        output_name = dpg.get_value("merge_output_name")

        if not file1 or file1 == "No files found":
            self._update_status("Please select first file", (255, 100, 100))
            return

        if not file2 or file2 == "No files found":
            self._update_status("Please select second file", (255, 100, 100))
            return

        if not output_name:
            self._update_status("Please enter output name", (255, 100, 100))
            return

        self._update_status("Merging lists...", (255, 200, 100))

        try:
            # Read both files
            file1_path = os.path.join(self.config.database_dir, file1)
            file2_path = os.path.join(self.config.database_dir, file2)

            ids1 = main_module.read_workshop_ids_file(file1_path)
            ids2 = main_module.read_workshop_ids_file(file2_path)

            # Merge and remove duplicates
            seen = set()
            merged_ids = []
            for workshop_id in ids1 + ids2:
                if workshop_id not in seen:
                    seen.add(workshop_id)
                    merged_ids.append(workshop_id)

            duplicates = len(ids1) + len(ids2) - len(merged_ids)

            # Save
            output_path = main_module.get_rwpackageid_path(output_name)
            main_module.write_workshop_ids_file(output_path, merged_ids, "Merged ID List")

            result_text = (
                f"✓ Merged successfully!\n"
                f"File 1: {len(ids1)} IDs\n"
                f"File 2: {len(ids2)} IDs\n"
                f"Result: {len(merged_ids)} unique IDs\n"
                f"Removed {duplicates} duplicate(s)\n"
                f"Saved to: {output_path}"
            )
            dpg.set_value("merge_result", result_text)

            self._update_status("Lists merged successfully!", (100, 255, 100))

        except Exception as e:
            dpg.set_value("merge_result", f"❌ Error: {str(e)}")
            self._update_status(f"Error: {str(e)}", (255, 100, 100))

    def _refresh_remove_lists(self):
        """Refresh the remove file lists."""
        files = main_module.list_rwpackageid_files()
        items = files if files else ["No files found"]
        dpg.configure_item("remove_base_list", items=items)
        dpg.configure_item("remove_removal_list", items=items)

    def _remove_ids(self):
        """Remove IDs from base list."""
        base_file = dpg.get_value("remove_base_list")
        removal_file = dpg.get_value("remove_removal_list")
        output_name = dpg.get_value("remove_output_name")

        if not base_file or base_file == "No files found":
            self._update_status("Please select BASE file", (255, 100, 100))
            return

        if not removal_file or removal_file == "No files found":
            self._update_status("Please select REMOVAL file", (255, 100, 100))
            return

        # Assign default output name if empty
        if not output_name:
            output_name = base_file.replace('.rwpackageId', '_filtered')

        self._update_status("Removing IDs...", (255, 200, 100))

        try:
            # Read both files
            base_path = os.path.join(self.config.database_dir, base_file)
            removal_path = os.path.join(self.config.database_dir, removal_file)

            base_ids = main_module.read_workshop_ids_file(base_path)
            removal_ids = main_module.read_workshop_ids_file(removal_path)

            # Remove IDs
            removal_set = set(removal_ids)
            filtered_ids = [wid for wid in base_ids if wid not in removal_set]

            removed_count = len(base_ids) - len(filtered_ids)

            if len(filtered_ids) == 0:
                dpg.set_value("remove_result", "⚠ Warning: Result would be empty. Operation cancelled.")
                self._update_status("Operation cancelled - result would be empty", (255, 200, 100))
                return

            # Save
            output_path = main_module.get_rwpackageid_path(output_name)
            main_module.write_workshop_ids_file(
                output_path,
                filtered_ids,
                f"Filtered ID List (removed {removed_count} IDs)"
            )

            result_text = (
                f"✓ IDs removed successfully!\n"
                f"Base: {len(base_ids)} IDs\n"
                f"Removal: {len(removal_ids)} IDs\n"
                f"Result: {len(filtered_ids)} IDs\n"
                f"Removed: {removed_count} ID(s)\n"
                f"Saved to: {output_path}"
            )
            dpg.set_value("remove_result", result_text)

            self._update_status("IDs removed successfully!", (100, 255, 100))

        except Exception as e:
            dpg.set_value("remove_result", f"❌ Error: {str(e)}")
            self._update_status(f"Error: {str(e)}", (255, 100, 100))

    def _save_settings(self):
        """Save settings to config file."""
        try:
            # Update config values
            self.config.parser['Paths']['database_dir'] = dpg.get_value("setting_database_dir")
            self.config.parser['Paths']['default_mods_dir'] = dpg.get_value("setting_mods_dir")
            self.config.parser['Display']['max_files_listed'] = str(dpg.get_value("setting_max_files"))
            self.config.parser['Display']['max_warning_lines'] = str(dpg.get_value("setting_max_warnings"))
            self.config.parser['RimWorld']['default_version'] = dpg.get_value("setting_version")
            self.config.parser['RimWorld']['include_expansions'] = str(dpg.get_value("setting_include_expansions")).lower()

            # Save to file
            self.config.save()

            self._update_status("Settings saved successfully!", (100, 255, 100))

        except Exception as e:
            self._update_status(f"Error saving settings: {str(e)}", (255, 100, 100))

    def _reset_settings(self):
        """Reset settings to defaults."""
        try:
            self.config.create_default_config()

            # Update UI
            dpg.set_value("setting_database_dir", self.config.database_dir)
            dpg.set_value("setting_mods_dir", self.config.default_mods_dir)
            dpg.set_value("setting_max_files", self.config.max_files_listed)
            dpg.set_value("setting_max_warnings", self.config.max_warning_lines)
            dpg.set_value("setting_version", self.config.default_version)
            dpg.set_value("setting_include_expansions", self.config.include_expansions)

            self._update_status("Settings reset to defaults!", (100, 255, 100))

        except Exception as e:
            self._update_status(f"Error resetting settings: {str(e)}", (255, 100, 100))

    def run(self):
        """Run the application."""
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()


def main():
    """Main entry point for GUI application."""
    app = RimWorldModlistGUI()
    app.run()


if __name__ == '__main__':
    main()
