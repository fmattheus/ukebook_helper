"""
Data models and file handling for Ukebook Helper
"""
from typing import List, NamedTuple
from pathlib import Path


class Song(NamedTuple):
    """Represents a song from the website."""
    title: str
    artist: str
    href: str


class InputSong(NamedTuple):
    """Represents a song from the input list file."""
    title: str
    artist: str
    gema_nr: str
    leader: str


def read_input_list(filepath: str) -> List[InputSong | str]:
    """
    Read and parse the input.list file.

    Args:
        filepath: Path to the input.list file

    Returns:
        List[InputSong | str]: List of songs and break markers from the input file
    """
    songs = []
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Split by tabs and clean up each field
            parts = [part.strip() for part in line.split('\t')]

            # Handle "Break" entries
            if parts[0] == "Break":
                songs.append("Break")
                continue

            # Handle regular song entries
            if len(parts) >= 4:
                songs.append(InputSong(
                    title=parts[0],
                    artist=parts[1],
                    gema_nr=parts[2],
                    leader=parts[3]
                ))

    return songs
