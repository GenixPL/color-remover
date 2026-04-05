import base64
import io

from PIL import Image, ImageOps
from pyscript import window, web, when, display, document
from js import console, fetch

@when("click", "#translate-button")
def translate_english(event):
    input_text = web.page["english"]
    english = input_text.value
    output_div = web.page["output"]
    output_div.innerText = english


@when("change", "#file-selector")
async def on_file_selected(event):
    # Grab the file list from the target element
    file_list = event.target.files

    if len(file_list) == 0:
        return

    selected_file = file_list.item(0)

    # ------------------------------------------------
    # 2. PIL Manipulation
    # ------------------------------------------------

    # 1. Read the file as an ArrayBuffer (raw bytes)
    # Using ArrayBuffer is more direct for converting to Python bytes than Base64
    array_buffer = await selected_file.arrayBuffer()

    # Convert JS ArrayBuffer to Python bytes
    img_bytes = array_buffer.to_py()

    # Open the image from bytes using io.BytesIO
    pil_image = Image.open(io.BytesIO(img_bytes))

    # --- Apply Manipulations here ---
    # Example 1: Convert to Grayscale
    pil_image = ImageOps.grayscale(pil_image)

    # ------------------------------------------------
    # 3. Convert PIL Image back to usable HTML format
    # ------------------------------------------------

    # Save the manipulated image to a BytesIO object
    buffered_output = io.BytesIO()
    # You must specify the format (PNG/JPEG).
    # PNG is usually safer for keeping transparency and quality.
    pil_image.save(buffered_output, format="PNG")

    # Get the bytes from the buffer
    new_img_bytes = buffered_output.getvalue()

    # Encode to base64 to set as src
    base64_str = base64.b64encode(new_img_bytes).decode('utf-8')

    # ------------------------------------------------
    # 4. Display the result
    # ------------------------------------------------
    img_element = document.querySelector("#output-image")
    img_element.src = f"data:image/png;base64,{base64_str}"
    img_element.style.display = "block"
    return 

    # We use the browser's FileReader API via the window object
    reader = window.FileReader.new()

    # Define what happens when the file is finished loading
    def on_load(e):
        img_element = document.querySelector("#output-image")
        # Set the result (base64 string) as the image source
        img_element.src = reader.result
        img_element.style.display = "block"

    # Assign the callback and read the file
    reader.onload = on_load
    reader.readAsDataURL(selected_file)