from tkinter import filedialog
from tkinter import *
from PIL import ImageTk
from PIL import Image
import exifread
import folium
import os
import tkintermapview

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

def get_coordinates(image_path):
    with open(image_path, 'rb') as image_file:
        metadata = exifread.process_file(image_file)
    # location data
    latitude = False
    longitude = False
    if metadata.get('GPS GPSLatitude') or metadata.get('GPS GPSLongitude'):
        latitude = convert_to_decimal_degrees(metadata.get('GPS GPSLatitude'))
        longitude = convert_to_decimal_degrees(metadata.get('GPS GPSLongitude'))
        latitude_ref = metadata.get('GPS GPSLatitudeRef')
        longitude_ref = metadata.get('GPS GPSLongitudeRef')
    return latitude, longitude

# Add files
root = Tk()

root.attributes('-fullscreen', True)

root.title("AÑADIR ARCHIVOS")

root.geometry("1820x980")

my_label = LabelFrame(root)

my_label.pack(pady=20)

locations = []

files = filedialog.askopenfilenames()

for file_path in files:
    latitude, longitude = get_coordinates(file_path)
    locations.append({latitude:longitude}) if latitude and longitude else None

map_widget = tkintermapview.TkinterMapView(my_label, width=1920, height=1080, corner_radius=0)
map_widget.set_zoom(8)

def marker_callback(marker):
    print(marker.text)
    marker.delete()

map_widget.pack()

for file_path in files:
    image_marker = ImageTk.PhotoImage(Image.open(file_path).resize((40, 40)))
    marker_1 = map_widget.set_marker(52.476062, 13.394172, text=file_path.split("/")[-1], icon=image_marker, command=marker_callback)

map_widget.set_position(40.447303, -3.998593, marker=False)

# for location in locations:
#     latitude = list(location.keys())[0]
#     longitude = location[latitude]
#     map_widget.add_marker(latitude, longitude)

root.mainloop()