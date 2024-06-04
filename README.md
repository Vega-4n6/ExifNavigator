# ExifNavigator

ExifNavigator is an OSINT tool for extracting and analyzing EXIF data from images. It lists all JPG and JPEG files in a given folder, extracts EXIF data, saves it to a CSV file, and plots images with GPS coordinates on a map.

## Features

- Extracts EXIF data including:
  - GPS coordinates (latitude and longitude)
  - Device information (make and model)
  - Image creation date and time
- Saves EXIF data to a CSV file
- Plots images with GPS coordinates on an interactive map

## Installation

### Prerequisites

Ensure you have Python 3.x installed. You can download Python from [python.org](https://www.python.org/).

### Clone the Repository

1. Open your terminal or command prompt.
2. Run the following command to clone the repository:
   ```bash
   git clone https://github.com/your-username/exifnavigator.git
   cd exifnavigator
   ```


## Install Dependencies
Run the following command to install the required Python packages:
     ```bash
     
     pip install -r requirements.txts
     

## How to Use
1. Run the Tool:

Execute the Python script from the command line using the following command:

  ```Bash
  python exifnavigator.py
  ```


2. Provide the Folder Path:

When prompted, enter the path to the folder containing the images you want to analyze. Here's an example:

```bash 
Enter the folder path containing images: /path/to/images
```

3. View the Output:

The tool will perform the following actions:

List all JPG and JPEG files within the specified folder.
Extract EXIF data from each image.
Save the extracted data to a CSV file named exifnavigator_data.csv located in the current directory.
The CSV file will contain columns for:

Filename
-Image DateTime

-GPSLatitude

-GPSLongitude

-Make

-Model


4. Plotting GPS Coordinates (Optional):

If the images contain GPS coordinates, the tool will generate an interactive map using folium, visualizing the image locations. This map will open in your default web browser.
