import os
import tkinter as tk
from tkinter import Canvas, Scrollbar
from PIL import Image, ImageTk, ImageChops

# ----- Configuration -----
drive_path = "D:\\"  # Scan entire D drive
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
IMAGE_WIDTH = 150
IMAGES_PER_ROW = 5

images = []
image_labels = []
loading = True
angle = 0  # rotation angle
original_spinner = None

# ----- Animate Static Spinner by Rotation -----
def rotate_spinner():
    global angle
    if not loading or original_spinner is None:
        spinner_label.place_forget()
        return

    rotated = original_spinner.rotate(angle)
    spinner_tk = ImageTk.PhotoImage(rotated)
    spinner_label.config(image=spinner_tk)
    spinner_label.image = spinner_tk  # prevent garbage collection

    angle = (angle + 10) % 360
    root.after(50, rotate_spinner)

# ----- Scan and Display Images -----
def displayImages():
    global images, loading

    for root_dir, dirs, files in os.walk(drive_path):
        dirs[:] = [d for d in dirs if d != 'node_modules']
        for file in files:
            if file.lower().endswith(image_extensions):
                path = os.path.join(root_dir, file)
                try:
                    timestamp = os.path.getmtime(path)
                    images.append((timestamp, path))
                except Exception as e:
                    print(f"Error reading file: {path} — {e}")

    if not images:
        spinner_label.config(text="No images found on D: drive.")
        loading = False
        return

    images.sort()

    row = col = 0
    for _, file_path in images:
        try:
            img = Image.open(file_path)

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
    loading = False  # stop spinner

# ----- Show Full Image on Click -----
def show_full_image(path):
    top = tk.Toplevel(root)
    top.title("Full Image")
    try:
        img = Image.open(path)
        tk_img = ImageTk.PhotoImage(img)
        label = tk.Label(top, image=tk_img)
        label.image = tk_img
        label.pack()
    except Exception as e:
        print(f"Failed to open full image: {e}")

# ----- Tkinter GUI Setup -----
root = tk.Tk()
root.title("Image Gallery")
root.geometry("1000x700")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

canvas = Canvas(frame, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

v_scroll = Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=v_scroll.set)

scrollable_frame = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox(tk.ALL))

scrollable_frame.bind("<Configure>", on_configure)

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ----- Static Spinner Image Setup -----
spinner_label = tk.Label(root, bg="white")
spinner_label.place(relx=0.5, rely=0.5, anchor="center")  # Center of window

try:
    original_spinner = Image.open("spinner.gif").convert("RGBA")
except Exception as e:
    print(f"⚠️ Could not load spinner.gif: {e}")
    original_spinner = None

# ----- Start -----
root.after(100, displayImages)
rotate_spinner()
root.mainloop()
