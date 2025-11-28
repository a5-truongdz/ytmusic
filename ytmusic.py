import ytmusicapi
import colorama
import art
import subprocess
import os
import sys
from typing import *
import readchar
colorama.init(autoreset=True)

yt = ytmusicapi.YTMusic()

def clearTerminal() -> None:
    if os.name == "nt":
        os.system("cls");
    else:
        os.system("clear")

def playVideoId(videoId: str) -> None:
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
    return(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}[!]{colorama.Style.RESET_ALL} {message}")

def infoMessage(message: str) -> str:
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
            lyricsId: dict[str, list[dict[str, Any]] | str | None] = yt.get_watch_playlist(videoId=videoId)["lyrics"]
            try:
                lyrics: ytmusicapi.models.lyrics.Lyrics | ytmusicapi.models.lyrics.TimedLyrics | None = yt.get_lyrics(browseId=lyricsId)
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
        main()
    except KeyboardInterrupt:
        clearTerminal()
        print(infoMessage("Ctrl-C detected. Bye!"))
        exit(1)