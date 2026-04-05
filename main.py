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

    if len(file_list) > 0:
        selected_file = file_list.item(0)

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