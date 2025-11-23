import ytmusicapi
import colorama
import art
import subprocess
import os
import sys
from typing import *
from pydbus import SessionBus
from gi.repository import GLib
import threading
from pydbus.generic import signal
colorama.init(autoreset=True)

# Creating the MPRIS server
with open("mpris.xml", "r") as m:
    MPRIS_METADATA_ONLY: str = m.read()
bus: Any = SessionBus()
loop: None = GLib.MainLoop()
class Mpris:
    PropertiesChanged: signal = signal()
    def __init__(self) -> None:
        self.metadata: dict[None] = {}
        self.playbackStatus: str = "Paused"
    def Quit(self):
        loop.quit()
    @property
    def CanQuit(self) -> bool:
        return True
    @property
    def CanRaise(self) -> bool:
        return False
    @property
    def HasTrackList(self) -> bool:
        return False
    @property
    def Identity(self) -> str:
        return "ytmusic"
    @property
    def SupportedUriSchemes(self) -> list[None]:
        return []
    @property
    def SupportedMimeTypes(self) -> list[None]:
        return []
    @property
    def PlaybackStatus(self) -> str:
        return self.playbackStatus
    @property
    def Metadata(self) -> dict[str, str | int]:
        return self.metadata
    @property
    def DesktopEntry(seslf) -> str:
        return "ytmusic"
    @property
    def Position(self) -> int:
        return 1000
    def Get(self, interface: str, prop: str) -> Any:
        if interface == "org.mpris.MediaPlayer2":
            return GLib.Variant("v", GLib.Variant(self._prop_type(prop), getattr(self, prop)))
        if interface == "org.mpris.MediaPlayer2.Player":
            return GLib.Variant("v", GLib.Variant(self._prop_type(prop), getattr(self, prop)))
        return GLib.Variant("v", None)
    def GetAll(self, interface: str) -> Any:
        result: dict[str, Any] = {}
        if interface == "org.mpris.MediaPlayer2":
            result = {
                "CanQuit": GLib.Variant("b", self.CanQuit),
                "CanRaise": GLib.Variant("b", self.CanRaise),
                "HasTrackList": GLib.Variant("b", self.HasTrackList),
                "Identity": GLib.Variant("s", self.Identity),
                "DesktopEntry": GLib.Variant("s", self.DesktopEntry),
                "SupportedUriSchemes": GLib.Variant("as", self.SupportedUriSchemes),
                "SupportedMimeTypes": GLib.Variant("as", self.SupportedMimeTypes),
            }
        elif interface == "org.mpris.MediaPlayer2.Player":
            result = {
                "PlaybackStatus": GLib.Variant("s", self.playbackStatus),
                "Metadata": GLib.Variant("a{sv}", self.metadata),
            }

        return result
    def Set(self, interface: str, prop: str, value) -> None:
        pass
    def _prop_type(self, prop: str) -> str:
        TYPES: dict[str, str] = {
            "PlaybackStatus": "s",
            "Metadata": "a{sv}",
            "CanQuit": "b",
            "CanRaise": "b",
            "HasTrackList": "b",
            "Identity": "s",
            "SupportedUriSchemes": "as",
            "SupportedMimeTypes": "as",
            "DesktopEntry": "s",
            "Position": "x"
        }
        return TYPES[prop]
    def updateMetadata(self, update: bool, title: str, artist: str, length: int) -> None:
        if update:
            self.metadata: dict[str, str | int | list] = {
                "xesam:title": GLib.Variant("s", title),
                "xesam:artist": GLib.Variant("as", [artist]),
                "mpris:length": GLib.Variant("x", int(length) * 1000000),
            }
            self.playbackStatus = "Playing"
        else:
            self.metadata: dict[None] = {}
            self.playbackStatus = "Paused"
        self.PropertiesChanged(
            "org.mpris.MediaPlayer2.ytmusic",
            {
                "Metadata": GLib.Variant("a{sv}", self.metadata),
                "PlaybackStatus": GLib.Variant("s", self.playbackStatus)
            },
            []
        )
player: Mpris = Mpris()
bus.publish("org.mpris.MediaPlayer2.ytmusic", ("/org/mpris/MediaPlayer2", player, MPRIS_METADATA_ONLY))
yt: ytmusicapi.YTMusic = ytmusicapi.YTMusic()

# Running the loop in the background
threading.Thread(target=loop.run, daemon=True).start()

