#importing modules needed
import tkinter as tk
import customtkinter
from pytube import YouTube

def startdownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()

        title.configure(text=ytObject.title, text_color="white")
        downloadLabel.configure(text="")
        video.download()
        downloadLabel.configure(text="Downloaded Successfully!", text_color="green")
    except:
        downloadLabel.configure(text="There was an error!", text_color="red")

def on_progress(stream,chunk,bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=per + '%')
    pPercentage.update()
    progressBar.set(float(percentage_of_completion) / 100)
    progressBar.update()


#System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

#App frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Downloader for YT")

#Adding GUI Elements
title = customtkinter.CTkLabel(app, text="Insert your YouTube link")
title.pack(padx=10,pady=10)

#Input Link
url_var = tk.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

#Download Button
download = customtkinter.CTkButton(app, text="Download", command=startdownload)
download.pack(padx=10,pady=10)

#Download Completed
downloadLabel = customtkinter.CTkLabel(app, text="")
downloadLabel.pack()

#Progress info
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10,pady=10)

#Run App
app.mainloop()
