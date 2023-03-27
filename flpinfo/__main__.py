"""FLPInfo CLI."""

from __future__ import annotations

import enum
import pathlib

import pyflp
import rich
import typer
from pyflp.channel import Automation, Instrument, Layer, Sampler
from pyflp.mixer import Slot
from pyflp.plugin import PluginID, VSTPlugin
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


class ChannelSortOrder(str, enum.Enum):
    Index = "index"
    Type = "type"


@app.command()
def arrangements(filename: pathlib.Path = typer.Argument(..., exists=True)):
    for i, arrangement in enumerate(pyflp.parse(filename).arrangements):
        rich.print(arrangement.name or f"[italic]Arrangement {i + 1}[/italic]")


@app.command()
def channels(
    filename: pathlib.Path = typer.Argument(..., exists=True),
    sort_by: ChannelSortOrder = typer.Option(
        ChannelSortOrder.Index.name, case_sensitive=False
    ),
):
    channels = tuple(pyflp.parse(filename).channels)
    if sort_by == "index":
        table = Table("Type", "Name")
        for channel in channels:
            table.add_row(channel.__class__.__name__, channel.display_name)
        rich.print(table)
    elif sort_by == "type":
        for label, channel_type in {
            "Automations": Automation,
            "Instruments": Instrument,
            "Layers": Layer,
            "Samplers": Sampler,
        }.items():
            table = Table("#", "Name", title=label)
            for i, channel in enumerate(channels):
                if isinstance(channel, channel_type):
                    table.add_row(str(i + 1), channel.display_name)

            if table.rows:
                rich.print(table)


@app.command()
def inserts(filename: pathlib.Path = typer.Argument(..., exists=True)):
    mixer = pyflp.parse(filename).mixer
    table = Table("Name", f"Slots used\n(out of {mixer.max_slots})")
    for i, insert in enumerate(mixer):
        table.add_row(
            insert.name or f"[italic]Insert {i + 1}[/italic]",
            str(len(tuple(insert.events.get(PluginID.Data)))),
        )

    if table.row_count:
        rich.print(table)
    else:
        rich.print(
            ":warning: [red]No inserts found - this is most likely an error.[/red]"
        )


@app.command()
def instruments(
    filename: pathlib.Path = typer.Argument(..., exists=True),
    plugins_only: bool = typer.Option(False),
):
    project = pyflp.parse(filename)
    data: list[str | None | tuple[str, str | None, str | None]] = []
    for i, instrument in enumerate(project.channels.instruments):
        if isinstance(instrument.plugin, VSTPlugin):
            plugin_name = instrument.plugin.name
        else:
            plugin_name = instrument.internal_name

        if plugins_only:
            data.append(plugin_name)
        else:
            data.append((str(i + 1), instrument.display_name, plugin_name))

    if plugins_only:
        for name in data:
            print(name)
    else:
        table = Table("#", "Name", "Plugin")
        for items in data:
            table.add_row(*items)  # type: ignore

        if table.row_count:
            rich.print(table)
        else:
            print("No Instrument channels found")


@app.command()
def samplers(filename: pathlib.Path = typer.Argument(..., exists=True)):
    table = Table("Name", "Path")
    for sampler in pyflp.parse(filename).channels.samplers:
        table.add_row(sampler.display_name, str(sampler.sample_path))

    if table.row_count:
        rich.print(table)
    else:
        print("No Sampler channels found")


@app.command()
def samples(filename: pathlib.Path = typer.Argument(..., exists=True)):
    """File paths of audio samples used throughout the project."""
    paths = frozenset(
        s.sample_path
        for s in pyflp.parse(filename).channels.samplers
        if s.sample_path is not None
    )

    if paths:
        for path in paths:
            print(path)
    else:
        print("No samples have been used")


@app.command()
def patterns(filename: pathlib.Path = typer.Argument(..., exists=True)):
    for pattern in pyflp.parse(filename).patterns:
        rich.print(pattern.name or f"Pattern {pattern.iid}")


@app.command()
def plugins(filename: pathlib.Path = typer.Argument(..., exists=True)):
    project = pyflp.parse(filename)
    native: set[tuple[str, str]] = set()
    vst: set[tuple[str, str, str]] = set()
    native_table = Table("Name", "Type", title="Native")
    vst_table = Table("Name", "Type", "Path", title="VST 2/3")

    container: list[Instrument | Slot] = [i for i in project.channels.instruments]
    container.extend(s for s in [slot for insert in project.mixer for slot in insert])

    for item in container:
        plugin = item.plugin
        plugin_type = "Synth" if isinstance(item, Instrument) else "Effect"
        if isinstance(plugin, VSTPlugin):
            vst.add((plugin.name, plugin_type, plugin.plugin_path))
        elif plugin is not None:
            native.add((item.internal_name or "", plugin_type))

    for n in native:
        native_table.add_row(*n)

    for v in vst:
        vst_table.add_row(*v)

    if native_table.row_count:
        rich.print(native_table)
    else:
        print("No native plugins used")

    if vst_table.row_count:
        rich.print(vst_table)
    else:
        print("No VST plugins used")


@app.command()
def tracks(
    filename: pathlib.Path = typer.Argument(..., exists=True),
    arrangement: int = typer.Argument(0),
):
    for i, track in enumerate(  # type: ignore
        pyflp.parse(filename).arrangements[arrangement].tracks  # type: ignore
    ):
        rich.print(track.name or f"[italic]Track {i + 1}[/italic]")  # type: ignore


if __name__ == "__main__":
    app()
