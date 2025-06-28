import ffmpeg
import asyncio

async def convert_video_format(input_file_path: str, output_file_path: str):
    def run_ffmpeg():
        try:
            (
                ffmpeg
                .input(input_file_path)
                .output(output_file_path)
                .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            print("🚨 FFmpeg stderr:", e.stderr.decode())
            raise Exception("FFmpeg conversion failed") from e

    # ✅ Run in a background thread to avoid blocking FastAPI
    await asyncio.to_thread(run_ffmpeg)