def clearTerminal() -> None:
    """
    Clear the terminal. Support both Windows and Linux.
    """
    if os.name == "nt":
        os.system("cls");
    else:
        os.system("clear")

def playVideoId(videoId: str) -> None:
    """
    Play a song with an ID `videoId` (https://www.youtube.com/watch?v=`videoId`).
    With `yt-dlp` and `ffplay`.

    :param videoId: The ID of the song.
    """
    ytDlp = subprocess.Popen(
        ["yt-dlp", "-f", "bestaudio", "--remote-components", "ejs:github", "-o", "-", f"https://www.youtube.com/watch?v={videoId}"],
        stdout=subprocess.PIPE
    )
    ffplay = subprocess.Popen(
        ["ffplay", "-vn", "-nodisp", "-autoexit", "-i", "-"],
        stdin=ytDlp.stdout,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    ffplay.wait()

def errorMessage(message: str) -> str:
    """
    Return '[!] `message`'.

    :param message: The message.
    """
    return(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}[!]{colorama.Style.RESET_ALL} {message}")

def infoMessage(message: str) -> str:
    """
    Return '[*] `message`'.

    :param message: The message.
    """
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
            1. `videoId`:
            Title: `title`
            Artists: `artists`
            Album: `album`
            """
            print(infoMessage("Enter a search query:"))
            query: str = input(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}>>>{colorama.Style.RESET_ALL} ")
            clearTerminal()
            results: list[dict[str, Any]] = yt.search(query=query, filter="songs", limit=5)
            for i, result in enumerate(results, 1):
                videoId = result["videoId"]
                title = result["title"]
                artists = ", ".join([artist["name"] for artist in result["artists"]])
                album = result["album"]["name"] if result["album"]["name"] != title else "Single"
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}{i}.{colorama.Style.RESET_ALL} {videoId}{colorama.Style.BRIGHT}:{colorama.Style.RESET_ALL}")
                print(f"Title: {colorama.Style.BRIGHT}{title}{colorama.Style.RESET_ALL}")
                print(f"Artists: {colorama.Style.BRIGHT}{artists}{colorama.Style.RESET_ALL}")
                print(f"Album: {colorama.Style.BRIGHT}{album}{colorama.Style.RESET_ALL}")
                print()
            input("Press any key to continue...")
        if choice == 2:
            # Get `videoId` from search.
            print(infoMessage("Enter a video ID:"))
            while True:
                # Check if videoId is a song.
                videoId: str = input(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}>>>{colorama.Style.RESET_ALL} ")
                metadata: dict[str, Any] = yt.get_song(videoId=videoId)
                if metadata["playabilityStatus"]["status"] != "OK":
                    sys.stderr.write(errorMessage("Invalid video ID!\n"))
                    continue 
                break
            clearTerminal()
            title = metadata["videoDetails"]["title"]
            artist = metadata["videoDetails"]["author"]
            seconds = metadata["videoDetails"]["lengthSeconds"]
            print(infoMessage(f"Playing {title} by {artist}!"))
            player.updateMetadata(update=True, title=title, artist=artist, length=seconds)
            playVideoId(videoId)
            player.updateMetadata(update=False, title="", artist="", length="")
            print()
            input("Press any key to continue...")
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
            # Getting browseId, starts with "MPLYt...".
            lyricsId: dict[str, list[dict[str, Any]] | str | None] = yt.get_watch_playlist(videoId=videoId)["lyrics"]
            try:
                # Fetching lyrics from browseId.
                lyrics: ytmusicapi.models.lyrics.Lyrics | ytmusicapi.models.lyrics.TimedLyrics | None = yt.get_lyrics(browseId=lyricsId)
            except ytmusicapi.exceptions.YTMusicUserError:
                # Failed fetching lyrics.
                print(infoMessage(f"{metadata["videoDetails"]["title"]} by {metadata["videoDetails"]["author"]} doesn't have lyric."))
                print(infoMessage("Or Youtube hasn't update it yet."))
            else:
                print(infoMessage(f"Lyrics of {metadata["videoDetails"]["title"]} by {metadata["videoDetails"]["author"]}:"))
                print()
                print(lyrics["lyrics"])
            print()
            input("Press any key to continue...")
        if choice == 4:
            clearTerminal()
            print(infoMessage("Bye!"))
            exit(0)

if __name__ == "__main__":
    main()