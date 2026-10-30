"""talkaty CLI — Typer + Rich terminal interface."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .config import get_settings
from .pipeline import run
from .script import parse_script
from .voices import list_personas, resolve_persona

app = typer.Typer(
    name="talkaty",
    help="Generate voiceover audio from script.md using open-source TTS.",
)
console = Console()


@app.command()
def generate(
    script: Path = typer.Argument(..., help="Path to script.md"),
    brief: Path | None = typer.Option(None, "--brief", help="Optional brief/description file"),
    voice: str = typer.Option("smooth female", "--voice", "-v", help="Persona name or voice id"),
    accent: str = typer.Option("US", "--accent", "-a", help="Accent hint (US, UK, AU, IN, NG, ZA)"),
    backend: str = typer.Option("edge-tts", "--backend", "-b", help="TTS backend: edge-tts or kittentts"),
    pitch: float = typer.Option(0.0, "--pitch", help="Pitch shift in semitones"),
    speed: float = typer.Option(1.0, "--speed", help="Speed multiplier (0.5–2.0)"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output audio path"),
    subtitles: bool = typer.Option(False, "--subtitles", help="Also emit .srt subtitle file"),
) -> None:
    """Generate voiceover audio from a script.md."""
    opts = {
        "script_path": str(script),
        "brief_path": str(brief) if brief else None,
        "voice": voice,
        "accent": accent,
        "backend": backend,
        "pitch": pitch,
        "speed": speed,
        "output_path": str(output) if output else None,
        "subtitles": subtitles,
    }
    result = asyncio.run(run(__import__("talkaty.pipeline", fromlist=["GenerateOptions"]).GenerateOptions(**opts)))  # noqa: E501
    console.print(f"[green]✓[/green] Voiceover written to {result.path}")
    console.print(f"  voice: {result.voice_used}  backend: {result.backend_used}  duration: {result.duration_seconds:.1f}s")


@app.command()
def voices(
    backend: str = typer.Option("edge-tts", "--backend", "-b", help="Filter by backend"),
) -> None:
    """List available voices/personas."""
    table = Table(title="talkaty voices")
    table.add_column("Persona", style="cyan")
    table.add_column("Voice ID", style="magenta")
    table.add_column("Accent", style="green")
    table.add_column("Gender", style="yellow")
    table.add_column("Description")
    for p in list_personas():
        if backend and p.backend != backend:
            continue
        table.add_row(p.id, p.voice_id(backend), p.accent, p.gender, p.description)
    console.print(table)


@app.command()
def personas() -> None:
    """Alias for `talkaty voices`."""
    voices()


@app.command()
def preview(
    text: str = typer.Argument(..., help="Short text to preview"),
    voice: str = typer.Option("smooth female", "--voice", "-v", help="Persona name"),
    backend: str = typer.Option("edge-tts", "--backend", "-b", help="TTS backend"),
) -> None:
    """Preview a short sample with a voice."""
    from tempfile import NamedTemporaryFile

    from .pipeline import run as _run
    from .pipeline import GenerateOptions

    with NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
        fh.write(text)
        tmp = fh.name

    try:
        result = asyncio.run(
            _run(
                GenerateOptions(
                    script_path=tmp,
                    voice=voice,
                    backend=backend,
                )
            )
        )
        console.print(f"[green]✓[/green] Preview: {result.path}")
        os.unlink(tmp)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@app.command()
def batch(
    scripts_dir: Path = typer.Argument(..., help="Directory of *.md scripts"),
    output_dir: Path = typer.Argument(..., help="Directory for output audio"),
    voice: str = typer.Option("smooth female", "--voice", "-v", help="Persona name"),
    accent: str = typer.Option("US", "--accent", "-a", help="Accent hint"),
    backend: str = typer.Option("edge-tts", "--backend", "-b", help="TTS backend"),
    pitch: float = typer.Option(0.0, "--pitch", help="Pitch shift in semitones"),
    speed: float = typer.Option(1.0, "--speed", help="Speed multiplier"),
    subtitles: bool = typer.Option(False, "--subtitles", help="Also emit .srt files"),
) -> None:
    """Generate voiceovers for all *.md in a directory."""
    scripts_dir = scripts_dir.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    scripts = sorted(scripts_dir.glob("*.md"))
    if not scripts:
        console.print(f"[yellow]No *.md files found in {scripts_dir}[/yellow]")
        return

    from .pipeline import run as _run
    from .pipeline import GenerateOptions

    for script in scripts:
        out = output_dir / (script.stem + ".mp3")
        try:
            result = asyncio.run(
                _run(
                    GenerateOptions(
                        script_path=str(script),
                        voice=voice,
                        accent=accent,
                        backend=backend,
                        pitch=pitch,
                        speed=speed,
                        output_path=str(out),
                        subtitles=subtitles,
                    )
                )
            )
            console.print(f"[green]✓[/green] {script.name} → {result.path}")
        except Exception as exc:  # noqa: BLE001
            console.print(f"[red]✗[/red] {script.name}: {exc}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
