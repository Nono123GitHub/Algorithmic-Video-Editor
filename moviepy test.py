from moviepy import ImageSequenceClip, AudioFileClip, vfx
from PIL import Image
import os
import librosa
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from moviepy import *

# ffmpeg -i "C:\Users\nshei\Downloads\audio.mp3" -ar 44100 -ac 2 fixed_audio.mp3 <- convert music into playable

global image_freq_var
root = tk.Tk()
root.geometry('1000x400')
root.title('Algorithmic Video Editor')

label_font = ("Helvetica", 12)
info_font = ("Helvetica", 10, "italic")

# Image directory
tk.Label(root, text="Select image directory:", font=label_font).pack(anchor="w", pady=(0, 5))
image_dir = filedialog.askdirectory()
tk.Label(root, text=f"📂 Image directory: {image_dir}", font=info_font, fg="blue").pack(anchor="w", pady=(0, 15))

# Audio file
tk.Label(root, text="Select audio file:", font=label_font).pack(anchor="w", pady=(0, 5))
audio_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
tk.Label(root, text=f"🎵 Audio file: {audio_file}", font=info_font, fg="green").pack(anchor="w", pady=(0, 15))

# Frequency entry
tk.Label(root, text="Select image frequency (images per beat):", font=label_font).pack(anchor="w", pady=(0, 5))
entry_freq = tk.Entry(root)
entry_freq.insert(0, "8")
entry_freq.pack(anchor="w", pady=(0, 10))

# store value
image_freq_var = None

def on_continue():
    global image_freq_var
    image_freq_var = entry_freq.get()
    root.destroy()

tk.Button(root, text="Continue", command=on_continue, font=label_font).pack(pady=(20, 0))
root.mainloop()

print(image_freq_var)
audio_path = audio_file
y, sr = librosa.load(audio_path)
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
tempo = float(tempo)
interval = 60 / tempo
print(f"🎵 BPM: {tempo:.2f}, Interval: {interval:.2f}s")

image_folder = image_dir
image_files = [os.path.join(image_folder, f) 
               for f in os.listdir(image_folder) 
               if f.lower().endswith(".jpg")]

resized_images = []
target_size = (640, 480)

for img_path in image_files:
    img = Image.open(img_path).resize(target_size)
    resized_path = img_path.replace(".jpg", "_resized.jpg")
    img.save(resized_path)
    resized_images.append(resized_path)

audio = AudioFileClip(audio_path)
fps = (tempo / 60) * int(image_freq_var)  
num_frames = int(audio.duration * fps)
looped_images = (resized_images * ((num_frames // len(resized_images)) + 1))[:num_frames]



duration = len(image_files) / fps
clip = ImageSequenceClip(looped_images, fps=fps).with_audio(audio)

output_path = "" # Note to viewers - enter your desired output path here
print(f"'Writing to {output_path}")
clip.write_videofile(output_path, audio=True)

os.startfile(output_path)
