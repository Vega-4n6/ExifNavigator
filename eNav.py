import os
import csv
import folium
from PIL import Image
from exifread import process_file

def get_jpg_files(folder_path):
    jpg_files = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg")):
            jpg_files.append(os.path.join(folder_path, filename))
    return jpg_files

def extract_exif_data(image_path):
    exif_data = {}
    try:
        with open(image_path, 'rb') as image_file:
            tags = process_file(image_file)
            if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                lat = tags['GPS GPSLatitude'].values
                lon = tags['GPS GPSLongitude'].values
                lat_ref = tags['GPS GPSLatitudeRef'].values
                lon_ref = tags['GPS GPSLongitudeRef'].values
                exif_data['GPSLatitude'] = convert_to_degrees(lat, lat_ref)
                exif_data['GPSLongitude'] = convert_to_degrees(lon, lon_ref)
            if 'EXIF DateTimeOriginal' in tags:
                exif_data['DateTime'] = str(tags['EXIF DateTimeOriginal'])
            if 'Image Make' in tags:
                exif_data['Make'] = str(tags['Image Make'])
            if 'Image Model' in tags:
                exif_data['Model'] = str(tags['Image Model'])
            exif_data['ImageName'] = os.path.basename(image_path)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error accessing image: {image_path} - {e}")
    return exif_data

def convert_to_degrees(value, ref):
    d = value[0].num / value[0].den
    m = value[1].num / value[1].den
    s = value[2].num / value[2].den

    result = d + (m / 60.0) + (s / 3600.0)
    if ref in ['S', 'W']:
        result = -result
    return result

def create_csv(image_data, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['ImageName', 'DateTime', 'GPSLatitude', 'GPSLongitude', 'Make', 'Model']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in image_data.values():
            row = {field: data.get(field, '0') for field in fieldnames}
            writer.writerow(row)

def plot_gps_images(image_data, map_filename):
    m = folium.Map(location=[0, 0], zoom_start=2)
    for data in image_data.values():
        if 'GPSLatitude' in data and 'GPSLongitude' in data:
            latitude = data['GPSLatitude']
            longitude = data['GPSLongitude']
            popup = f"Image: {data['ImageName']}<br>Date/Time: {data.get('DateTime', 'Unknown')}<br>Make: {data.get('Make', 'Unknown')}<br>Model: {data.get('Model', 'Unknown')}"
            folium.Marker([latitude, longitude], popup=popup).add_to(m)
    m.save(map_filename)
    print(f"Saved map with images to {map_filename}.")

def main():
    folder_path = input("Enter the folder path containing images: ")

    # List JPG/JPEG files
    jpg_files = get_jpg_files(folder_path)
    if not jpg_files:
        print("No JPG or JPEG files found in the specified folder.")
        return

    # Extract EXIF data and store in dictionary
    image_data = {}
    for image in jpg_files:
        exif_data = extract_exif_data(image)
        image_data[image] = exif_data

    # Create CSV file with EXIF data
    csv_filename = "image_navigator_data.csv"
    create_csv(image_data, csv_filename)
    print(f"EXIF data saved to CSV file: {csv_filename}")

    # Plot images with GPS coordinates on a map
    map_filename = "images_map.html"
    plot_gps_images(image_data, map_filename)

if __name__ == "__main__":
    main()
