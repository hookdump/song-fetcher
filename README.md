<p align="center">
  <img width="400" alt="image" src="https://github.com/user-attachments/assets/ea25339e-3e3d-48db-96a1-b69cab60a59f" />
</p>


# Song Fetcher

A command-line tool to search for songs and download them as MP3 files from YouTube.

<img width="1399" height="1224" alt="image" src="https://github.com/user-attachments/assets/3e43e166-4dc9-46cd-a94b-dc422722697f" />


## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Interactive mode (default):
```bash
python main.py
```

### Search directly from command line:
```bash
python main.py "Pink Champagne"
python main.py "In Christ Alone"
```

### Specify custom download folder:
```bash
python main.py -o ~/Music
python main.py --output /path/to/music/folder
```

### Combine search and custom folder:
```bash
python main.py -o ~/Music "In Christ Alone"
python main.py --output ~/Downloads "Pink Champagne"
```

1. If you provide a search term, it will search immediately
2. Review the search results  
3. Enter the number of the song you want to download
4. Confirm the download
5. The MP3 file will be saved in your specified folder (default: `downloads/`)
6. After downloading (or skipping), you can search for more songs

## Features

- Search YouTube for music videos
- Filter results to prioritize official releases
- Download and convert to MP3 format (192kbps)
- Clean, interactive CLI interface
- Automatic filename sanitization

## Requirements

- Python 3.8+
- ffmpeg (for audio conversion)

## Note

Make sure you have ffmpeg installed on your system:
- Ubuntu/Debian: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`
- Windows: Download from https://ffmpeg.org/download.html
