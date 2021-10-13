"""Prints basic information about an FLP."""

import logging
import os

import colorama

from pyflp import Parser
from pyflp.flobject.arrangement.enums import ArrangementEvent
from pyflp.flobject.misc.enums import MiscEvent
from pyflp.flobject.channel.enums import ChannelEvent
from pyflp.flobject.pattern.enums import PatternEvent


class FLPInfo:
    def __init__(self, args) -> None:
        colorama.init(autoreset=True)
        self.__bad_flp = False
        self.__term_cols = os.get_terminal_size().columns
        self.path = args.flp
        self.__no_color = args.no_color
        self.__verbose = True if args.verbose else False
        self.__full_lists = args.full_lists

    def color(self, color, what):
        if self.__no_color:
            return what
        return color + str(what) + colorama.Style.RESET_ALL

    def green(self, what):
        return self.color(colorama.Fore.GREEN, what)

    def cyan(self, what):
        return self.color(colorama.Fore.CYAN, what)

    def yellow(self, what):
        return self.color(colorama.Fore.YELLOW, what)

    def bright(self, what):
        return self.color(colorama.Style.BRIGHT, what)

    def red(self, what):
        self.__bad_flp = True
        return self.color(colorama.Fore.RED, what)

    def print_col(self, kind, what):
        """Clip output to the end of a terminal columns.
        This will ensure long lists get truncated."""
        kind = self.bright(kind)
        if not (self.__verbose or self.__full_lists):
            if len(what) > self.__term_cols:
                end = "...]" if what[-1] == "]" else "..."
                what = what[: self.__term_cols - 20] + end
        print(kind, what)

    def info(self):
        if self.__verbose:
            parser = Parser(self.__verbose)
        else:
            parser = Parser(True, verbosity=logging.ERROR)
        events = parser.get_events(self.path)

        title = artists = genre = comments = version = url = tempo = None
        channels, arrangements, patterns = [], [], []

        for e in events:
            if e.id == MiscEvent.Artists:
                artists = e.to_str()
            elif e.id == MiscEvent.Comment:
                comments = e.to_str()
            elif e.id == MiscEvent.Genre:
                genre = e.to_str()
            elif e.id == MiscEvent.Tempo:
                tempo = e.to_uint32() / 1000
            elif e.id == MiscEvent.Url:
                url = e.to_str()
            elif e.id == MiscEvent.Version:
                version = e.to_str()
            elif e.id == ChannelEvent.New:
                self.__new_channel = True
            elif e.id == ChannelEvent.DefaultName:
                channels.append(e.to_str())
            elif e.id == ChannelEvent.Name:
                if self.__new_channel:
                    channels[-1] = e.to_str()
                    self.__new_channel = False
            elif e.id == ArrangementEvent.Name:
                arrangements.append(e.to_str())
            elif e.id == PatternEvent.Name:
                patterns.append(e.to_str())

        # Separate logging and program output
        if self.__verbose:
            print("")

        self.print_col("Title:           ", self.green(title))
        self.print_col("Artist(s):       ", self.green(artists))
        self.print_col("Genre:           ", self.green(genre))
        self.print_col("Tempo (BPM):     ", self.green(tempo))
        # TODO Incorrect formatting
        # ! self.print_col("Comments:        ", comments)

        url = self.cyan(url) if url else ""
        self.print_col("Project URL:     ", url)
        self.print_col("FL Version:      ", self.green(version))

        ch_len = len(channels)
        if ch_len == 0:
            channels = self.red(0)
        else:
            channels = f"{self.green(ch_len)} [{', '.join(channels)}]"
        self.print_col("Channel(s):      ", channels)

        arr_len = len(arrangements)
        if arr_len == 0:
            arrangements = self.red(0)
        else:
            arrangements = f"{self.green(arr_len)} [{', '.join(arrangements)}]"
        self.print_col("Arrangement(s):  ", arrangements)

        pat_len = len(patterns)
        if pat_len == 0:
            patterns = self.yellow(0)
        else:
            # c_p = [self.blue(p) for p in patterns]
            patterns = f"{self.green(pat_len)} [{', '.join(patterns)}]"
        self.print_col("Pattern(s):      ", patterns)

        if not self.__full_lists:
            print(
                "\nIf you want to see the full lists run with the",
                self.bright("--full-lists"),
                "option",
            )

        if self.__bad_flp:
            flp_inspect = self.cyan("FLPInspect")
            print(
                "\nFLP seems to have been corrupted,"
                f" try inspecting in {flp_inspect}"
            )
