import subprocess
import json
import os


def generate_srt(json_data):
    transcript = json_data["transcript"]
    words = json_data["words"]

    srt_output = ""
    for i, word in enumerate(words, start=1):
        start_time = int(word["start"] * 1000)
        end_time = int(word["end"] * 1000)
        srt_output += f"{i}\n"
        srt_output += f"{format_time(start_time)} --> {format_time(end_time)}\n"
        srt_output += f"{word['word']}\n\n"

    return srt_output


def format_time(milliseconds):
    hours = milliseconds // (60 * 60 * 1000)
    minutes = (milliseconds // (60 * 1000)) % 60
    seconds = (milliseconds // 1000) % 60
    milliseconds = milliseconds % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def create_video_with_subtitles(video_path, json_file_path, video_output_path, subtitle_path):

    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    srt_content = generate_srt(json_data)
    srt_file_path = f"{subtitle_path}.srt"

    with open(srt_file_path, "w") as file:
        file.write(srt_content)

    print("SRT file saved successfully.")

    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles={srt_file_path}",
        video_output_path
    ]
    subprocess.call(cmd)

    print("Video with subtitles has been created and saved as:", video_output_path)

    # Remove the temporary subtitle file
    os.remove(srt_file_path)
