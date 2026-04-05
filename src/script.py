from PIL import Image

def remove_color(image_path, target_color, output_path, threshold=0):
    """
    Removes a specific color from an image.

    :param image_path: Path to input image
    :param target_color: Tuple (R, G, B) to remove
    :param output_path: Path to save result (must be .png for transparency)
    :param threshold: How 'close' a color must be to be removed (0 is exact match)
    """
    img = Image.open(image_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Check if pixel matches target color within a threshold
        is_match = all(abs(item[i] - target_color[i]) <= threshold for i in range(3))

        if is_match:
            # Replace with transparent pixel
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Success! Saved to {output_path}")


# --- Usage ---
# Target color as (Red, Green, Blue)
# Example: Pure white is (255, 255, 255)
target = (48, 48, 48)

remove_color("images/myword-banner.jpg", target, "images/myword-banner.png", threshold=100,)