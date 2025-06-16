import tkinter as tk # Keep for StringVar, but mock Tk and Label
from tkinter import ttk
import requests
from threading import Thread, current_thread
import time # For simulating delays and joining threads in tests

# --- Mocking Tkinter for testing without GUI ---
class MockTk:
    def __init__(self):
        self.title_val = ""
        self.geometry_val = ""
    def title(self, val): self.title_val = val
    def geometry(self, val): self.geometry_val = val
    def grid_columnconfigure(self, idx, weight): pass
    def resizable(self, w, h): pass
    def configure(self, bg): pass
    def mainloop(self): print("Mock mainloop called. Exiting test run.")

class MockLabel:
    def __init__(self, master, text, height, pady, wraplength, font, bg=None, fg=None):
        self.text = text
        print(f"MockLabel created with initial text: '{text}'")
    def configure(self, text):
        self.text = text
        printable_text = self.text.replace('\n', ' ')[:100] # Corrected line
        print(f"MockLabel configured with text: <<<{printable_text}...>>>")
    def grid(self, **kwargs): pass

_real_tk_Tk = tk.Tk
_real_tk_Label = tk.Label
tk.Tk = MockTk
tk.Label = MockLabel
# --- End Mocking ---

# --- Application Code (Copied from Level 1 Python Scripts/Quote Generator.py with minor test adaptations) ---
api = "http://api.quotable.io/random"
quotes = []
quote_number = 0

window = tk.Tk()
window.geometry("900x320")
window.title("Quote Generator")
window.grid_columnconfigure(0, weight=1)
window.resizable(False, False)
window.configure(bg="grey")

source_selection_var = tk.StringVar()
_active_preload_thread_obj = None # Stores the active preload Thread object

def preload_quotes():
    global quotes, _active_preload_thread_obj
    _active_preload_thread_obj = current_thread()

    print("***Loading some more general quotes***")
    current_quotes_count = len(quotes)
    for x in range(2): # Fetch 2 new quotes
        try:
            random_quote = requests.get(api, timeout=5).json()
            content = random_quote["content"]
            author = random_quote["author"]
            quote = content + "\n\n" + "By " + author
            print(f"Fetched general: {content[:30]}...")
            quotes.append(quote)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching general quote: {e}")
        except KeyError:
            print(f"Error parsing general quote data for: {random_quote if 'random_quote' in locals() else 'N/A'}")
    print(f"***Finished loading general quotes! Quotes list size: {len(quotes)} (was {current_quotes_count})***")
    _active_preload_thread_obj = None


initial_preload_thread = Thread(target=preload_quotes, name="preload_quotes_thread_initial")
initial_preload_thread.start()

def fetch_poetry_quote():
    poetry_api_url = "https://poetrydb.org/random/1/author,lines.json"
    print("Fetching poetry quote...")
    try:
        response = requests.get(poetry_api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list):
            poem_data = data[0]
            author = poem_data.get("author", "Unknown Author")
            lines = poem_data.get("lines", [])
            if not lines: return f"Poetry quote found, but no lines available.\n\nBy {author}"
            formatted_poem = "\n".join(lines)
            print(f"Fetched poetry: {author} - {formatted_poem[:30]}...")
            return f"{formatted_poem}\n\nBy {author}"
        else:
            print(f"Unexpected API response structure for poetry: {data}")
            return "Poetry quote not found in API response.\n\nN/A"
    except requests.exceptions.Timeout:
        print("Error fetching poetry quote: Request timed out.")
        return "Could not fetch poetry quote (timeout). Please try again.\n\nN/A"
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching poetry quote (HTTP error): {e}")
        return "Could not fetch poetry quote (server error). Please try again.\n\nN/A"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poetry quote (network/request): {e}")
        return "Could not fetch poetry quote. Please check connection.\n\nN/A"
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing poetry quote data: {e}")
        return "Error parsing poetry quote data.\n\nN/A"
    except Exception as e: # General catch-all
        print(f"An unexpected error occurred while fetching poetry: {e}")
        return "An unexpected error occurred. Please try again.\n\nN/A"

