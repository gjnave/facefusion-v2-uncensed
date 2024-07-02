import tkinter as tk
from tkinter import filedialog, simpledialog
import os
import subprocess

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png"), ("All Files", "*.*")]
    )

    return file_path

def convert_to_video(input_file, duration, quality_option):
    if not input_file:
        print("No file selected or operation cancelled.")
        return

    # Check if the selected file exists
    if not os.path.exists(input_file):
        print(f"Selected file does not exist: {input_file}")
        return

    # Prepare output video file name based on the input image name
    file_name, file_ext = os.path.splitext(os.path.basename(input_file))
    output_file = f"img-vid\\{file_name}.mkv"

    if quality_option == 1:  # Good Quality / Low Size
        ffmpeg_cmd = [
            "ffmpeg",
            "-loop", "1",
            "-i", input_file,
            "-c:v", "h264",
            "-crf", "23",  # Adjust as needed for quality vs size trade-off
            "-t", str(duration),
            output_file
        ]
    elif quality_option == 2:  # Excellent Quality / Huge Size
        ffmpeg_cmd = [
            "ffmpeg",
            "-loop", "1",
            "-i", input_file,
            "-c:v", "prores_ks",
            "-profile:v", "3",  # Profile 3 is for ProRes 422 HQ, offering higher quality
            "-t", str(duration),
            "-pix_fmt", "yuv422p10le",
            output_file
        ]
    else:
        print("Invalid quality option selected.")
        return

    # Run ffmpeg command
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Conversion completed: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def main():
    input_file = select_file()
    if not input_file:
        return  # Exit if no file selected
    
    # Ask user for video duration
    duration_str = simpledialog.askstring("Video Duration", "Enter video duration in seconds:")
    if duration_str is None:
        return  # Exit if user cancels

    # Convert duration string to integer
    try:
        duration = int(duration_str)
        if duration <= 0:
            print("Duration must be a positive integer.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return

    # Ask user for quality option
    quality_option_str = simpledialog.askstring("Quality Option", "Choose quality option:\n1) Good Quality / Low Size\n2) Excellent Quality / Potentially Huge")
    if quality_option_str is None:
        return  # Exit if user cancels
    
    try:
        quality_option = int(quality_option_str)
        if quality_option not in [1, 2]:
            print("Invalid quality option selected.")
            return
    except ValueError:
        print("Invalid input. Please enter 1 or 2.")
        return

    convert_to_video(input_file, duration, quality_option)

if __name__ == "__main__":
    main()
