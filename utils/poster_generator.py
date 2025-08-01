from PIL import Image, ImageDraw, ImageFont

def generate_poster(img, text, font_path, font_size, font_color, alignment, orientation):
    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Handle vertical orientation
    if orientation == "vertical":
        text = "\n".join(text)

    # Create a temporary image just to calculate text size
    temp_img = Image.new("RGBA", (img.width, 1000), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    text_bbox = temp_draw.textbbox((0, 0), text, font=font)

    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Add some padding to the top section
    padding_top = 20
    padding_bottom = 20
    heading_height = text_height + padding_top + padding_bottom

    # Create new image with space for heading
    new_img = Image.new("RGBA", (img.width, heading_height + img.height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(new_img)

    # Calculate X position based on alignment
    if alignment == "center":
        x = (img.width - text_width) // 2
    elif alignment == "right":
        x = img.width - text_width - 20
    else:  # left
        x = 20

    y = padding_top  # Always start from top padding

    # Draw the text
    draw.text((x, y), text, font=font, fill=font_color)

    # Paste the original image below the text heading
    new_img.paste(img, (0, heading_height))

    return new_img
