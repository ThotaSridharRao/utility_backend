import ffmpeg
import os

async def convert_video_format(input_file_path: str, output_file_path: str):
    try:
        # Use FFmpeg to convert video format
        (
            ffmpeg
            .input(input_file_path)
            .output(output_file_path)
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        raise Exception("FFmpeg conversion failed") from e
