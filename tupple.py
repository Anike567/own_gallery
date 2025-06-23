import os

image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')  
drive_path = "D:\\"

# List to hold (timestamp, filepath) pairs
images = []

for root, dirs, files in os.walk(drive_path):
    # Skip node_modules directories
    dirs[:] = [d for d in dirs if d != 'node_modules']

    for file in files:
        if file.lower().endswith(image_extensions):
            path = os.path.join(root, file)
            try:
                timestamp = os.path.getmtime(path)  # Get last modified time
                images.append((timestamp, path))
            except Exception as e:
                print(f"Error reading file: {path} — {e}")

# Sort by time (oldest to newest)
images.sort()

# Print sorted image file paths
for ts, path in images:
    print(path)
