"""
Steam Workshop collection utilities.
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple


def extract_collection_id(url_or_id: str) -> Optional[str]:
    """
    Extract collection ID from a Steam Workshop URL or return the ID if already provided.
    
    Args:
        url_or_id: Steam Workshop collection URL or collection ID
        
    Returns:
        Collection ID string, or None if invalid
    """
    # If it's just a number, return it
    if url_or_id.isdigit():
        return url_or_id
    
    # Try to extract ID from URL
    match = re.search(r'[?&]id=(\d+)', url_or_id)
    if match:
        return match.group(1)
    
    return None


def fetch_collection_details(collection_id: str) -> Tuple[str, List[str]]:
    """
    Fetch Steam Workshop collection details and extract mod IDs.
    
    Args:
        collection_id: Steam Workshop collection ID
        
    Returns:
        Tuple of (collection_title, list_of_mod_ids)
        
    Raises:
        Exception if unable to fetch or parse the collection
    """
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={collection_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch collection URL: {e}")
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract collection title
    title_elem = soup.find("div", class_="workshopItemTitle")
    if not title_elem:
        raise Exception("Could not find collection title. Make sure this is a valid Steam Workshop collection.")
    
    collection_title = title_elem.get_text(strip=True)
    
    # Extract mod IDs from collection items
    id_nodes = soup.find_all("div", class_="collectionItem")
    mod_ids = []
    
    for node in id_nodes:
        if node.has_attr("id"):
            # ID format is "sharedfile_XXXXXXXXXX"
            full_id = node.get("id")
            if full_id.startswith("sharedfile_"):
                mod_id = full_id[11:]  # Remove "sharedfile_" prefix
                mod_ids.append(mod_id)
    
    if not mod_ids:
        raise Exception("No mods found in this collection. It may be empty or private.")
    
    return collection_title, mod_ids
