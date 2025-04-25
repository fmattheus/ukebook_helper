# Ukebook Helper

A helper tool for managing Ukebook song selections, providing an interactive interface for matching songs and managing the performance flow.

## Features

- Next performer announcements
- Interactive song selection with fuzzy matching
- TUI interface with keyboard navigation
- Break management with go-back functionality
- Automatic browser integration for song pages
- Simple configuration via TOML file

## Prerequisites

- Python 3.9 or newer
- [uv](https://github.com/astral-sh/uv) for dependency management

## Setup

1. Create your configuration file:
   ```bash
   cp config.example.toml config.toml
   ```

2. Install dependencies with uv:
   ```bash
   uv install .
   ```
## Configuration

Create a `config.toml` file based on the example:

```toml
# Ukebook Helper Configuration

# Base URL of the Ukebook website
host_url = "https://muc-uke.de"

# Login credentials
username = "your_username"
password = "your_password"

# Optional URL to open during breaks
break_url = "/ukebook/"
```

3. Create an `input.list` file in your working directory with the following tab-separated format:
   ```
   Song Title    Artist    GEMA Nr.    Leader
   Break
   Song Title    Artist    GEMA Nr.    Leader
   ```

## Usage

Run the program using uv:
```bash
uv run python -m ukebook_helper config.toml
```

## Navigation

- Use ↑/↓ arrow keys to navigate options
- Press Enter to select
- Press Ctrl+C to exit cleanly at any time

## Program Flow

1. The program starts by opening the Ukebook website and songbook
2. For each entry in the input list:
   - For songs:
     - Shows the next performer announcement
     - Finds matching songs using fuzzy matching
     - Lets you select the correct match
     - Opens the selected song in the browser
   - For breaks:
     - Asks for confirmation
     - Opens the Ukebook website during breaks
4. At the end, opens the Ukebook website one final time

## Project Structure

- `src/ukebook_helper/` - Main package directory
  - `__init__.py` - Package initialization
  - `client.py` - Ukebook website interaction
  - `models.py` - Data models
  - `matcher.py` - Fuzzy matching logic
  - `ui.py` - User interface components

## License

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/gpl-2.0.html>. 