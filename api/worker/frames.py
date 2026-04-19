import subprocess

def extract_frames(video_path: str, time_stamps: list[float], job_id: str) -> list[str]:
    """Extract frames from the video at the specified timestamps and prep for storage.

    Args:
        video_path: Local file path to the video.
        time_stamps: List of timestamps (in seconds) at which to extract frames.
        job_id: Used to name the output files uniquely.
        
    Returns:
        List of local file paths to the extracted frames.
    """
    frame_paths: list[str] = []
    for time in time_stamps:
        frame_output_path = f"/tmp/{job_id}_{time}.jpg"
        subprocess.run(
            ["ffmpeg", "-ss", str(time), "-i", video_path, "-frames:v", "1", "-y", frame_output_path], check=True
        )
        frame_paths.append(frame_output_path)

    return frame_paths
#EOF





if __name__ == "__main__":
    # Example usage
    VIDEO_PATH = "/tmp/example-job-id.mp4"  # This should be the path to the downloaded video/audio file
    TIME_STAMPS = [10.0, 30.0, 60.0]  # Example timestamps in seconds
    JOB_ID = "example-job-id"
    
    print("Extracting frames...")
    frame_paths = extract_frames(VIDEO_PATH, TIME_STAMPS, JOB_ID)
    print("Extracted frame paths:")
    for path in frame_paths:
        print(path)