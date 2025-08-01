import os

def list_fonts(font_dir="fonts"):
    fonts = []
    for folder in os.listdir(font_dir):
        folder_path = os.path.join(font_dir, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".ttf"):
                    fonts.append(f"{folder}/{file}")
    return fonts

def get_font_path(font_name, font_dir="fonts"):
    return os.path.join(font_dir, font_name) if font_name else None