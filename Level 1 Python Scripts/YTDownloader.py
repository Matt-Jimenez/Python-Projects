#importing modules needed
import tkinter as tk
from tkinter import filedialog
import customtkinter
from pytube import YouTube
import os

# Global variables for UI elements
video_title_label = None
status_label = None
link_entry = None
pPercentage = None
progressBar = None
app = None # Added app to globals for update_idletasks
download_path_var = None # For displaying the selected download path
DEFAULT_DOWNLOAD_DIR = "Downloads" # Default download directory name


def select_download_path():
    global download_path_var
    # Open dialog to select directory
    chosen_path = filedialog.askdirectory()
    if chosen_path:  # If a path is chosen (dialog not cancelled)
        download_path_var.set(chosen_path)

def startdownload():
    global video_title_label, status_label, link_entry, pPercentage, progressBar, app, download_path_var

    if not all([app, link_entry, video_title_label, status_label, pPercentage, progressBar]):
        print("Error: UI elements not fully initialized.")
        if status_label:
            status_label.configure(text="UI Error. Please restart.", text_color="red")
        return

    try:
        ytLink = link_entry.get()
        if not ytLink:
            status_label.configure(text="Please enter a YouTube link.", text_color="orange")
            return

        # Clear previous messages and title, reset progress
        status_label.configure(text="Fetching video info...", text_color="gray")
        video_title_label.configure(text="")
        pPercentage.configure(text="0%")
        progressBar.set(0)
        app.update_idletasks() # Ensure UI updates

        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()

        video_title_label.configure(text=ytObject.title) 
        status_label.configure(text="Downloading...", text_color="blue")
        app.update_idletasks()

        actual_download_path = download_path_var.get()
        # Ensure the chosen directory exists, especially if it's the default or manually entered
        if not os.path.isdir(actual_download_path):
            try:
                os.makedirs(actual_download_path, exist_ok=True)
                print(f"Created download directory: {actual_download_path}")
            except OSError as oe:
                print(f"Error creating directory {actual_download_path}: {oe}")
                status_label.configure(text=f"Error: Cannot create path {actual_download_path}", text_color="red")
                return
        
        print(f"Downloading to: {actual_download_path}")
        video.download(output_path=actual_download_path) 
        status_label.configure(text="Downloaded Successfully!", text_color="green")

    except Exception as e:
        print(f"An error occurred: {e}") 
        if video_title_label:
            video_title_label.configure(text="Error") 
        if status_label:
            status_label.configure(text="Download Error. Check link or connection.", text_color="red")
    finally:
        # Reset progress bar after download attempt (success or fail)
        if progressBar:
            progressBar.set(0)
        if pPercentage:
            pPercentage.configure(text="0%")
        app.update_idletasks()


def on_progress(stream, chunk, bytes_remaining):
    global pPercentage, progressBar, app
    if not all([pPercentage, progressBar, app]):
        return

    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    
    pPercentage.configure(text=per + '%')
    progressBar.set(float(percentage_of_completion) / 100)
    # app.update_idletasks() # Updating too frequently here can make UI sluggish

# Theme toggle function
def toggle_theme(switch_var):
    if switch_var.get() == 1: # Switch is ON
        customtkinter.set_appearance_mode("Dark")
    else: # Switch is OFF
        customtkinter.set_appearance_mode("Light")

#System Settings
customtkinter.set_appearance_mode("Light") # Default to Light mode
customtkinter.set_default_color_theme("blue") 

#App frame
app_instance = customtkinter.CTk() # Renamed to avoid conflict if 'app' is used as global elsewhere
app_instance.geometry("720x480") 
app_instance.title("YouTube Video Downloader")

# Assign to global 'app' for use in functions
app = app_instance

# Main frame for overall padding and structure
main_frame = customtkinter.CTkFrame(app)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Input Section
input_frame = customtkinter.CTkFrame(main_frame)
input_frame.pack(pady=(0, 15), fill="x") 

instruction_label = customtkinter.CTkLabel(input_frame, text="Insert your YouTube link below:", font=("Arial", 14))
instruction_label.pack(pady=(10, 5)) 

url_var = tk.StringVar()
link_entry = customtkinter.CTkEntry(input_frame, textvariable=url_var, height=40, font=("Arial", 12))
link_entry.pack(fill="x", padx=20, pady=(0, 10), expand=True) 

# Download Path Selection Section
path_selection_frame = customtkinter.CTkFrame(main_frame)
path_selection_frame.pack(pady=(0,10), fill="x", padx=20)

path_label = customtkinter.CTkLabel(path_selection_frame, text="Save Location:", font=("Arial", 12))
path_label.pack(side="left", padx=(0, 5), pady=5)

download_path_var = tk.StringVar() # Moved initialization here to be after tk.Tk() is implicitly called by CTk()
selected_path_display_label = customtkinter.CTkLabel(path_selection_frame, textvariable=download_path_var, font=("Arial", 12, "italic"), anchor="w")
selected_path_display_label.pack(side="left", fill="x", expand=True, padx=(0,10), pady=5)

browse_button = customtkinter.CTkButton(path_selection_frame, text="Choose Folder", command=select_download_path, width=120)
browse_button.pack(side="left", pady=5)

# Video Title Display
video_title_label = customtkinter.CTkLabel(main_frame, text="", font=("Arial", 16, "bold"), wraplength=app.winfo_width() - 60) # Consider adjusting wraplength if layout changes
video_title_label.pack(pady=(0, 15))

#Download Button
download_button = customtkinter.CTkButton(main_frame, text="Download", command=startdownload, height=40, font=("Arial", 14, "bold"))
download_button.pack(pady=(0, 15))

# Progress Section
progress_frame = customtkinter.CTkFrame(main_frame)
progress_frame.pack(pady=(0, 15), fill="x", padx=20)

pPercentage = customtkinter.CTkLabel(progress_frame, text="0%", font=("Arial", 12))
pPercentage.pack(pady=(5,2))

progressBar = customtkinter.CTkProgressBar(progress_frame, height=15) 
progressBar.set(0)
progressBar.pack(fill="x", pady=(0,10), expand=True)

#Status Label
status_label = customtkinter.CTkLabel(main_frame, text="", font=("Arial", 12))
status_label.pack(pady=(0, 5))

# Theme Switch Frame
theme_switch_frame = customtkinter.CTkFrame(main_frame)
theme_switch_frame.pack(pady=(10, 0), fill="x", side="bottom") # Pack to bottom, fill x

theme_label = customtkinter.CTkLabel(theme_switch_frame, text="Dark Mode:", font=("Arial", 12))
theme_label.pack(side="left", padx=(20, 5), pady=10)

theme_switch_var = customtkinter.IntVar(value=0) # Switch is off by default
theme_switch = customtkinter.CTkSwitch(theme_switch_frame, text="", variable=theme_switch_var, onvalue=1, offvalue=0, command=lambda: toggle_theme(theme_switch_var))
theme_switch.pack(side="left", padx=(0, 20), pady=10)

# Initialize default download path and create directory if it doesn't exist
try:
    # Ensure the default directory exists at startup
    if not os.path.exists(DEFAULT_DOWNLOAD_DIR):
        os.makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)
    download_path_var.set(os.path.abspath(DEFAULT_DOWNLOAD_DIR)) # Set to absolute path for clarity
except Exception as e:
    print(f"Error setting up default download directory: {e}")
    download_path_var.set(os.getcwd()) # Fallback to current working directory


#Run App
app.mainloop()
