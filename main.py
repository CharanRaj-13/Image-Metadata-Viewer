import tkinter as tk
from tkinter import filedialog
from PIL import Image, ExifTags
from geopy.geocoders import Nominatim

import os
import mimetypes
from datetime import datetime


# ==========================================
# FORMAT FILE SIZE
# ==========================================

def format_size(size):

    if size < 1024:
        return f"{size} bytes"

    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"

    else:
        return f"{size / (1024 * 1024):.2f} MB"


# ==========================================
# GET FILE DATES
# ==========================================

def get_file_dates(file_path):

    created = os.path.getctime(file_path)
    modified = os.path.getmtime(file_path)

    created_date = datetime.fromtimestamp(
        created
    ).strftime("%Y-%m-%d %H:%M:%S")

    modified_date = datetime.fromtimestamp(
        modified
    ).strftime("%Y-%m-%d %H:%M:%S")

    return created_date, modified_date


# ==========================================
# CONVERT GPS COORDINATES
# ==========================================

def convert_to_degrees(value):

    degrees = float(value[0])
    minutes = float(value[1])
    seconds = float(value[2])

    return degrees + (
        minutes / 60.0
    ) + (
        seconds / 3600.0
    )


# ==========================================
# EXTRACT GPS DATA
# ==========================================

def get_gps_data(image):

    gps_info = {}

    try:

        exif = image.getexif()

        # GPSInfo EXIF tag is usually 34853
        gps_tag = None

        for tag_id, tag_name in ExifTags.TAGS.items():

            if tag_name == "GPSInfo":

                gps_tag = tag_id
                break


        if gps_tag is not None and gps_tag in exif:

            gps_data = exif.get(gps_tag)

            # Convert GPS tag numbers to readable names
            for key in gps_data:

                gps_name = ExifTags.GPSTAGS.get(
                    key,
                    key
                )

                gps_info[gps_name] = gps_data[key]


    except Exception as error:

        print(f"GPS Error: {error}")


    return gps_info


# ==========================================
# GET LATITUDE AND LONGITUDE
# ==========================================

def get_decimal_coordinates(gps_info):

    latitude = None
    longitude = None

    try:

        # LATITUDE
        if (
            "GPSLatitude" in gps_info
            and "GPSLatitudeRef" in gps_info
        ):

            latitude = convert_to_degrees(
                gps_info["GPSLatitude"]
            )

            if gps_info["GPSLatitudeRef"] == "S":

                latitude = -latitude


        # LONGITUDE
        if (
            "GPSLongitude" in gps_info
            and "GPSLongitudeRef" in gps_info
        ):

            longitude = convert_to_degrees(
                gps_info["GPSLongitude"]
            )

            if gps_info["GPSLongitudeRef"] == "W":

                longitude = -longitude


    except Exception as error:

        print(f"Coordinate Error: {error}")


    return latitude, longitude


# ==========================================
# GET LOCATION NAME FROM COORDINATES
# ==========================================

def get_location_name(latitude, longitude):

    if latitude is None or longitude is None:

        return "Not Available"


    try:

        geolocator = Nominatim(
            user_agent="image_metadata_viewer"
        )

        location = geolocator.reverse(
            f"{latitude}, {longitude}",
            language="en"
        )


        if location:

            return location.address

        else:

            return "Location name not found"


    except Exception as error:

        return f"Could not retrieve location: {error}"


# ==========================================
# GET ALL EXIF METADATA
# ==========================================

def get_all_exif(image):

    exif_metadata = []

    try:

        exif = image.getexif()

        if exif:

            for tag_id, value in exif.items():

                tag_name = ExifTags.TAGS.get(
                    tag_id,
                    tag_id
                )

                exif_metadata.append(
                    f"{tag_name}: {value}"
                )


    except Exception as error:

        exif_metadata.append(
            f"Could not read EXIF data: {error}"
        )


    return exif_metadata


# ==========================================
# SELECT IMAGE
# ==========================================

