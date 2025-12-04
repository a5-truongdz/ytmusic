# thats a huge amount of packages for a music player ngl
import ytmusicapi
import colorama
import art
import subprocess
import os
import sys
from typing import *
import readchar
import shutil
import distro

# windows
if os.name == "nt":
    colorama.init(autoreset=True)

yt = ytmusicapi.YTMusic()

def clearTerminal() -> None:
    if os.name == "nt":
        # windows
        os.system("cls");
    else:
        # unix
        os.system("clear")

def playVideoId(videoId: str) -> None:
    # use yt-dlp to stream audio to stdout
    # then pipe it to ffplay stdin to play
    ytDlp: subprocess.Popen = subprocess.Popen(
        ["yt-dlp", "-f", "bestaudio", "--remote-components", "ejs:github", "-o", "-", f"https://www.youtube.com/watch?v={videoId}"],
        stdout=subprocess.PIPE
    )
    ffplay: subprocess.Popen = subprocess.Popen(
        ["ffplay", "-vn", "-nodisp", "-autoexit", "-i", "-"],
        stdin=ytDlp.stdout,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    ffplay.wait()

def errorMessage(message: str) -> str:
    # [!]
    return(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}[!]{colorama.Style.RESET_ALL} {message}")

def infoMessage(message: str) -> str:
    # [*]
    return(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}[*]{colorama.Style.RESET_ALL} {message}")

def main() -> None:
    while True:
        clearTerminal()
        print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}{art.text2art("ytmusic")}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Style.BRIGHT}1.{colorama.Style.RESET_ALL} Search")
        print(f"{colorama.Style.BRIGHT}2.{colorama.Style.RESET_ALL} Play")
        print(f"{colorama.Style.BRIGHT}3.{colorama.Style.RESET_ALL} Lyrics")
        print(f"{colorama.Style.BRIGHT}4.{colorama.Style.RESET_ALL} Quit")
        while True:
            try:
                choice: int = int(input(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}>>>{colorama.Style.RESET_ALL} "))
            except ValueError:
                sys.stderr.write(errorMessage("Please enter a number.\n"))
                continue
            if not 0 < choice < 5:
                sys.stderr.write(errorMessage("Invalid choice.\n"))
                continue
            break
        if choice == 1:
            """
            i. videoId:
            Title: title
            Artists: artist1, artist2, ...
            Album: album

            """
            print(infoMessage("Enter a search query:"))
            query: str = input(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}>>>{colorama.Style.RESET_ALL} ")
            clearTerminal()
            results: list[dict[str, Any]] = yt.search(query=query, filter="songs", limit=5)
            for i, result in enumerate(results, 1):
                videoId: str = result["videoId"]
                title: str = result["title"]
                artists: str = ", ".join([artist["name"] for artist in result["artists"]])
                album: str = result["album"]["name"] if result["album"]["name"] != title else "Single"
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}{i}.{colorama.Style.RESET_ALL} {videoId}{colorama.Style.BRIGHT}:{colorama.Style.RESET_ALL}")
                print(f"Title: {colorama.Style.BRIGHT}{title}{colorama.Style.RESET_ALL}")
                print(f"Artists: {colorama.Style.BRIGHT}{artists}{colorama.Style.RESET_ALL}")
                print(f"Album: {colorama.Style.BRIGHT}{album}{colorama.Style.RESET_ALL}")
                print()
            print("Press any key to continue...", end="", flush=True)
            readchar.readkey()
        if choice == 2:
            # get videoid from search, duh
            print(infoMessage("Enter a video ID:"))
            while True:
                videoId: str = input(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}>>>{colorama.Style.RESET_ALL} ")
                metadata: dict[str, Any] = yt.get_song(videoId=videoId)
                if metadata["playabilityStatus"]["status"] != "OK":
                    sys.stderr.write(errorMessage("Invalid video ID!\n"))
                    continue 
                break
            clearTerminal()
            print(infoMessage(f"Playing {metadata["videoDetails"]["title"]} by {metadata["videoDetails"]["author"]}!"))
            playVideoId(videoId)
            print("Press any key to continue...", end="", flush=True)
            readchar.readkey()
        if choice == 3:
            print(infoMessage("Enter a video ID:"))
            while True:
                videoId: str = input(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}>>>{colorama.Style.RESET_ALL} ")
                metadata: dict[str, Any] = yt.get_song(videoId=videoId)
                if metadata["playabilityStatus"]["status"] != "OK":
                    sys.stderr.write(errorMessage("Invalid video ID!\n"))
                    continue 
                break
            clearTerminal()
            # get browseid from watch playlist (idk why yt put it there)
            browseId: dict[str, list[dict[str, Any]] | str | None] = yt.get_watch_playlist(videoId=videoId)["lyrics"]
            try:
                # pass it to get_lyrics
                lyrics: ytmusicapi.models.lyrics.Lyrics | ytmusicapi.models.lyrics.TimedLyrics | None = yt.get_lyrics(browseId=browseId)
            except ytmusicapi.exceptions.YTMusicUserError:
                print(infoMessage(f"{metadata["videoDetails"]["title"]} by {metadata["videoDetails"]["author"]} doesn't have lyrics."))
                print(infoMessage(f"Or Youtube hasn't update it yet."))
            else:
                print(infoMessage(f"Lyrics of {metadata["videoDetails"]["title"]} by {metadata["videoDetails"]["author"]}:"))
                print()
                print(f"{colorama.Style.BRIGHT}{lyrics["lyrics"]}{colorama.Style.RESET_ALL}")
            print()
            print("Press any key to continue...", end="", flush=True)
            readchar.readkey()
        if choice == 4:
            clearTerminal()
            print(infoMessage("Bye!"))
            break

