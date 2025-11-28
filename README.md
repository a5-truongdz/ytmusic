# ytmusic
A simple Youtube Music player in the terminal.

# Requirements
- Python 3.10 or higher - https://www.python.org
- ytmusicapi - https://github.com/sigma67/ytmusicapi
- colorama - https://pypi.org/project/colorama
- art - https://pypi.org/project/art
- typing - https://pypi.org/project/typing
- yt-dlp - https://github.com/yt-dlp/yt-dlp
- ffmpeg - https://www.ffmpeg.org

(Make sure you add ffplay to PATH!)

# Installation
- For Arch Linux

Update the system:
```
# pacman -Syu
```

Download necessary packages:
```
# pacman -S --needed yt-dlp ffmpeg python
```

Clone the repository (to home):
```
$ cd ~
$ git clone https://github.com/a5-truongdz/ytmusic.git
```

Download necessary pip packages:
```
$ cd ytmusic
$ pip install -r requirements.txt
```

# Launching
```
$ python ytmusic.py
```