def select_image():

    file_path = filedialog.askopenfilename(

        title="Select an Image",

        filetypes=[

            (
                "Image Files",

                (
                    "*.jpg",
                    "*.jpeg",
                    "*.png",
                    "*.gif",
                    "*.bmp",
                    "*.webp",
                    "*.tiff"
                )

            ),

            ("All Files", "*.*")

        ]

    )


    if not file_path:

        return


    try:

        # ==========================================
        # OPEN IMAGE
        # ==========================================

        image = Image.open(file_path)


        # ==========================================
        # FILE INFORMATION
        # ==========================================

        file_name = os.path.basename(file_path)

        file_extension = os.path.splitext(
            file_path
        )[1]

        file_size_bytes = os.path.getsize(
            file_path
        )

        file_size = format_size(
            file_size_bytes
        )

        created_date, modified_date = get_file_dates(
            file_path
        )

        mime_type, encoding = mimetypes.guess_type(
            file_path
        )


        # ==========================================
        # IMAGE INFORMATION
        # ==========================================

        width, height = image.size

        total_pixels = width * height

        aspect_ratio = width / height

        image_format = image.format

        color_mode = image.mode

        frames = getattr(
            image,
            "n_frames",
            1
        )

        is_animated = getattr(
            image,
            "is_animated",
            False
        )

        channels = len(
            image.getbands()
        )

        color_bands = ", ".join(
            image.getbands()
        )

        transparency = image.info.get(
            "transparency",
            "Not Available"
        )


        # ==========================================
        # EXIF DATA
        # ==========================================

        exif_metadata = get_all_exif(
            image
        )


        # ==========================================
        # GPS DATA
        # ==========================================

        gps_info = get_gps_data(
            image
        )

        latitude, longitude = get_decimal_coordinates(
            gps_info
        )


        # ==========================================
        # LOCATION NAME
        # ==========================================

        if latitude is not None and longitude is not None:

            result_text.delete(
                "1.0",
                tk.END
            )

            result_text.insert(
                tk.END,
                "🔍 Extracting location information...\n"
            )

            root.update()

            location_name = get_location_name(
                latitude,
                longitude
            )

            maps_link = (
                f"https://www.google.com/maps?q="
                f"{latitude},{longitude}"
            )

        else:

            location_name = "Not Available"

            maps_link = "Not Available"


        # ==========================================
        # BUILD METADATA OUTPUT
        # ==========================================

        metadata = f"""
════════════════════════════════════════════
           📸 IMAGE METADATA VIEWER
════════════════════════════════════════════


📁 FILE INFORMATION
────────────────────────────────────────────

File Name:
{file_name}

Full Path:
{file_path}

Extension:
{file_extension}

MIME Type:
{mime_type}

File Size:
{file_size}

File Size (Bytes):
{file_size_bytes:,}

Created:
{created_date}

Last Modified:
{modified_date}


🖼️ IMAGE PROPERTIES
────────────────────────────────────────────

Format:
{image_format}

Width:
{width} pixels

Height:
{height} pixels

Total Pixels:
{total_pixels:,}

Aspect Ratio:
{aspect_ratio:.4f}:1

Color Mode:
{color_mode}

Color Channels:
{channels}

Color Bands:
{color_bands}

Number of Frames:
{frames}

Animated:
{is_animated}

Transparency:
{transparency}


📍 GPS LOCATION INFORMATION
────────────────────────────────────────────

Latitude:
{latitude if latitude is not None else "Not Available"}

Longitude:
{longitude if longitude is not None else "Not Available"}

Location Name:
{location_name}

Google Maps:
{maps_link}


📸 ALL AVAILABLE EXIF METADATA
────────────────────────────────────────────
"""


        if exif_metadata:

            for item in exif_metadata:

                metadata += f"\n{item}\n"

        else:

            metadata += (
                "\nNo EXIF metadata found.\n"
            )


        # ==========================================
        # DISPLAY METADATA
        # ==========================================

        result_text.delete(
            "1.0",
            tk.END
        )

        result_text.insert(
            tk.END,
            metadata
        )


        image.close()


    except Exception as error:

        result_text.delete(
            "1.0",
            tk.END
        )

        result_text.insert(

            tk.END,

            f"""
❌ ERROR

Could not open or analyze this image.

Details:

{error}
"""

        )


# ==========================================
# CREATE GUI
# ==========================================

root = tk.Tk()

root.title(
    "Image Metadata & Location Viewer"
)

root.geometry(
    "900x750"
)


# ==========================================
# TITLE
# ==========================================

title_label = tk.Label(

    root,

    text="📸 Image Metadata & Location Viewer",

    font=(
        "Arial",
        20,
        "bold"
    )

)

title_label.pack(
    pady=15
)


# ==========================================
# SELECT IMAGE BUTTON
# ==========================================

select_button = tk.Button(

    root,

    text="📁 Select Image",

    font=(
        "Arial",
        12
    ),

    command=select_image,

    padx=15,

    pady=8

)

select_button.pack(
    pady=10
)


# ==========================================
# METADATA FRAME
# ==========================================

frame = tk.Frame(
    root
)

frame.pack(

    fill="both",

    expand=True,

    padx=20,

    pady=15

)


# ==========================================
# SCROLLBAR
# ==========================================

scrollbar = tk.Scrollbar(
    frame
)

scrollbar.pack(

    side="right",

    fill="y"

)


# ==========================================
# TEXT AREA
# ==========================================

result_text = tk.Text(

    frame,

    font=(
        "Consolas",
        10
    ),

    wrap="word",

    yscrollcommand=scrollbar.set

)

result_text.pack(

    side="left",

    fill="both",

    expand=True

)


scrollbar.config(
    command=result_text.yview
)


# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()