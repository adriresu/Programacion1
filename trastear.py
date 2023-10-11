from tkinter import filedialog
from PIL import Image
import exifread
import folium
import tkinter as tk
from tkinterhtml import HtmlFrame
import os

def convert_to_decimal_degrees(coord):
    if isinstance(coord.values[0], exifread.utils.Ratio):
        degrees = float(coord.values[0].num) / float(coord.values[0].den)
    else:
        degrees = float(coord.values[0])

    minutes = float(coord.values[1].num) / float(coord.values[1].den) / 60
    seconds = float(coord.values[2].num) / float(coord.values[2].den) / 3600

    if isinstance(degrees, float) and isinstance(minutes, float) and isinstance(seconds, float):
        return degrees + minutes + seconds
    else:
        return None

files_added = False
root = tk.Tk()
show_map_frame = None

def show_map():
    image_path = r'C:\Users\adrir\Desktop\alex.jpg'
    with open(image_path, 'rb') as image_file:
        metadata = exifread.process_file(image_file)

    # location data
    # region
    latitude = convert_to_decimal_degrees(metadata.get('GPS GPSLatitude'))
    longitude = convert_to_decimal_degrees(metadata.get('GPS GPSLongitude'))
    latitude_ref = metadata.get('GPS GPSLatitudeRef')
    longitude_ref = metadata.get('GPS GPSLongitudeRef')
    #endregion

    map = folium.Map(location=[latitude, longitude], zoom_start=2)
    map.save("map.html")
    return map

def add_files():
    global files_added
    global show_map_frame
    files = filedialog.askopenfilenames()
    for file in files:
        files_added = True
        print("Archivo añadido:", file)
    if files_added:
        show_map()
        show_map_frame = tk.Frame(root)
        frame = HtmlFrame(root, horizontal_scrollbar="auto")
        frame.set_content(os.getcwd() + "\\map.html")
        frame.pack()
    switch_view(show_map_frame)

def switch_view(frame):
    add_files_frame.pack_forget()
    if frame is not None:
        frame.pack_forget()
    frame.pack()

add_files_frame = tk.Frame(root)
add_files_button = tk.Button(add_files_frame, text="Añadir archivos", command=add_files)
add_files_button.pack()

switch_view(add_files_frame)

root.mainloop()