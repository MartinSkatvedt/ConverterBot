import os
import shutil
from typing import Tuple

import requests
from moviepy.editor import VideoFileClip


def get_parent_dir(filename: str) -> str:
    """Per-conversion directory, derived from the attachment filename."""
    file_folder_name = filename.split(".")[0]
    return f"./tmp/{file_folder_name}"


def convert_webm_to_mp4(filename: str, webm_file_url: str) -> Tuple[str, str]:
    print(f"Converting {filename} to mp4...")

    parent_dir = get_parent_dir(filename)
    os.makedirs(parent_dir, exist_ok=True)

    input_file = f"{parent_dir}/input.webm"
    output_file = f"{parent_dir}/output.mp4"

    # Download the webm file. Context managers guarantee the socket and the
    # file handle are released even if the write fails partway.
    with requests.get(webm_file_url, allow_redirects=True) as r:
        r.raise_for_status()
        with open(input_file, "wb") as f:
            f.write(r.content)

    # VideoFileClip spawns an ffmpeg subprocess connected by OS pipes. The
    # try/finally guarantees clip.close() terminates that subprocess and frees
    # its file descriptors even when write_videofile raises (corrupt input,
    # unsupported codec, etc.) -- otherwise they leak until the process hits
    # the open-file limit and crashes.
    clip = VideoFileClip(input_file)
    try:
        clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
    finally:
        clip.close()

    return output_file, parent_dir


def clean_up_files(file_path: str) -> None:
    print(f"Cleaning up files in {file_path}...")
    # rmtree (vs os.remove + os.rmdir) tolerates partial conversions, leftover
    # moviepy *TEMP_MPY_* audio files, and a missing directory.
    shutil.rmtree(file_path, ignore_errors=True)
