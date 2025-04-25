"""
TUI elements for interactive song selection
"""
from typing import List, Optional, Tuple
import sys
from prompt_toolkit import prompt
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.keys import Keys
from .matcher import Match


def select_match(matches: List[Match], song_title: str) -> Tuple[Optional[Match], bool]:
    """
    Display an interactive selection dialog for choosing a match.

    Args:
        matches: List of potential matches to choose from
        song_title: Title of the input song being matched

    Returns:
        Tuple of (Selected Match object or None if skipped, bool indicating if user wants to go back)
    """
    # Add skip and go back options, with skip after the matches
    choices = [(m, m.display_name) for m in matches] + [(None, 'Skip'), (None, 'Go back')]
    selected_index = len(matches) - 1  # Start with last match selected

    def get_choice_text(index: int, choice: tuple) -> str:
        """Format a single choice."""
        match = choice[0]
        is_selected = index == selected_index
        prefix = "  ▶ " if is_selected else "    "

        # Format with cyan color if selected
        if is_selected:
            if choice[1] in ('Skip', 'Go back'):
                return f"{prefix}<style fg='cyan'>{choice[1]}</style>"

            # For songs, format display name and similarity
            display_name = choice[0].display_name
            if len(display_name) > 50:
                display_name = display_name[:47] + "..."
            return f"{prefix}<style fg='cyan'>{display_name} ({match.similarity}%)</style>"

        # Non-selected items
        if choice[1] in ('Skip', 'Go back'):
            return f"{prefix}{choice[1]}"

        # For non-selected songs
        display_name = choice[0].display_name
        if len(display_name) > 50:
            display_name = display_name[:47] + "..."
        return f"{prefix}{display_name} ({match.similarity}%)"

    def get_formatted_text():
        """Get the complete formatted text for display."""
        title = f'Trying to match: <b>{song_title}</b>\n'
        choices_text = '\n'.join(get_choice_text(i, c) for i, c in enumerate(choices))
        return HTML(title + choices_text)

    # Create key bindings
    kb = KeyBindings()
    result = [None, False]  # [selected_match, go_back]

    @kb.add('up')
    def handle_up(event):
        nonlocal selected_index
        selected_index = (selected_index - 1) % len(choices)
        text_area.text = get_formatted_text()

    @kb.add('down')
    def handle_down(event):
        nonlocal selected_index
        selected_index = (selected_index + 1) % len(choices)
        text_area.text = get_formatted_text()

    @kb.add('enter')
    def handle_enter(event):
        choice = choices[selected_index]
        if choice[1] == 'Go back':
            result[1] = True
        else:
            result[0] = choice[0]
        event.app.exit()

    @kb.add('c-c')
    def handle_ctrl_c(event):
        event.app.exit()
        print("\nOperation cancelled by user")
        sys.exit(0)

    # Create the layout
    text_area = FormattedTextControl(text=get_formatted_text())
    window = Window(content=text_area)
    root_container = HSplit([window])

    # Create and run the application
    application = Application(
        layout=Layout(root_container),
        key_bindings=kb,
        mouse_support=True,
        full_screen=True
    )

    try:
        application.run()
        return (result[0], result[1])
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)


def confirm_action(prompt_text: str) -> bool:
    """
    Display a yes/no confirmation prompt using TUI.

    Args:
        prompt_text: The text to display in the prompt

    Returns:
        True if confirmed, False otherwise
    """
    choices = [(True, "Yes"), (False, "No")]
    selected_index = 0  # Default to "Yes"

    def get_choice_text(index: int, choice: tuple) -> str:
        """Format a single choice."""
        is_selected = index == selected_index
        prefix = "  ▶ " if is_selected else "    "

        # Format with cyan color if selected
        if is_selected:
            return f"{prefix}<style fg='cyan'>{choice[1]}</style>"
        return f"{prefix}{choice[1]}"

    def get_formatted_text():
        """Get the complete formatted text for display."""
        title = f'<b>{prompt_text}</b>\n'
        choices_text = '\n'.join(get_choice_text(i, c) for i, c in enumerate(choices))
        return HTML(title + choices_text)

    # Create key bindings
    kb = KeyBindings()
    result = [False]  # Default to No

    @kb.add('up')
    def handle_up(event):
        nonlocal selected_index
        selected_index = (selected_index - 1) % len(choices)
        text_area.text = get_formatted_text()

    @kb.add('down')
    def handle_down(event):
        nonlocal selected_index
        selected_index = (selected_index + 1) % len(choices)
        text_area.text = get_formatted_text()

    @kb.add('enter')
    def handle_enter(event):
        result[0] = choices[selected_index][0]
        event.app.exit()

    @kb.add('c-c')
    def handle_ctrl_c(event):
        event.app.exit()
        print("\nOperation cancelled by user")
        sys.exit(0)

    # Create the layout
    text_area = FormattedTextControl(text=get_formatted_text())
    window = Window(content=text_area)
    root_container = HSplit([window])

    # Create and run the application
    application = Application(
        layout=Layout(root_container),
        key_bindings=kb,
        mouse_support=True,
        full_screen=True
    )

    try:
        application.run()
        return result[0]
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)


def confirm_break() -> tuple[bool, bool]:
    """
    Display a break confirmation prompt with go back option.

    Returns:
        Tuple of (take_break: bool, go_back: bool)
    """
    choices = [(True, "Take a break"), (False, "Skip break"), (None, "Go back")]
    selected_index = 0  # Default to "Take a break"

    def get_choice_text(index: int, choice: tuple) -> str:
        """Format a single choice."""
        is_selected = index == selected_index
        prefix = "  ▶ " if is_selected else "    "

        # Format with cyan color if selected
        if is_selected:
            return f"{prefix}<style fg='cyan'>{choice[1]}</style>"
        return f"{prefix}{choice[1]}"

    def get_formatted_text():
        """Get the complete formatted text for display."""
        title = '<b>Break time?</b>\n'
        choices_text = '\n'.join(get_choice_text(i, c) for i, c in enumerate(choices))
        return HTML(title + choices_text)

    # Create key bindings
    kb = KeyBindings()
    result = [False, False]  # [take_break, go_back]

    @kb.add('up')
    def handle_up(event):
        nonlocal selected_index
        selected_index = (selected_index - 1) % len(choices)
        text_area.text = get_formatted_text()

    @kb.add('down')
    def handle_down(event):
        nonlocal selected_index
        selected_index = (selected_index + 1) % len(choices)
        text_area.text = get_formatted_text()

    @kb.add('enter')
    def handle_enter(event):
        choice = choices[selected_index]
        if choice[1] == "Go back":
            result[1] = True
        else:
            result[0] = choice[0]
        event.app.exit()

    @kb.add('c-c')
    def handle_ctrl_c(event):
        event.app.exit()
        print("\nOperation cancelled by user")
        sys.exit(0)

    # Create the layout
    text_area = FormattedTextControl(text=get_formatted_text())
    window = Window(content=text_area)
    root_container = HSplit([window])

    # Create and run the application
    application = Application(
        layout=Layout(root_container),
        key_bindings=kb,
        mouse_support=True,
        full_screen=True
    )

    try:
        application.run()
        return (result[0], result[1])
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
