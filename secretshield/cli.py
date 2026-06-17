import typer
from pathlib import Path
from rich.console import Console

from secretshield.patterns import load_patterns
from secretshield.scanner import scan_file

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()


@app.command()
def scan(path: str = typer.Argument(".", help="File or directory to scan")):
    """Scan a file or directory for hardcoded secrets."""
    target = Path(path)

    if not target.exists():
        console.print(f"[red]Error:[/red] path '{path}' does not exist")
        raise typer.Exit(code=1)

    patterns_path = Path(__file__).parent / "rules" / "default_patterns.yaml"
    patterns = load_patterns(patterns_path)

    if target.is_file():
        console.print(f"Scanning 1 file...\n")
        findings = scan_file(target, patterns)
        _report(findings)
    else:
        from secretshield.scanner import scan_directory
        findings, scanned, skipped = scan_directory(target, patterns)
        console.print(f"Scanning {scanned} files...\n")
        _report(findings)
        clean_count = scanned - len({f.file_path for f in findings})
        console.print(f"\n[green]{clean_count} files clean[/green]")
        if skipped > 0:
            console.print(f"[yellow]{skipped} files skipped (binary or inaccessible)[/yellow]")

@app.command("version")
def version():
    """Show SecretShield version."""
    console.print("SecretShield v0.1.0")

def _report(findings):
    if not findings:
        console.print("[green]Clean — no secrets found.[/green]")
        return

    for f in findings:
        console.print(
            f"[bold red]{f.severity}[/bold red] — {f.pattern_name}\n"
            f"  File: {f.file_path} line {f.line_number}\n"
            f"  Match: {f.matched_text}\n"
        )


if __name__ == "__main__":
    app()