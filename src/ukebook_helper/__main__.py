"""
Ukebook Helper - A tool for managing Ukebook song selections
Copyright (C) 2024 Frank Mattheus

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

"""
Command line interface for Ukebook Helper
"""
import sys
import webbrowser
from pathlib import Path
from urllib.parse import urljoin
import tomli
from .client import UkebookClient
from .models import read_input_list
from .matcher import find_matches
from .ui import select_match, confirm_action, confirm_break


def read_config(config_path: str) -> dict:
    """Read and parse the TOML config file."""
    try:
        with open(config_path, 'rb') as f:
            return tomli.load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found!")
        sys.exit(1)
    except tomli.TOMLDecodeError as e:
        print(f"Error parsing config file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)


def main():
    """Main entry point for the Ukebook Helper CLI."""
    if len(sys.argv) != 2:
        print("Usage: ukebook_helper <config_file>")
        print("Example: ukebook_helper config.toml")
        sys.exit(1)

    # Read config file
    config = read_config(sys.argv[1])

    try:
        host_url = config['host_url']
        username = config['username']
        password = config['password']
    except KeyError as e:
        print(f"Error: Missing required config value: {e}")
        sys.exit(1)

    # Get optional break URL
    break_url = config.get('break_url')

    # Initialize client
    client = UkebookClient(host_url)

    # Read input list
    try:
        input_songs = read_input_list('input.list')
        print(f"Found {len(input_songs)} entries in input.list")
    except FileNotFoundError:
        print("Error: input.list file not found!")
        sys.exit(1)

    # Attempt login
    if not client.login(username, password):
        print("Login failed!")
        sys.exit(1)

    print("Successfully logged in!")

    # Fetch songs
    print("\nFetching song list...")
    available_songs = client.fetch_songs()

    if not available_songs:
        print("No songs found!")
        sys.exit(1)

    print(f"\nFound {len(available_songs)} songs on the website")

    # Open initial URLs
    if confirm_action("Open Ukebook website and songbook?"):
        if break_url:
            webbrowser.open(urljoin(host_url, break_url))
        webbrowser.open(urljoin(host_url, '/songbook/'))
        print("\033[2J\033[H")  # Clear screen
        try:
            input()
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            sys.exit(0)

    # Process input songs
    print("\nProcessing input list:")
    selected_songs = []
    i = 0
    while i < len(input_songs):
        entry = input_songs[i]

        if entry == "Break":
            # Skip break handling if break_url is not configured
            if not break_url:
                i += 1
                continue

            print("\n--- BREAK ---")
            take_break, go_back = confirm_break()
            if go_back:
                i = max(0, i - 1)  # Go back one song, but not before the start
                continue
            if take_break:
                selected_songs.append(("break", None))
                webbrowser.open(urljoin(host_url, break_url))
                print("\033[2J\033[H")  # Clear screen
                try:
                    input()
                except KeyboardInterrupt:
                    print("\nOperation cancelled by user")
                    sys.exit(0)
            i += 1
            continue

        # Show the current performer announcement
        print("\033[2J\033[H")  # Clear screen
        print(f"\n\033[1m{entry.leader}\033[0m - you're up next, with {entry.title}")
        print("Please make sure your uke is tuned, and come to the front before the end of the current song.")
        try:
            input()
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            sys.exit(0)

        print(f"\nProcessing: {entry.title} - {entry.artist}")
        print(f"Leader: {entry.leader}")

        # Find potential matches
        matches = find_matches(entry, available_songs)
        if not matches:
            print("No matches found!")
            if confirm_action("Skip this song?"):
                i += 1
                continue
            else:
                sys.exit(1)

        # Let user select the match
        selected, go_back = select_match(matches, f"{entry.title} - {entry.artist}")
        if go_back:
            i = max(0, i - 1)  # Go back one song, but not before the start
            continue

        if selected:
            selected_songs.append(("song", selected))
            print(f"\nSelected: {selected.display_name}")
            # Open the song URL
            song_url = urljoin(host_url, selected.song.href)
            webbrowser.open(song_url)
            i += 1
        else:
            print("\nSkipped song")
            i += 1

    # Only show final break if break_url is configured
    if break_url:
        print("\033[2J\033[H")  # Clear screen
        try:
            input()
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            sys.exit(0)
        webbrowser.open(urljoin(host_url, break_url))


if __name__ == "__main__":
    main()
