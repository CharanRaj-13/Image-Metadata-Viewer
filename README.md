# 📸 Image Metadata Viewer

A Python desktop application that extracts and displays detailed
information about an image, including file properties, image dimensions,
EXIF metadata, and GPS location when available.

Built with **Python**, **Tkinter**, and **Pillow**, the application
provides a simple interface for inspecting image metadata.

## ✨ Features

### 📁 File Information

-   File name and full file path
-   File extension and MIME type
-   File size in bytes and a readable format (KB or MB)
-   File creation and last-modified timestamps

### 🖼️ Image Properties

-   Image format
-   Width and height in pixels
-   Total pixel count
-   Aspect ratio
-   Color mode, number of color channels, and color bands
-   Number of frames and animation status
-   Transparency information, when available

### 📍 GPS Location Information

-   Extracts GPS metadata embedded in an image's EXIF data
-   Converts GPS coordinates to decimal latitude and longitude
-   Attempts to identify the location name using reverse geocoding
-   Provides a Google Maps link for available coordinates

### 🏷️ EXIF Metadata

-   Displays available EXIF tags and their values
-   Reports when EXIF metadata is unavailable

### 🪟 Desktop Interface

-   Built with Tkinter
-   File picker for selecting images
-   Scrollable metadata output
-   Error messages when an image cannot be opened or analyzed

## 🛠️ Technologies Used

-   **Python**: application logic
-   **Tkinter**: graphical user interface
-   **Pillow**: image processing and EXIF metadata extraction
-   **geopy**: reverse geocoding through Nominatim
-   **Python standard library**: file information, MIME type detection,
    and date formatting

## 📂 Supported Image Types

The file picker includes the following formats:

-   JPG / JPEG
-   PNG
-   GIF
-   BMP
-   WEBP
-   TIFF

Metadata availability depends on the image format and the information
embedded in the selected file.

## ⚙️ Requirements

-   Python 3.9 or later recommended
-   `Pillow`
-   `geopy`
-   Internet access for reverse geocoding of GPS coordinates

Tkinter is included with many Python installations. On some Linux
distributions, it may need to be installed separately.

## 🚀 Installation

### 1. Clone the repository

``` bash
git clone https://github.com/CharanRaj-13/Image-Metadata-Viewer.git
cd Image-Metadata-Viewer
```

### 2. (Optional) Create a virtual environment

**Windows**

``` bash
python -m venv .venv
.venv\\Scripts\\activate
```

**Linux / macOS**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
python -m pip install Pillow geopy
```

## ▶️ Usage

1.  Run the application:

    ``` bash
    python main.py
    ```

2.  Click **Select Image**.

3.  Choose an image from your computer.

4.  Review the displayed file information, image properties, GPS
    details, and available EXIF metadata.

5.  If GPS coordinates are embedded in the image, the application
    attempts to retrieve a readable location name and displays a Google
    Maps URL.

## 📍 Notes About GPS and Location Data

-   Not every image contains GPS metadata.
-   Social media platforms and image-editing tools may remove EXIF data
    when an image is uploaded or exported.
-   A location name can only be retrieved when usable GPS coordinates
    are present and the reverse-geocoding service is reachable.
-   Reverse geocoding requires an internet connection and depends on the
    Nominatim service.
-   Location results may be approximate or may not identify the exact
    place where a photo was taken.
-   The application sends coordinates to the reverse-geocoding service
    when requesting a location name. Avoid processing sensitive photos
    if you do not want their coordinates shared with an external
    service.
-   File creation timestamps can behave differently across operating
    systems and may not represent the original date the photo was taken.

## 🗂️ Project Structure

``` text
Image-Metadata-Viewer/
├── main.py
└── README.md
```

Your repository may contain additional files depending on how you
organize the project.

## 🔒 Privacy

Image metadata can contain sensitive information, including GPS
coordinates, device details, and timestamps. Be careful when sharing
images or metadata publicly.

The application processes the selected image locally for metadata
extraction, but the reverse-geocoding step sends its GPS coordinates to
Nominatim to look up a location name.

## 🛣️ Possible Future Improvements

-   Display a preview of the selected image
-   Export metadata to TXT, JSON, or CSV
-   Add a copy-to-clipboard option for GPS coordinates
-   Show the location on an embedded map
-   Add support for additional metadata standards
-   Improve handling of images with missing or malformed metadata

## 🤝 Contributing

Suggestions and improvements are welcome. To contribute, fork the
repository, create a branch for your changes, and submit a pull request.

## 📄 License

No license has been specified yet. Add a license file if you intend to
allow others to reuse, modify, or distribute this project.

------------------------------------------------------------------------

**Image Metadata Viewer**\
*Explore the information hidden inside your images.*
