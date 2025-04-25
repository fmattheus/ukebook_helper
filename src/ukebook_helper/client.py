"""
Ukebook client implementation for handling website interactions
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Dict
from .models import Song


class UkebookClient:
    def __init__(self, host_url: str):
        """Initialize the Ukebook client with the base URL."""
        self.host_url = host_url.rstrip('/')
        self.session = requests.Session()
        self._logged_in = False

    def login(self, username: str, password: str) -> bool:
        """
        Log in to the Ukebook website.

        Args:
            username: The username for login
            password: The password for login

        Returns:
            bool: True if login was successful, False otherwise
        """
        login_url = urljoin(self.host_url, '/songbook/login/')

        # Prepare login data
        login_data = {
            'username': username,
            'password': password,
            'loginBtn': 'Login'
        }

        try:
            # Send login request
            response = self.session.post(
                login_url,
                data=login_data,
                allow_redirects=False  # Don't follow redirects, similar to Go implementation
            )

            # Check if login was successful (usually indicated by a redirect)
            if response.status_code in (301, 302):
                self._logged_in = True
                return True

            return False

        except requests.RequestException as e:
            print(f"Login error: {e}")
            return False

    def fetch_songs(self) -> Dict[str, Song]:
        """
        Fetch and parse the song list from the website.

        Returns:
            Dict[str, Song]: Dictionary mapping song display names to Song objects
        """
        if not self._logged_in:
            raise RuntimeError("Must be logged in to fetch songs")

        songbook_url = urljoin(self.host_url, '/songbook/')

        try:
            # Fetch the songbook page
            response = self.session.get(
                songbook_url,
                headers={'Accept-Encoding': 'identity'}  # Prevent compression, matching Go implementation
            )
            response.raise_for_status()

            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the song list (ol with class songList)
            song_list = soup.find('ol', class_='songList')
            if not song_list:
                print("WARNING: No songList element found in the HTML!")
                return {}

            songs = {}
            for idx, song_link in enumerate(song_list.find_all('a')):
                title_elem = song_link.find('strong', class_='songTitle')
                artist_elem = song_link.find('em', class_='songArtist')

                if title_elem:
                    title = title_elem.get_text(strip=True)
                    artist = artist_elem.get_text(strip=True) if artist_elem else ''
                    href = song_link.get('href', '')

                    # Create unique key with index, similar to Go implementation
                    key = f"{title} - {artist} ({idx})" if artist else f"{title} ({idx})"
                    songs[key] = Song(title=title, artist=artist, href=href)

            return songs

        except requests.RequestException as e:
            print(f"Error fetching songs: {e}")
            return {}

    @property
    def is_logged_in(self) -> bool:
        """Check if the client is currently logged in."""
        return self._logged_in
