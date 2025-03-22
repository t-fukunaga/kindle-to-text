import os
from PIL import Image
import argparse

def images_to_pdf(folder_path, output_path):
    # 画像ファイルのリストを取得
    image_files = [f for f in os.listdir(folder_path) if f.startswith("picture_") and f.endswith(".png")]
    image_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

    # 画像を読み込んでPDFに追加
    images = []
    for image_file in image_files:
        image_path = f"{folder_path}/{image_file}"
        try:
            image = Image.open(image_path)
            images.append(image.convert("RGB"))
        except FileNotFoundError:
            print(f"File not found: {image_path}")

    # 先頭の画像をベースにPDFを作成し、残りの画像を追加
    if images:
        images[0].save(
            output_path, "PDF", resolution=100.0,
            save_all=True, append_images=images[1:]
        )
        print(f"PDF created: {output_path}")
    else:
        print("No images found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert images to PDF")
    parser.add_argument("folder_path", help="Path to the folder containing images")
    parser.add_argument("output_path", help="Path to the output PDF file")
    args = parser.parse_args()

    images_to_pdf(args.folder_path, args.output_path)