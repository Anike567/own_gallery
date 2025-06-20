from threading import Thread
import os
from queue import Queue
import time 
from PIL import Image


start_time = time.time()
q = Queue()

def readFile():
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

    drive_path = "D:\\"

    for root, dirs, files in os.walk(drive_path):

        dirs[:] = [d for d in dirs if d != 'node_modules']

        for file in files:
            if file.lower().endswith(image_extensions):
                q.put(os.path.join(root, file))

    q.put('Null')

def writeFile():
    with open("a.txt", 'w', encoding='utf-8') as fl:
        while True:
            file = q.get()
            if file == 'Null':
                break
            else:
                fl.write(file + '\n')

t1 = Thread(target=readFile)
t2 = Thread(target=writeFile)

t1.start()
t2.start()

t1.join()
t2.join()


end_time = time.time()

print(end_time - start_time)