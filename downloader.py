import yt_dlp
import os
from pathlib import Path
from typing import Optional, Dict


class MusicDownloader:
    def __init__(self, output_dir: str = "downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def download_as_mp3(self, video_info: Dict, filename: Optional[str] = None) -> Optional[str]:
        if not filename:
            safe_title = self._sanitize_filename(video_info['title'])
            safe_channel = self._sanitize_filename(video_info['channel'])
            filename = f"{safe_channel} - {safe_title}"
        
        output_path = self.output_dir / f"{filename}.mp3"
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(self.output_dir / f"{filename}.%(ext)s"),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'no_playlist': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading: {video_info['title']}")
                print(f"By: {video_info['channel']}")
                print(f"Duration: {video_info['duration']}")
                
                info = ydl.extract_info(video_info['url'], download=True)
                
                if output_path.exists():
                    print(f"\nSuccessfully downloaded to: {output_path}")
                    return str(output_path)
                else:
                    possible_path = self.output_dir / f"{filename}.mp3"
                    if possible_path.exists():
                        print(f"\nSuccessfully downloaded to: {possible_path}")
                        return str(possible_path)
                    
                    for file in self.output_dir.glob(f"{filename}*"):
                        if file.suffix == '.mp3':
                            print(f"\nSuccessfully downloaded to: {file}")
                            return str(file)
                    
                    print("Download completed but file location uncertain")
                    return None
                    
        except Exception as e:
            print(f"Download failed: {e}")
            return None
    
    def _sanitize_filename(self, filename: str) -> str:
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        filename = filename.strip('. ')
        
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename or "unknown"