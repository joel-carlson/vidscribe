# Downloading the video
import yt_dlp 
import os



def download_video(video_url: str, job_id: str) -> str:
    """Download video to local temp storage.                                                                                                                                  
    
    Args:                                                                                                                                                                     
        video_url: YouTube URL or GCS path.
        job_id: Used to name the output file uniquely.                                                                                                                        
    
    Returns:                                                                                                                                                                  
        Local file path to the downloaded video.                                                                                                                              
    """
    output_path = f"/tmp/{job_id}.mp4"
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "outtmpl": output_path,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return output_path




if __name__ == "__main__":
    # Example usage
    video_url = "https://www.youtube.com/watch?v=DgXV8QSlI4U&list=WL&index=26&t=19s"
    job_id = "example-job-id"
    local_video_path = download_video(video_url, job_id)
    print(f"Video downloaded to: {local_video_path}")