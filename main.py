import asyncio
import base64
import io

from PIL import Image, ImageOps
from pyscript import window, web, when, display, document
from js import console, fetch


# Global variable to hold the processed image data
processed_image_data = None

color_to = (0, 0, 0, 0)
color_from = (0, 0, 0, 0)
threshold = 0

@when("change", "#file-selector")
async def on_file_selected(event):
    print("SELECTED")
    global processed_image_data

    # Grab the file list from the target element
    file_list = event.target.files

    if len(file_list) == 0:
        return

    selected_file = file_list.item(0)

    # 1. Read the file as an ArrayBuffer (raw bytes)
    # Using ArrayBuffer is more direct for converting to Python bytes than Base64
    array_buffer = await selected_file.arrayBuffer()

    # Convert JS ArrayBuffer to Python bytes
    img_bytes = array_buffer.to_py()

    new_img_bytes = io.BytesIO(img_bytes).getvalue()

    base64_str = base64.b64encode(new_img_bytes).decode('utf-8')

    processed_image_data = f"data:image/png;base64,{base64_str}"

    # ------------------------------------------------
    # 4. Display the result
    # ------------------------------------------------
    img_element = document.querySelector("#output-image")
    img_element.src = f"data:image/png;base64,{base64_str}"
    img_element.style.display = "block"

    # Show the download button
    document.querySelector("#btn-div").style.display = "inline-block"

@when("input", ".color-controls input")
def on_color_input(event):
    global color_from, color_to, threshold

    # Helper to grab values from the DOM
    def get_rgba(prefix):
        r = int(document.querySelector(f"#{prefix}-r").value or 0)
        g = int(document.querySelector(f"#{prefix}-g").value or 0)
        b = int(document.querySelector(f"#{prefix}-b").value or 0)
        a = int(document.querySelector(f"#{prefix}-a").value or 0)
        return (r, g, b, a)

    threshold = int(document.querySelector("#threshold").value or 0)
    color_from = get_rgba("from")
    color_to = get_rgba("to")

@when("click", "#download-btn")
def download_image(event):
    if processed_image_data:
        # Create a temporary anchor (<a>) element
        link = document.createElement("a")
        link.href = processed_image_data
        link.download =  "editted.png"  # The default filename

        # Trigger the download
        link.click()

@when("click", "#change-btn")
async def modify_image(event):
    # TODO(genix): add spinner

    print("1")
    global processed_image_data, color_to, color_from, threshold

    if processed_image_data is None:
        return

    img_element = document.querySelector("#output-image")
    print("2")

    # 2. Strip the header ("data:image/png;base64,")
    # We split by the comma and take the second part
    header, base64_str = processed_image_data.split(',')

    # 3. Decode the Base64 string into raw bytes
    img_bytes = base64.b64decode(base64_str)

    # 4. Open the image using io.BytesIO
    img = Image.open(io.BytesIO(img_bytes))
    img = img.convert("RGBA")
    # img = ImageOps.grayscale(img)
    # img = ImageOps.invert(img)

    datas = img.getdata()

    new_data = []
    for item in datas:
        # Check if pixel matches target color within a threshold
        is_match = all(abs(item[i] - color_from[i]) <= threshold for i in range(3))

        if is_match:
            new_data.append(color_to)
        else:
            new_data.append(item)

    print("3")

    # 1. Apply the data back to the image object

    img.putdata(new_data)

    # # 2. Save the image into a BytesIO buffer (instead of a physical path)
    buffered_output = io.BytesIO()
    img.save(buffered_output, format="PNG")

    print("4")

    # 3. Get the raw bytes from that buffer
    final_img_bytes = buffered_output.getvalue()

    # 4. Encode those bytes back to Base64 and update the global variable
    base64_encoded = base64.b64encode(final_img_bytes).decode('utf-8')
    processed_image_data = f"data:image/png;base64,{base64_encoded}"

    print("5")

    # 5. Update the UI so the user sees the change

    img_element.src = processed_image_data
    print("6")
