import os
import tkinter as tk
from tkinter import Scrollbar, Canvas
from PIL import Image, ImageTk, ImageChops
from threading import Thread
from queue import Queue

q = Queue()
image_labels = [] 
IMAGE_WIDTH = 300  
IMAGES_PER_ROW = 3  
index = 0  

# ----------- Read image paths from D drive -----------
def readImage():
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

    drive_path = "D:\\"

    for root, dirs, files in os.walk(drive_path):

        dirs[:] = [d for d in dirs if d != 'node_modules']

        for file in files:
            if file.lower().endswith(image_extensions):
                path = os.path.join(root, file)
                q.put(os.path.join(root, file))


    q.put(None)  #  mark end of images

# ----------- Show full image in popup -----------
def show_full_image(img_path):
    top = tk.Toplevel(root)
    top.title("Full View")
    img = Image.open(img_path)
    img_tk = ImageTk.PhotoImage(img)
    lbl = tk.Label(top, image=img_tk)
    lbl.image = img_tk
    lbl.pack()

# ----------- Display images in a scrollable grid -----------
def displayImages():
    global index
    row = col = 0
    while True:
        file_path = q.get()
        if file_path is None:
            break
        try:
            img = Image.open(file_path).convert("RGB")
            # Auto-crop whitespace
            bg = Image.new(img.mode, img.size, (255, 255, 255))
            diff = ImageChops.difference(img, bg)
            bbox = diff.getbbox()
            if bbox:
                img = img.crop(bbox)

            img.thumbnail((IMAGE_WIDTH, IMAGE_WIDTH))
            tk_img = ImageTk.PhotoImage(img)
            image_labels.append(tk_img)

            label = tk.Label(scrollable_frame, image=tk_img, bg="white")
            label.grid(row=row, column=col, padx=10, pady=10)
            label.bind("<Enter>", lambda e: e.widget.config(bg="lightblue"))
            label.bind("<Leave>", lambda e: e.widget.config(bg="white"))
            label.bind("<Button-1>", lambda e, path=file_path: show_full_image(path))

            col += 1
            if col >= IMAGES_PER_ROW:
                row += 1
                col = 0

        except Exception as e:
            print(f"Error loading image: {file_path}, {e}")

    canvas.config(scrollregion=canvas.bbox(tk.ALL))
    loading_label.destroy()

# ----------- GUI Setup -----------
root = tk.Tk()
root.title("Image Gallery")
root.geometry("1000x700")

# Frame for scrollable area
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

canvas = Canvas(frame, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

v_scroll = Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=v_scroll.set)

# Scrollable inner frame
scrollable_frame = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

# Update scroll region
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox(tk.ALL))

scrollable_frame.bind("<Configure>", on_configure)

# Mouse scroll (Windows only)
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ----------- Loading Indicator -----------
loading_label = tk.Label(root, text="Loading images...", font=("Arial", 16))
loading_label.pack()

# ----------- Start Threads -----------
t1 = Thread(target=readImage)
t2 = Thread(target=displayImages)
t1.start()
t2.start()

root.mainloop()
t1.join()
t2.join()
