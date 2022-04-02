"""
FLPInfo
~~~~~~~

Prints basic information about an FL Studio project file (.flp).
"""  # noqa

import argparse
import os

import colorama

from pyflp import Parser
from pyflp.arrangement import Arrangement
from pyflp.misc import Misc
from pyflp.channel import Channel
from pyflp.pattern import Pattern


class FLPInfo:
    """Prints basic information about an FL Studio project file (.flp)."""

    def __init__(self, args) -> None:
        """Initialises colored output if needed and finds terminal column width.

        Args:
            args: Arguments passed from command line.
        """
        colorama.init(autoreset=True)
        self.__bad_flp = False
        self.__term_cols = os.get_terminal_size().columns
        self.__path = args.flp
        self.__no_color = args.no_color
        self.__full_lists = args.full_lists
        self.__new_channel = False

    def __color(self, color, what) -> str:
        if self.__no_color:
            return what
        return color + str(what) + colorama.Style.RESET_ALL

    def __green(self, what):
        return self.__color(colorama.Fore.GREEN, what)

    def __cyan(self, what):
        return self.__color(colorama.Fore.CYAN, what)

    def __yellow(self, what):
        return self.__color(colorama.Fore.YELLOW, what)

    def __bright(self, what):
        return self.__color(colorama.Style.BRIGHT, what)

    def __red(self, what):
        self.__bad_flp = True
        return self.__color(colorama.Fore.RED, what)

    def __print_col(self, kind, what):
        """Clip output at the end of the terminal to truncate long lists."""
        kind = self.__bright(kind)
        if not self.__full_lists:
            if len(str(what)) > self.__term_cols:
                end = "...]" if what[-1] == "]" else "..."
                what = what[: self.__term_cols - 20] + end
        print(kind, what)

    def info(self):
        """Gathers events and collects event data to print it."""
        events = Parser().get_events(self.__path)

        title = artists = genre = comments = version = url = tempo = None
        channels, arrangements, patterns = [], [], []

        for e in events:
            if e.id == Misc.EventID.Artists:
                artists = e.to_str()
            elif e.id == Misc.EventID.Comment:
                comments = e.to_str()
            elif e.id == Misc.EventID.Genre:
                genre = e.to_str()
            elif e.id == Misc.EventID.Tempo:
                tempo = e.to_uint32() / 1000
            elif e.id == Misc.EventID.Url:
                url = e.to_str()
            elif e.id == Misc.EventID.Version:
                version = e.to_str()
            elif e.id == Channel.EventID.New:
                self.__new_channel = True
            elif e.id == Channel.EventID.DefaultName:
                channels.append(e.to_str())
            elif e.id == Channel.EventID.Name:
                if self.__new_channel:
                    channels[-1] = e.to_str()
                    self.__new_channel = False
            elif e.id == Arrangement.EventID.Name:
                arrangements.append(e.to_str())
            elif e.id == Pattern.EventID.Name:
                patterns.append(e.to_str())

        self.__print_col("Title:           ", self.__green(title))
        self.__print_col("Artist(s):       ", self.__green(artists))
        self.__print_col("Genre:           ", self.__green(genre))
        self.__print_col("Tempo (BPM):     ", self.__green(tempo))
        self.__print_col("Comments:        ", comments)  # TODO Formatting

        url = self.__cyan(url) if url else ""
        self.__print_col("Project URL:     ", url)
        self.__print_col("FL Version:      ", self.__green(version))

        ch_len = len(channels)
        if ch_len == 0:
            channels = self.__red(0)
        else:
            channels = f"{self.__green(ch_len)} [{', '.join(channels)}]"
        self.__print_col("Channel(s):      ", channels)

        arr_len = len(arrangements)
        if arr_len == 0:
            arrangements = self.__red(0)
        else:
            arrangements = f"{self.__green(arr_len)} [{', '.join(arrangements)}]"
        self.__print_col("Arrangement(s):  ", arrangements)

        pat_len = len(patterns)
        if pat_len == 0:
            patterns = self.__yellow(0)
        else:
            # c_p = [self.blue(p) for p in patterns]
            patterns = f"{self.__green(pat_len)} [{', '.join(patterns)}]"
        self.__print_col("Pattern(s):      ", patterns)

        if not self.__full_lists:
            print(
                "\nIf you want to see the full lists run with the",
                self.__bright("--full-lists"),
                "option.",
            )

        if self.__bad_flp:
            print(
                "\nFLP seems to have been corrupted, try inspecting in",
                self.__cyan("FLPInspect"),
            )


def main():
    """Parses the command line arguments and passes them to `FLPInfo`."""
    ap = argparse.ArgumentParser(prog="flpinfo", description=FLPInfo.__doc__)
    ap.add_argument(
        "flp",
        help="The location of FLP to show information about. "
        "Zipped FLPs are not yet supported!",
    )
    ap.add_argument(
        "--full-lists",
        action="store_true",
        help="Lists will not appear truncated.",
    )
    ap.add_argument(
        "--no-color",
        action="store_true",
        help="Disables colored output",
    )
    args = ap.parse_args()
    FLPInfo(args).info()


if __name__ == "__main__":
    main()
