"""
Kindle to PDF Converter for MacOS
"""
import os
import time
import cv2
import pyautogui
from PIL import Image
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Configuration variables with sensible defaults for MacOS
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", os.path.expanduser("~/Documents/KindlePDF"))
PAGE_TURN_KEY = os.getenv("PAGE_TURN_KEY", "right")  # right or left arrow key
CAPTURE_DELAY = float(os.getenv("CAPTURE_DELAY", "0.2"))  # seconds between captures

class KindleToPDF:
    """
    Simple tool to capture Kindle pages and convert them to PDF
    """
    
    def __init__(self):
        """Initialize folders"""
        # Create output folder if it doesn't exist
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
    
    def get_capture_coordinates(self):
        """
        Get the coordinates of the capture area from user
        
        Returns:
            tuple: (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)
        """
        print("\n===== KINDLE TO PDF CONVERTER =====")
        print("This tool will capture your Kindle pages and convert them to PDF.")
        
        # Get the left upper corner coordinates
        print("\n1. Place your cursor at the TOP-LEFT corner of the Kindle reading area")
        print("   You have 10 seconds to position your cursor...")
        for i in range(10, 0, -1):
            print(f"   {i}...", end="\r")
            time.sleep(1)
        
        upper_left_x, upper_left_y = pyautogui.position()
        print(f"   TOP-LEFT position captured: ({upper_left_x}, {upper_left_y})    ")
        
        # Get the right bottom corner coordinates
        print("\n2. Now place your cursor at the BOTTOM-RIGHT corner of the Kindle reading area")
        print("   You have 10 seconds to position your cursor...")
        for i in range(10, 0, -1):
            print(f"   {i}...", end="\r")
            time.sleep(1)
            
        bottom_right_x, bottom_right_y = pyautogui.position()
        print(f"   BOTTOM-RIGHT position captured: ({bottom_right_x}, {bottom_right_y})    ")
        
        return upper_left_x, upper_left_y, bottom_right_x, bottom_right_y

    def capture_kindle_pages(self, x1, y1, x2, y2, book_name):
        """
        Capture Kindle pages by taking screenshots and turning pages
        
        Args:
            x1, y1: Top-left coordinates
            x2, y2: Bottom-right coordinates
            book_name: Name of the book (used for folder name)
            
        Returns:
            tuple: (page_count, image_folder_path)
        """
        # Create a folder for this book
        book_folder = os.path.join(OUTPUT_FOLDER, book_name)
        images_folder = os.path.join(book_folder, "images")
        
        if not os.path.exists(book_folder):
            os.makedirs(book_folder)
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
            
        print(f"\n3. Capturing will begin in 5 seconds...")
        print("   Switch to your Kindle app and make sure it's in focus!")
        for i in range(5, 0, -1):
            print(f"   {i}...", end="\r")
            time.sleep(1)
        
        print("\n4. Starting capture - DO NOT MOVE OR USE YOUR COMPUTER!")
        print("   (Press Ctrl+C to stop capturing)")
        
        # Capture region dimensions
        width = x2 - x1
        height = y2 - y1
        
        # Capture the first page
        first_image_path = os.path.join(images_folder, f"page_0.png")
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        screenshot.save(first_image_path)
        
        # Now capture subsequent pages
        page = 1
        max_pages = 1000  # Safety limit
        
        try:
            while page < max_pages:
                # Turn the page
                pyautogui.press(PAGE_TURN_KEY)
                time.sleep(CAPTURE_DELAY)
                
                # Capture the new page
                current_image_path = os.path.join(images_folder, f"page_{page}.png")
                screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
                screenshot.save(current_image_path)
                
                # Compare with previous page to detect end of book
                prev_image = cv2.imread(os.path.join(images_folder, f"page_{page-1}.png"))
                curr_image = cv2.imread(current_image_path)
                
                # Convert images to grayscale
                prev_gray = cv2.cvtColor(prev_image, cv2.COLOR_BGR2GRAY)
                curr_gray = cv2.cvtColor(curr_image, cv2.COLOR_BGR2GRAY)
                
                # Calculate the difference between the two images
                diff = cv2.absdiff(prev_gray, curr_gray)
                non_zero_count = cv2.countNonZero(diff)
                
                # Print progress
                print(f"   Captured page {page} (diff: {non_zero_count})", end="\r")
                
                # If the difference is minimal, we've reached the end of the book or a stuck page
                if non_zero_count < 100:
                    print(f"\n   Detected end of book or no page turn at page {page}")
                    # Delete the duplicate page
                    os.remove(current_image_path)
                    page -= 1  # Adjust page count
                    break
                
                page += 1
                
        except KeyboardInterrupt:
            print("\n\nCapture interrupted by user")
        
        print(f"\n   Successfully captured {page+1} pages from Kindle")
        return page+1, images_folder
    
    def images_to_pdf(self, image_folder, pdf_output_path):
        """
        Convert captured images to a single PDF file
        
        Args:
            image_folder: Folder containing the images
            pdf_output_path: Path to save the PDF file
        """
        print("\n5. Converting images to PDF...")
        
        # Get list of image files
        image_files = [f for f in os.listdir(image_folder) if f.startswith("page_") and f.endswith(".png")]
        image_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
        
        # Open and convert images
        images = []
        for image_file in image_files:
            image_path = os.path.join(image_folder, image_file)
            try:
                with Image.open(image_path) as img:
                    # Convert to RGB (required for PDF)
                    rgb_img = img.convert("RGB")
                    images.append(rgb_img)
            except Exception as e:
                print(f"   Error processing {image_file}: {e}")
        
        # Save as PDF if we have images
        if images:
            first_image = images[0]
            first_image.save(
                pdf_output_path,
                save_all=True,
                append_images=images[1:],
                resolution=150.0
            )
            print(f"\n6. PDF created successfully: {pdf_output_path}")
        else:
            print("   No images found to convert to PDF")

def main():
    """Main function to run the Kindle to PDF converter"""
    global PAGE_TURN_KEY
    
    parser = argparse.ArgumentParser(description="Capture Kindle pages and convert to PDF")
    parser.add_argument("--book", help="Book name (used for folder naming)")
    parser.add_argument("--direction", choices=["right", "left"], default=PAGE_TURN_KEY,
                      help="Page turn direction (default: right)")
    args = parser.parse_args()
    
    # Override page turn key if specified
    if args.direction:
        PAGE_TURN_KEY = args.direction
    
    # Create converter instance
    converter = KindleToPDF()
    
    # Get book name
    book_name = args.book
    if not book_name:
        print("\nEnter a name for this book (used for folder naming):")
        book_name = input("> ").strip()
        if not book_name:
            book_name = f"kindle_book_{int(time.time())}"
    
    # Get capture coordinates
    x1, y1, x2, y2 = converter.get_capture_coordinates()
    
    # Capture pages
    page_count, images_folder = converter.capture_kindle_pages(x1, y1, x2, y2, book_name)
    
    # Path for the output PDF
    pdf_path = os.path.join(OUTPUT_FOLDER, book_name, f"{book_name}.pdf")
    
    # Convert to PDF
    converter.images_to_pdf(images_folder, pdf_path)
    
    print("\n===== CONVERSION COMPLETE =====")
    print(f"- Captured {page_count} pages")
    print(f"- Images saved to: {images_folder}")
    print(f"- PDF saved to: {pdf_path}")
    print("\nThank you for using Kindle to PDF Converter!")

if __name__ == "__main__":
    main()