def get_random_quote():
    global quote_label, quotes, quote_number, source_selection_var, _active_preload_thread_obj
    selected_source = source_selection_var.get()
    print(f"\n--- Button Clicked (Source: {selected_source}) ---")

    if selected_source == "Poetry":
        poetry_quote_text = fetch_poetry_quote()
        quote_label.configure(text=poetry_quote_text)
    elif selected_source == "General/Literary":
        needs_preload_now = not quotes or quote_number >= len(quotes)
        should_trigger_preload = needs_preload_now or (quote_number >= len(quotes) - 1)

        if needs_preload_now:
            message = "No general quotes available. "
            if quotes and quote_number >= len(quotes):
                message = "Reached the end of preloaded general quotes. "
            quote_label.configure(text=message + "Loading more, please wait or click again shortly.")

            if not (_active_preload_thread_obj and _active_preload_thread_obj.is_alive()):
                 print("LOGIC: Starting preload due to lack/end of quotes.")
                 thread = Thread(target=preload_quotes, name="preload_quotes_thread_ অভাব")
                 thread.start()
            else:
                print("LOGIC: Preload already running (lack/end of quotes check).")
            return

        quote_label.configure(text=quotes[quote_number])
        quote_number += 1

        if should_trigger_preload and not needs_preload_now :
            print(f"LOGIC: General quotes state: (quote_number: {quote_number}, len: {len(quotes)}). Triggering preload if needed.")
            if not (_active_preload_thread_obj and _active_preload_thread_obj.is_alive()):
                 print("LOGIC: Starting preload due to nearing end.")
                 thread = Thread(target=preload_quotes, name="preload_quotes_thread_nearing_end")
                 thread.start()
            else:
                print("LOGIC: Preload already running (nearing end check).")
    else:
        quote_label.configure(text="Invalid source selected. Please choose from the list.")

_tk_Label_for_grid = _real_tk_Label
source_label = _tk_Label_for_grid(window, text="Quote Source:", bg="grey", fg="black", font=('Courier', 12))
source_label.grid(row=0, column=0, stick="W", padx=20, pady=(10,0))

source_options = ["General/Literary", "Poetry"]
source_combobox = ttk.Combobox(window, textvariable=source_selection_var, values=source_options, state="readonly", font=('Courier', 12), width=30)
source_combobox.grid(row=1, column=0, stick="EW", padx=20, pady=(0,10))

quote_label = MockLabel(window, text="Click 'Generate' to see a random quote!", height=6, pady=10, wraplength=800, font=('Courier', 14))

# --- Test Harness ---
if __name__ == "__main__":
    print("--- Test Run Start ---")

    print("Waiting for initial preload to complete (max 10s)...")
    initial_preload_thread.join(timeout=10)
    if initial_preload_thread.is_alive():
        print("WARN: Initial preload thread still alive after timeout!")
    else:
        print("Initial preload complete/joined.")

    print("\n--- Test 1: General/Literary Quotes (expecting 2 initial + 2 preloaded) ---")
    source_selection_var.set("General/Literary")
    for i in range(5):
        print(f"Simulating click {i+1} for General/Literary...")
        get_random_quote()
        time.sleep(0.1)

    if _active_preload_thread_obj and _active_preload_thread_obj.is_alive():
        print("Waiting for general preload from Test 1 to finish (max 7s)...")
        _active_preload_thread_obj.join(timeout=7)

    print("\n--- Test 2: Poetry Quotes ---")
    source_selection_var.set("Poetry")
    for i in range(2):
        print(f"Simulating click {i+1} for Poetry...")
        get_random_quote()
        time.sleep(1)

    print("\n--- Test 3: Poetry Error Simulation ---")
    original_fetch_poetry_func = fetch_poetry_quote
    def mock_fetch_poetry_error_func():
        print("SIMULATING poetry fetch error...")
        return "This is a simulated poetry fetch error.\n\nBy System"
    globals()['fetch_poetry_quote'] = mock_fetch_poetry_error_func

    source_selection_var.set("Poetry")
    print("Simulating click for Poetry (with error)...")
    get_random_quote()
    globals()['fetch_poetry_quote'] = original_fetch_poetry_func
    print("Restored original poetry fetch function.")

    print("\n--- Test 4: Switch back to General/Literary ---")
    source_selection_var.set("General/Literary")
    print(f"Current general quotes list size: {len(quotes)}, quote_number: {quote_number}")
    for i in range(3):
        print(f"Simulating click {i+1} for General/Literary (post-poetry)...")
        get_random_quote()
        time.sleep(0.1)

    print("\n--- Test 5: Exhausting General Quotes ---")
    source_selection_var.set("General/Literary")
    print(f"Starting exhaust test. Quotes: {len(quotes)}, Number: {quote_number}")
    remaining_general_quotes = len(quotes) - quote_number if quote_number < len(quotes) else 0
    clicks_to_exhaust_and_trigger = remaining_general_quotes + 1
    print(f"Will simulate {clicks_to_exhaust_and_trigger} clicks to exhaust general quotes and trigger reload.")
    for i in range(clicks_to_exhaust_and_trigger):
        print(f"Simulating exhaust click {i+1} for General/Literary...")
        get_random_quote()
        time.sleep(0.1)
        if _active_preload_thread_obj and _active_preload_thread_obj.is_alive() and i == clicks_to_exhaust_and_trigger -1 :
             print("Waiting for exhaust-triggered preload (max 7s)...")
             _active_preload_thread_obj.join(timeout=7)

    print("\n--- Test Run End ---")
    tk.Tk = _real_tk_Tk
    tk.Label = _real_tk_Label
