import os
import time

sart_time = time.time()

image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
drive_path = "D:\\"
image_files = []

for root, dirs, files in os.walk(drive_path):
    # Skip 'node_modules' directories
    dirs[:] = [d for d in dirs if d != 'node_modules']

    for file in files:
        if file.lower().endswith(image_extensions):
            image_files.append(os.path.join(root, file))

# Write all image file paths to b.txt
with open("b.txt", 'w', encoding='utf-8') as fl:
    for file in image_files:
        fl.write(file + '\n')

print(f"Total no of images: {len(image_files)}")

end_time = time.time()

print(end_time - sart_time)
