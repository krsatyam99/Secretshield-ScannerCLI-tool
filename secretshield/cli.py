import typer
from pathlib import Path
from rich.console import Console

from secretshield.patterns import load_patterns
from secretshield.scanner import scan_file

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()

@app.command()
def scan(
    path: str = typer.Argument(".", help="File or directory to scan"),
    staged: bool = typer.Option(False, help="Scan only git-staged files")
):
    """Scan a file or directory for hardcoded secrets."""
    target = Path(path)

    # Load patterns
    patterns_path = Path(__file__).parent / "rules" / "default_patterns.yaml"
    patterns = load_patterns(patterns_path)
    
    findings = []

    if staged:
        from secretshield.git_utils import get_staged_files
        staged_files = get_staged_files(Path("."))
        console.print(f"Scanning {len(staged_files)} staged files...\n")
        for file_path in staged_files:
            findings.extend(scan_file(file_path, patterns))
    
    elif target.is_file():
        console.print(f"Scanning 1 file...\n")
        findings = scan_file(target, patterns)
    
    else:
        from secretshield.scanner import scan_directory
        findings, scanned, skipped = scan_directory(target, patterns)
        console.print(f"Scanning {scanned} files...\n")
        if skipped > 0:
            console.print(f"[yellow]{skipped} files skipped (binary or inaccessible)[/yellow]")

    _report(findings)
    
    # Exit with code 1 if findings found (useful for CI/CD and git hooks)
    if findings:
        raise typer.Exit(code=1)

@app.command("version")
def version():
    """Show SecretShield version."""
    console.print("SecretShield v0.1.0")

@app.command("install-hook")
def install_hook():
    """Install SecretShield as a git pre-commit hook."""
    from secretshield.git_utils import install_pre_commit_hook
    install_pre_commit_hook(Path("."))

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