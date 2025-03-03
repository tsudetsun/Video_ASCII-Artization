import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import argparse
import moviepy.editor as mp
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
import os
import multiprocessing

# アスキー文字セット
ASCII_SETS = {
    "default": "@%#*+=-:. ",
    "simple": "#@S%?*+;:,.",
    "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "
}

# 画像のサイズを変更する関数
def resize_image(image, char_width=4):
    height, width = image.shape[:2]
    ratio = height / width / 1.65
    new_width = int(width / char_width)
    new_height = int(new_width * ratio)
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
def image_to_ascii(image, ascii_chars, char_width=4, add_spaces=0, space_interval=9):
    image = resize_image(image, char_width)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image, ascii_chars)
    img_width = image.shape[1]
    ascii_str_len = len(ascii_str)
    
    ascii_img = ""
    for i in range(0, ascii_str_len, img_width):
        line = ascii_str[i:i+img_width]
        new_line = ""
        for j, char in enumerate(line):
            new_line += char
            if add_spaces > 0 and (j % space_interval) < add_spaces:
                new_line += char  # 左側の文字をコピーして空白を埋める
        ascii_img += new_line + "\n"
    
    return ascii_img

# フレームにアスキーアートを描画する関数
def draw_ascii_on_frame(ascii_img, frame_size, font_path="C:/Windows/Fonts/msgothic.ttc", font_size=10):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new("L", frame_size, color=255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), ascii_img, font=font, fill=0)
    return np.array(image)

# フレームを処理する関数
def process_frame(frame, width, height, font_path, font_size, add_spaces, space_interval, char_width, ascii_chars):
    ascii_img = image_to_ascii(frame, ascii_chars, char_width=char_width, add_spaces=add_spaces, space_interval=space_interval)
    ascii_frame = draw_ascii_on_frame(ascii_img, (width, height), font_path, font_size)
    return ascii_frame

# 動画をアスキーアートに変換する関数
def video_to_ascii(video_path, font_path, font_size, char_width, output_width, output_height, frame_skip, max_workers, ascii_set):
    cap = cv2.VideoCapture(video_path)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 縦横比に応じて補間する空白の数を計算
    aspect_ratio = height / width
    space_interval = 9
    add_spaces = max(0, int((1 / aspect_ratio) * space_interval - space_interval))
    
    # アスキーアートの行数と列数を計算
    sample_frame = cap.read()[1]
    sample_ascii_img = image_to_ascii(sample_frame, ASCII_SETS[ascii_set], char_width=char_width, add_spaces=add_spaces, space_interval=space_interval)
    lines = sample_ascii_img.split("\n")
    num_lines = len(lines)
    num_chars_per_line = len(lines[0]) if num_lines > 0 else 0
    
    # 新しい解像度を計算
    width_factor = round(0.5039 * font_size)
    if font_size < 10:
        height_factor = round(0.7474 * font_size + 5.4702)
    elif 10 <= font_size < 23:
        height_factor = round(1.02 * font_size + 4.6)
    else:
        height_factor = round(0.85 * font_size + 4.5, 1)
    
    new_height = height_factor * num_lines
    new_width = width_factor * num_chars_per_line
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('temp_video.avi', fourcc, fps / frame_skip, (new_width, new_height), isColor=False)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for frame_idx in tqdm(range(total_frames), desc="Processing frames"):
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % frame_skip == 0:
                futures.append(executor.submit(process_frame, frame, new_width, new_height, font_path, font_size, add_spaces, space_interval, char_width, ASCII_SETS[ascii_set]))
        
        for future in tqdm(futures, desc="Writing frames"):
            try:
                out.write(future.result())
            except Exception as e:
                print(f"Error processing frame {frame_idx}: {e}")

    cap.release()
    out.release()

    # temp_video.aviが正しく生成されたか確認
    if not os.path.exists('temp_video.avi'):
        raise FileNotFoundError("temp_video.aviが生成されませんでした。")

    video_clip = mp.VideoFileClip('temp_video.avi')
    audio_clip = mp.VideoFileClip(video_path).audio
    final_clip = video_clip.set_audio(audio_clip)
    
    final_clip = final_clip.resize(newsize=(output_width, output_height))
    
    base_name = os.path.basename(video_path)
    name, ext = os.path.splitext(base_name)
    
    # ユーザーフォルダ内のビデオフォルダに「ASCII-artized_videos」フォルダを作成
    video_folder = os.path.join(os.path.expanduser("~"), "Videos", "ASCII-artized_videos")
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    
    output_path = os.path.join(video_folder, f"{name}_asciivideo{ext}")
    counter = 1
    while os.path.exists(output_path):
        output_path = os.path.join(video_folder, f"{name}_asciivideo_{counter}{ext}")
        counter += 1
    
    final_clip.write_videofile(output_path, codec='libx264')

# メイン関数
def main():
    parser = argparse.ArgumentParser(description="Convert video to ASCII art")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("--font_path", default="C:/Windows/Fonts/msgothic.ttc", help="Path to the font file")
    parser.add_argument("--font_size", type=int, default=10, help="Font size for ASCII art")
    parser.add_argument("--char_width", type=int, default=4, help="Character width in pixels")
    parser.add_argument("--output_width", type=int, default=1280, help="Output video width")
    parser.add_argument("--output_height", type=int, default=720, help="Output video height")
    parser.add_argument("--frame_skip", type=int, default=1, help="Number of frames to skip")
    parser.add_argument("--max_workers", type=int, default=4, help="Number of parallel workers")
    parser.add_argument("--ascii_set", choices=ASCII_SETS.keys(), default="default", help="ASCII character set to use (default, simple, complex)")
    args = parser.parse_args()

    video_path = args.video_path.strip('"')

    video_to_ascii(video_path, args.font_path, args.font_size, args.char_width, args.output_width, args.output_height, args.frame_skip, args.max_workers, args.ascii_set)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