if __name__ == "__main__":
    try:
        # arch linux support
        # im too lazy for other distros
        if not shutil.which("yt-dlp"):
            print(errorMessage("yt-dlp is not installed. It is required to download music."))
            if distro.id() == "arch":
                print(infoMessage("Arch Linux detected. Do you want to install it automatically? [y/N]"))
                while True:
                    choice: str = input(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}>>>{colorama.Style.RESET_ALL} ").lower()
                    if not choice or not choice in ["y", "n"]:
                        continue
                    if choice == "n":
                        print(errorMessage("Please install yt-dlp and run this again."))
                        exit(1)
                    if choice == "y":
                        if subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "yt-dlp"]).returncode != 0:
                            print(errorMessage("An error occurred. Please try again."))
                            exit(1)
                        break
            else:
                exit(1)
        if not shutil.which("ffplay"):
            print(errorMessage("ffmpeg is not installed. It is required to download music."))
            if distro.id() == "arch":
                print(infoMessage("Arch Linux detected. Do you want to install it automatically? [y/N]"))
                while True:
                    choice: str = input(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}>>>{colorama.Style.RESET_ALL} ").lower()
                    if not choice or not choice in ["y", "n"]:
                        continue
                    if choice == "n":
                        print(errorMessage("Please install ffmpeg and run this again."))
                        exit(1)
                    if choice == "y":
                        if subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "ffmpeg"]).returncode != 0:
                            print(errorMessage("An error occurred. Please try again."))
                            exit(1)
                        break
            else:
                exit(1)
        if not shutil.which("deno"):
            print(errorMessage("deno is not installed. It is required to download music."))
            if distro.id() == "arch":
                print(infoMessage("Arch Linux detected. Do you want to install it automatically? [y/N]"))
                while True:
                    choice: str = input(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}>>>{colorama.Style.RESET_ALL} ").lower()
                    if not choice or not choice in ["y", "n"]:
                        continue
                    if choice == "n":
                        print(errorMessage("Please install deno and run this again."))
                        exit(1)
                    if choice == "y":
                        if subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "deno"]).returncode != 0:
                            print(errorMessage("An error occurred. Please try again."))
                            exit(1)
                        break
            else:
                exit(1)
    except KeyboardInterrupt:
        clearTerminal()
        print(infoMessage("Ctrl-C detected. Bye!"))
        exit(1)
    try:
        main()
    except KeyboardInterrupt:
        clearTerminal()
        print(infoMessage("Ctrl-C detected. Bye!"))
        exit(1)