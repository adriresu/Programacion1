from tkinter import filedialog
from tkinter import *
from PIL import ImageTk
from PIL import Image
import exifread
import folium
import os
import tkintermapview

def convert_to_decimal_degrees(gps_coords, gps_coords_ref):
    d, m, s =  gps_coords.values
    dd = d + m / 60 + s / 3600
    if gps_coords_ref.values.upper() in ('S', 'W'):
        return -dd
    elif gps_coords_ref.values.upper() in ('N', 'E'):
        return dd
    else:
        raise RuntimeError('Incorrect gps_coords_ref {}'.format(gps_coords_ref))

def get_coordinates(image_path):
    with open(image_path, 'rb') as image_file:
        metadata = exifread.process_file(image_file)
    # location data
    latitude = False
    longitude = False
    if metadata:
        print(metadata)
    if metadata.get('GPS GPSLatitude') or metadata.get('GPS GPSLongitude'):
        latitude = convert_to_decimal_degrees(metadata.get('GPS GPSLatitude'), metadata.get("GPS GPSLatitudeRef"))
        longitude = convert_to_decimal_degrees(metadata.get('GPS GPSLongitude'), metadata.get("GPS GPSLongitudeRef"))
        latitude_ref = metadata.get('GPS GPSLatitudeRef')
        longitude_ref = metadata.get('GPS GPSLongitudeRef')
        # print("Tiene coordenadas: {} {} {} {} {}".format(latitude, longitude, latitude_ref, longitude_ref))
    return latitude, longitude

# Add files
root = Tk()

root.attributes('-fullscreen', True)

root.title("AÑADIR ARCHIVOS")

root.geometry("1820x980")

my_label = LabelFrame(root)

my_label.pack(pady=20)

locations = {}

files = filedialog.askopenfilenames()

for file_path in files:
    latitude, longitude = get_coordinates(file_path)
    locations[file_path.split("/")[-1]] = {"latitude":latitude, "longitude":longitude} if latitude and longitude else None

map_widget = tkintermapview.TkinterMapView(my_label, width=1920, height=1080, corner_radius=0)
map_widget.set_zoom(3)

def marker_callback(marker):
    print(marker.text)
    marker.delete()

map_widget.pack()

for file_path in files:
    image_name = file_path.split("/")[-1]
    if locations[image_name]:
        image_marker = ImageTk.PhotoImage(Image.open(file_path).resize((40, 40)))
        marker = map_widget.set_marker(locations[image_name]["latitude"], locations[image_name]["longitude"], text=image_name, icon=image_marker, image_zoom_visibility=(0, float("inf")), command=marker_callback)

map_widget.set_position(40.447303, 3.998593, marker=False)

# for location in locations:
#     latitude = list(location.keys())[0]
#     longitude = location[latitude]
#     map_widget.add_marker(latitude, longitude)

root.mainloop()