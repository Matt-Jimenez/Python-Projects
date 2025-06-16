import tkinter as tk
from tkinter import ttk # Import ttk
import requests
from threading import Thread

api = "http://api.quotable.io/random" # This will be the default/general API
# We might need different APIs or parameters for poetry later.
quotes = []
quote_number = 0

window = tk.Tk()
window.geometry("900x320") # Increased height slightly for the new widgets
window.title("Quote Generator")
window.grid_columnconfigure(0, weight=1)
window.resizable(False, False)
window.configure(bg="grey")

# Global variable for Combobox selection
source_selection_var = tk.StringVar()

#function for preloading quotes (currently fetches general quotes)
def preload_quotes():
    global quotes

    # For now, this function doesn't use the source_selection_var.
    # That will be part of a later subtask.
    print("***Loading some more quotes***")
    for x in range(10):
        try:
            random_quote = requests.get(api).json()
            content = random_quote["content"]
            author = random_quote["author"]
            quote = content + "\n\n" + "By " + author
            print(content)
            quotes.append(quote)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching quote: {e}")
            # Optionally, add a placeholder or error message to the quotes list
            # quotes.append("Error loading quote.\n\nN/A")
        except KeyError: # Handle cases where the API response might not have 'content' or 'author'
            print(f"Error parsing quote data from API response: {random_quote}")
            # quotes.append("Error parsing quote data.\n\nN/A")

    print("***Finished loading more quotes!***")

preload_quotes()

# Function to fetch a poetry quote
def fetch_poetry_quote():
    poetry_api_url = "https://poetrydb.org/random/1/author,lines.json"
    try:
        response = requests.get(poetry_api_url, timeout=10) # Added timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

        data = response.json()

        if data and isinstance(data, list):
            poem_data = data[0]
            author = poem_data.get("author", "Unknown Author")
            lines = poem_data.get("lines", [])

            if not lines:
                return f"Poetry quote found, but no lines available.\n\nBy {author}"

            formatted_poem = "\n".join(lines)
            return f"{formatted_poem}\n\nBy {author}"
        else:
            # Handle cases where the response is not as expected (e.g., not a list, or empty)
            print(f"Unexpected API response structure: {data}")
            return "Poetry quote not found in API response.\n\nN/A"

    except requests.exceptions.Timeout:
        print("Error fetching poetry quote: Request timed out.")
        return "Could not fetch poetry quote (timeout). Please try again.\n\nN/A"
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching poetry quote (HTTP error): {e}")
        return "Could not fetch poetry quote (server error). Please try again.\n\nN/A"
    except requests.exceptions.RequestException as e:
        # General network/request error
        print(f"Error fetching poetry quote (network/request): {e}")
        return "Could not fetch poetry quote. Please check connection.\n\nN/A"
    except (KeyError, IndexError, TypeError) as e:
        # Errors during JSON parsing or if the structure is not as expected
        print(f"Error parsing poetry quote data: {e}")
        return "Error parsing poetry quote data.\n\nN/A"
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred while fetching poetry: {e}")
        return "An unexpected error occurred. Please try again.\n\nN/A"

#functions to gather quote
def get_random_quote():
    global quote_label
    global quotes
    global quote_number
    global source_selection_var # Ensure it's recognized as global

    selected_source = source_selection_var.get()
    print(f"Selected source: {selected_source}")

    if selected_source == "Poetry":
        # Fetch and display a poetry quote
        # Poetry quotes are fetched on demand, not preloaded into the 'quotes' list
        poetry_quote_text = fetch_poetry_quote()
        quote_label.configure(text=poetry_quote_text)
        # No need to manage quote_number or the general 'quotes' list for poetry

    elif selected_source == "General/Literary":
        # Use existing logic for general/literary quotes

        # Condition to preload:
        # 1. 'quotes' list is empty.
        # 2. 'quote_number' has reached or exceeded the length of 'quotes'.
        # 3. 'quote_number' is nearing the end of the 'quotes' list (e.g., within the last 3).
        should_preload = not quotes or quote_number >= len(quotes) - 3

        if not quotes or quote_number >= len(quotes):
            message = "No general quotes available. "
            if quotes and quote_number >= len(quotes): # Specifically ran out
                message = "Reached the end of preloaded general quotes. "

            quote_label.configure(text=message + "Loading more, please wait or click again shortly.")
            if not Thread(target=preload_quotes).is_alive(): # Start preload only if not already running
                 thread = Thread(target=preload_quotes)
                 thread.start()
            return

        # Display the quote
        quote_label.configure(text=quotes[quote_number])
        quote_number += 1

        # Preload if nearing the end and not already preloading
        if should_preload:
            print(f"General quotes state: (quote_number: {quote_number}, len: {len(quotes)}). Triggering preload if needed.")
            # Check if a preload thread is already active to avoid multiple threads
            # This is a simplified check; a more robust solution might use a lock or a dedicated flag
            active_threads = [t for t in Thread._active.values() if t.name == "preload_quotes_thread"]
            if not active_threads:
                 thread = Thread(target=preload_quotes, name="preload_quotes_thread")
                 thread.start()
            else:
                print("Preload thread already running.")
    else:
        # Fallback for any unexpected selection, though Combobox is readonly
        quote_label.configure(text="Invalid source selected. Please choose from the list.")

#UI

# Source Selection Label
source_label = tk.Label(window, text="Quote Source:", bg="grey", fg="black", font=('Courier', 12))
source_label.grid(row=0, column=0, stick="W", padx=20, pady=(10,0))

# Combobox for source selection
source_options = ["General/Literary", "Poetry"]
# Ensure ttk.Combobox is used, not tk.Combobox if tk was aliased as ttk
source_combobox = ttk.Combobox(window, textvariable=source_selection_var, values=source_options, state="readonly", font=('Courier', 12), width=30)
source_combobox.grid(row=1, column=0, stick="EW", padx=20, pady=(0,10))
source_selection_var.set(source_options[0]) # Set default value

# Quote Display Label
quote_label = tk.Label(window, text="Click 'Generate' to see a random quote!", # Changed initial text
                       height=6,
                       pady=10,
                       wraplength=800,
                       font=('Courier', 14))
quote_label.grid(row=2,column=0, stick="WE",padx=20,pady=10) # Shifted to row 2

#button
button = tk.Button(text="Generate", command=get_random_quote,bg='#0052cc', fg="#ffffff",
                   activebackground="grey", font=('Courier', 14))
button.grid(row=3,column=0, stick="WE",padx=20,pady=10) # Shifted to row 3


#program execute
if __name__ == "__main__":
    window.mainloop()
