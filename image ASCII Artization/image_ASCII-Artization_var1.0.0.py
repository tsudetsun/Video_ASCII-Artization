import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import argparse
import os
import sys

# アスキー文字セット
ASCII_SETS = {
    "default": "@%#*+=-:. ",
    "simple": "#@S%?*+;:,.",
    "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "
}

# フォントサイズに応じた文字の幅と高さを計算する関数
def calculate_char_size(font_size):
    char_width = round(0.5039 * font_size)
    if font_size < 10:
        char_height = round(0.7474 * font_size + 5.4702)
    elif 10 <= font_size < 23:
        char_height = round(1.02 * font_size + 4.6)
    else:
        char_height = round(0.85 * font_size + 4.5, 1)
    return char_width, char_height

# 画像のサイズを変更する関数
def resize_image(image, char_width=5.0, char_height=13.0):
    height, width = image.shape[:2]
    new_width = int(width / char_width)
    new_height = int(height / char_height)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

# 画像をグレースケールに変換する関数
def grayify(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# グレースケール画像のピクセルをアスキー文字に変換する関数
def pixels_to_ascii(image, ascii_chars):
    pixels = image.flatten()
    ascii_str = "".join([ascii_chars[min(pixel // (256 // len(ascii_chars)), len(ascii_chars) - 1)] for pixel in pixels])
    return ascii_str

# 画像をアスキーアートに変換する関数
def image_to_ascii(image, ascii_chars, char_width=5.0, char_height=13.0):
    image = resize_image(image, char_width, char_height)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image, ascii_chars)
    img_width = image.shape[1]
    ascii_str_len = len(ascii_str)
    
    ascii_img = ""
    for i in range(0, ascii_str_len, img_width):
        line = ascii_str[i:i+img_width]
        ascii_img += line + "\n"
    
    return ascii_img

# 画像にアスキーアートを描画する関数
def draw_ascii_on_image(ascii_img, image_size, font_path="C:/Windows/Fonts/msgothic.ttc", font_size=10):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new("L", image_size, color=255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), ascii_img, font=font, fill=0)
    return np.array(image)

# 画像をアスキーアートに変換して保存する関数
def image_file_to_ascii(image_path, font_path, font_size, ascii_set):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")
    
    # 日本語ファイル名を処理できるようにするため、cv2.imdecodeを使用
    with open(image_path, 'rb') as f:
        file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")
    
    height, width = image.shape[:2]
    
    # フォントサイズに応じた文字の幅と高さを計算
    char_width, char_height = calculate_char_size(font_size)
    
    # char_widthとchar_heightを表示
    print(f"char_width: {char_width}, char_height: {char_height}")
    
    ascii_img = image_to_ascii(image, ASCII_SETS[ascii_set], char_width=char_width, char_height=char_height)
    ascii_image = draw_ascii_on_image(ascii_img, (width, height), font_path, font_size)
    
    # ユーザーフォルダ内のピクチャフォルダに「ASCII-artized_images」フォルダを作成
    picture_folder = os.path.join(os.path.expanduser("~"), "Pictures", "ASCII-artized_images")
    if not os.path.exists(picture_folder):
        os.makedirs(picture_folder)
    
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    output_path = os.path.join(picture_folder, f"{name}_asciiimage{ext}")
    counter = 1
    while os.path.exists(output_path):
        output_path = os.path.join(picture_folder, f"{name}_asciiimage_{counter}{ext}")
        counter += 1
    
    cv2.imwrite(output_path, ascii_image)

# メイン関数
def main():
    parser = argparse.ArgumentParser(description="Convert image to ASCII art")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("--font_path", default="C:/Windows/Fonts/msgothic.ttc", help="Path to the font file")
    parser.add_argument("--font_size", type=int, default=10, help="Font size for ASCII art")
    parser.add_argument("--ascii_set", choices=ASCII_SETS.keys(), default="default", help="ASCII character set to use (default, simple, complex)")
    
    # 日本語ファイル名を処理できるようにするため、sys.argvをエンコードして解析
    args = parser.parse_args()
    
    image_file_to_ascii(args.image_path, args.font_path, args.font_size, args.ascii_set)

if __name__ == "__main__":
    main()