import random
import sys
from pathlib import Path # Helps find files reliably
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel

# --- CONFIGURATION ---
forest_theme = Theme({
    "narrative": "green",
    "event": "bold italic yellow",
    "prompt": "bold cyan",
    "alert": "bold red",
    "title": "bold magenta reverse"
})

console = Console(theme=forest_theme)

# --- HELPER FUNCTIONS ---
def load_events(filename):
    """
    Reads events from a text file located in the same directory as this script.
    Returns a default list if the file is missing or empty.
    """
    # Get the folder where this script is actually located
    script_dir = Path(__file__).parent
    file_path = script_dir / filename

    if not file_path.exists():
        console.print(f"[alert]Warning: '{filename}' not found at {file_path}. Using default events.[/alert]")
        return ["a bird screeches loudly", "you trip over a root", "a cold wind blows"]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Read lines, strip whitespace, and ignore empty lines
            events = [line.strip() for line in f if line.strip()]
            
        if not events:
            console.print(f"[alert]Warning: '{filename}' is empty. Using default events.[/alert]")
            return ["nothing happens", "a leaf falls"]
            
        return events
    except Exception as e:
        console.print(f"[alert]Error reading file: {e}[/alert]")
        return ["an unknown error occurs"]

def step(choice: str, events):
    if not events:
        return "[alert]No events available![/alert]"
        
    random_event = random.choice(events)

    if choice == "left":
        return left_path(random_event)
    elif choice == "right":
        return right_path(random_event)
    else:
        return "[alert]You stand still, unsure what to do. The forest swallows you.[/alert]"

def left_path(event):
    return f"[narrative]You walk left.[/narrative] [event]{event}[/event]"

def right_path(event):
    return f"[narrative]You walk right.[/narrative] [event]{event}[/event]"

# --- MAIN GAME LOOP ---
if __name__ == "__main__":
    # Load events safely
    events = load_events('events.txt')

    console.print(Panel.fit(
        "You wake up in a [narrative]dark forest[/narrative].\nYou can go [prompt]left[/prompt] or [prompt]right[/prompt].",
        title="[title] THE DARK FOREST [/title]",
        border_style="green"
    ))

    while True:
        choice = console.input("\n[prompt]Which direction do you choose? (left/right/exit): [/prompt]")
        choice = choice.strip().lower()
        
        if choice == 'exit':
            console.print("[alert]You flee the forest. Game Over.[/alert]")
            break
        
        result = step(choice, events)
        console.print(result)

    console.print("\n[bold magenta]👋 Goodbye! Thanks for playing.[/bold magenta]") 