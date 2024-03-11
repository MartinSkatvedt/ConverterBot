import os
from typing import Tuple
import requests

from moviepy.editor import *

def convert_webm_to_mp4(filename: str, webm_file_url: str) -> Tuple[str, str]:
    print(f"Converting {filename} to mp4...")

    # download the webm file
    r = requests.get(webm_file_url, allow_redirects=True)

    file_folder_name = filename.split(".")[0]
    parent_dir = f"./tmp/{file_folder_name}"

    os.makedirs(parent_dir, exist_ok=True)

    input_file = f"{parent_dir}/input.webm"

    open(input_file, "wb").write(r.content)
    
    output_file = f"{parent_dir}/output.mp4"

    # Load the .webm file
    clip = VideoFileClip(input_file)

    # Write the clip to an .mp4 file
    clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    # Close the clip
    clip.close()

    return output_file, parent_dir 

def clean_up_files(file_path: str):
    print(f"Cleaning up files in {file_path}...")
    os.remove(f"{file_path}/input.webm")
    os.remove(f"{file_path}/output.mp4")
    os.rmdir(file_path)


