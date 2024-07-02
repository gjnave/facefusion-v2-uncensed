import os
import subprocess
import tkinter as tk
import yt_dlp

class TimeChooser(tk.Tk):
    def __init__(self, title="Time Chooser", start_time="00:00:00", video_duration="00:00:00"):
        super().__init__()

        self.title(title)
        self.geometry("300x240")

        self.current_time = start_time

        self.hours = int(start_time[:2])
        self.minutes = int(start_time[3:5])
        self.seconds = int(start_time[6:])

        self.video_duration = video_duration

        self.label_duration = tk.Label(self, text=f"Video Duration: {self.video_duration}", font=("Arial", 10))
        self.label_duration.pack(pady=5)

        self.label = tk.Label(self, text=self.current_time, font=("Arial", 24))
        self.label.pack(pady=10)

        self.frame = tk.Frame(self)
        self.frame.pack()

        self.create_buttons()

        self.btn_submit = tk.Button(self, text="Submit", command=self.update_time)
        self.btn_submit.pack(pady=10)

    def create_buttons(self):
        # Hour buttons
        btn_hour_up = tk.Button(self.frame, text="▲", width=5, command=lambda: self.change_time("hour", 1))
        btn_hour_up.grid(row=0, column=0, padx=5, pady=5)
        btn_hour_down = tk.Button(self.frame, text="▼", width=5, command=lambda: self.change_time("hour", -1))
        btn_hour_down.grid(row=0, column=1, padx=5, pady=5)
        lbl_hour = tk.Label(self.frame, text="Hour")
        lbl_hour.grid(row=0, column=2, padx=5, pady=5)

        # Minute buttons
        btn_minute_up = tk.Button(self.frame, text="▲", width=5, command=lambda: self.change_time("minute", 1))
        btn_minute_up.grid(row=1, column=0, padx=5, pady=5)
        btn_minute_down = tk.Button(self.frame, text="▼", width=5, command=lambda: self.change_time("minute", -1))
        btn_minute_down.grid(row=1, column=1, padx=5, pady=5)
        lbl_minute = tk.Label(self.frame, text="Minute")
        lbl_minute.grid(row=1, column=2, padx=5, pady=5)

        # Second buttons
        btn_second_up = tk.Button(self.frame, text="▲", width=5, command=lambda: self.change_time("second", 1))
        btn_second_up.grid(row=2, column=0, padx=5, pady=5)
        btn_second_down = tk.Button(self.frame, text="▼", width=5, command=lambda: self.change_time("second", -1))
        btn_second_down.grid(row=2, column=1, padx=5, pady=5)
        lbl_second = tk.Label(self.frame, text="Second")
        lbl_second.grid(row=2, column=2, padx=5, pady=5)

    def change_time(self, unit, delta):
        if unit == "hour":
            self.hours = (self.hours + delta) % 24
        elif unit == "minute":
            self.minutes = (self.minutes + delta) % 60
        elif unit == "second":
            self.seconds = (self.seconds + delta) % 60

        self.current_time = f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}"
        self.label.config(text=self.current_time)

    def update_time(self):
        self.destroy()

    def get_time(self):
        return self.current_time

def get_video_duration(video_url):
    # Function to get the duration of the video in seconds
    with yt_dlp.YoutubeDL({}) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        duration = int(info_dict['duration'])
        return duration

def download_audio_segment(video_url, start_time, end_time, output_format):
    # Function to download and process the audio segment
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'forcefilename': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }],
        'outtmpl': './outputs/audio-cut/%(title)s.%(ext)s',  # Output template
    }

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_title = info_dict.get('title', None)
        video_filename = f"./outputs/audio-cut/{video_title}.{output_format}" if video_title else f"./outputs/audio-cut/output.{output_format}"

    # Cut the downloaded audio file using FFmpeg
    output_filename = f"./outputs/audio-cut/{video_title}_cut.{output_format}" if video_title else f"./outputs/audio-cut/output_cut.{output_format}"
    start_time = convert_time_to_seconds(start_time)
    end_time = convert_time_to_seconds(end_time)
    subprocess.run(['ffmpeg', '-i', video_filename, '-ss', str(start_time), '-to', str(end_time), '-vn', output_filename])

    # Clean up temporary files
    os.remove(video_filename)

    # Print summary
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
    print("Your Audio has been Downloaded:")
    print(f"File: {output_filename}")
    print(f"Timestamp used: {start_time} to {end_time}")

def convert_time_to_seconds(time_str):
    # Convert time in format hh:mm:ss to seconds
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def choose_time(title="Choose Time", start_time="00:00:00", video_duration="00:00:00"):
    app = TimeChooser(title, start_time, video_duration)
    app.mainloop()
    return app.get_time()

def main():
    while True:
        video_url = input("Enter the URL of the video (or 'exit' to quit): ")

        if video_url.lower() == 'exit':
            break
        
        # Get video duration
        video_duration = get_video_duration(video_url)
        video_duration_str = f"{video_duration // 3600}:{(video_duration % 3600) // 60:02}:{video_duration % 60:02}"
        print(f"Video duration: {video_duration_str}")

        # Ask for start time using graphical interface
        start_time = choose_time("Choose Start Time", "00:00:00", video_duration_str)
        print(f"Start time selected: {start_time}")

        # Ask for end time using graphical interface, pre-filled with start time
        end_time = choose_time("Choose End Time", start_time, video_duration_str)
        print(f"End time selected: {end_time}")

        # Ask for output format choice
        print("Choose output format:")
        print("1: WAV")
        print("2: MP3")
        output_choice = input("Enter your choice (1 or 2): ")

        if output_choice == '1':
            output_format = 'wav'
        elif output_choice == '2':
            output_format = 'mp3'
        else:
            print("Invalid choice. Please choose 1 or 2.")
            continue

        # Ensure the output directory exists
        os.makedirs('./outputs/audio-cut', exist_ok=True)

        download_audio_segment(video_url, start_time, end_time, output_format)

       

if __name__ == "__main__":
    main()
