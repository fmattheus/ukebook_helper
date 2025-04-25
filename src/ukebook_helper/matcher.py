"""
Fuzzy matching functionality for finding songs
"""
from typing import Dict, List, NamedTuple
from thefuzz import fuzz
from .models import Song, InputSong


class Match(NamedTuple):
    """Represents a potential match between an input song and a website song."""
    display_name: str  # The display name from the website
    song: Song        # The matched song from the website
    similarity: int   # The similarity score (0-100)


def find_matches(input_song: InputSong, available_songs: Dict[str, Song], threshold: int = 60) -> List[Match]:
    """
    Find potential matches for an input song from the available songs.

    Args:
        input_song: The song from the input list to match
        available_songs: Dictionary of songs from the website
        threshold: Minimum similarity score (0-100) to consider a match

    Returns:
        List of potential matches, sorted by similarity score (lowest first)
    """
    matches = []

    # Create the search string in the same format as the website
    search_string = f"{input_song.title} - {input_song.artist}"

    # Try matching against each available song
    for display_name, song in available_songs.items():
        # Calculate similarity using token sort ratio to handle word order differences
        similarity = fuzz.ratio(search_string, display_name)

        if similarity >= threshold:
            matches.append(Match(
                display_name=display_name,
                song=song,
                similarity=similarity
            ))

    # Sort matches by similarity score (lowest first)
    return sorted(matches, key=lambda x: x.similarity)
