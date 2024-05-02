import os
import customtkinter as ctk
from tkinter import ttk
from pytube import YouTube


def downlaodVideo():
    url = inputUrl.get()
    quality = resVar.get()

    loadLabel.pack(pady=(10, 5))
    progressLabel.pack(pady=(10, 5))
    progressBar.pack(pady=(10, 5))

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        # Get the available streams
        available_streams = yt.streams.filter(progressive=True)

        # Filter streams by resolution
        streams_by_resolution = {stream.resolution: stream for stream in available_streams}

        # Check if the selected resolution is available
        if quality in streams_by_resolution:
            selected_stream = streams_by_resolution[quality]
        else:
            # If selected resolution is not available, choose the maximum available resolution
            selected_stream = max(available_streams, key=lambda stream: int(stream.resolution[:-1]))

        # Download the selected stream
        filename = f"{yt.title}.mp4"
        output_path = os.path.join("D:/YouTubeVideos", filename)
        selected_stream.download(output_path=output_path)
        print(f"Video downloaded successfully to: {output_path}")
    except Exception as e:
        print("An error occurred:", e)



def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progressLabel.configure(text=f"{int(percentage)}%")
    progressLabel.update()
    progressBar.set(int(percentage / 100))


# Create the main window
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root.title("YouTube Downloader")

#set default size and min size
root.geometry("720x480")
root.minsize(480, 320)

#create frame
frame = ctk.CTkFrame(root)
frame.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

url = ctk.CTkLabel(frame, text="Enter the URL")
inputUrl = ctk.CTkEntry(frame, height=40, width=400)
url.pack(pady=(10, 5))
inputUrl.pack(pady=(10, 5))
downloadButton = ctk.CTkButton(frame, text="Download", command=downlaodVideo)
downloadButton.pack(pady=(10, 5))

resolution = ["1080p", "720p", "480p", "360p"]
resVar = ctk.StringVar()
combobox = ttk.Combobox(frame, values=resolution, textvariable=resVar,state='readonly')
combobox.pack(pady=(10, 5))
combobox.set("480p")

loadLabel = ctk.CTkLabel(frame, text="")

progressBar = ctk.CTkProgressBar(frame, width=400)
progressBar.set(0)
progressLabel = ctk.CTkLabel(frame, text="")
root.mainloop()
