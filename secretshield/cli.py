import os

import typer
from pathlib import Path
from rich.console import Console
from secretshield.patterns import load_patterns
from secretshield.scanner import scan_file
import json
from typing import Optional

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


@app.command()
def history(output: Optional[str] = typer.Option(None, "--output", "-o", help="Save report to a JSON file.")):
    """Perform a deep scan of all previous git commits."""
    from secretshield.scanner import scan_history
    from secretshield.patterns import load_patterns
    
    patterns_path = Path(__file__).parent / "rules" / "default_patterns.yaml"
    patterns = load_patterns(patterns_path)
    
    console.print("[bold blue]Running deep history scan...[/bold blue]")
    findings = scan_history(Path("."), patterns)
    
    if not findings:
        console.print("[green]No secrets found in repository history.[/green]")
        return

    # Handle JSON Export
    if output:
        with open(output, "w") as f:
            json.dump(findings, f, indent=4)
        console.print(f"[bold green]Report successfully saved to: {output}[/bold green]")
    else:
        # Default to Table output if no file is specified
        from rich.table import Table
        table = Table(title="Secrets Found in History")
        table.add_column("Commit", style="cyan")
        table.add_column("File", style="magenta")
        table.add_column("Pattern", style="red")

        for f in findings:
            table.add_row(f['commit'][:7], f['file'], f['pattern_name'])
        
        console.print(table)

@app.command()
def watch(path: str = typer.Argument(".", help="Directory to scan for sensitive files")):
    """Scan workspace for sensitive files that AI assistants might index."""
    console.print(f"[bold yellow]Monitoring workspace at {path} for sensitive exposure...[/bold yellow]")
    
    found_any = False
    for root, dirs, files in os.walk(path):
        # Skip common non-sensitive folders
        if ".git" in dirs: dirs.remove(".git")
        if "venv" in dirs: dirs.remove("venv")
        
        for file in files:
            # Check for exact matches OR specific sensitive extensions
            is_sensitive = (file in ["credentials.json", ".env"]) or \
                           (file.endswith(('.pem', '.key', '.secret')))
            
            if is_sensitive:
                console.print(f"[bold red]ALERT:[/bold red] Sensitive file found: {os.path.join(root, file)}")
                found_any = True
                
    if not found_any:
        console.print("[green]No high-risk sensitive files detected.[/green]")


@app.command()
def guard():
    """Scan all currently staged files for secrets using Python."""
    from secretshield.git_utils import get_staged_files
    from secretshield.scanner import scan_file
    
    staged_files = get_staged_files(Path("."))
    
    if not staged_files:
        console.print("[yellow]No staged files found.[/yellow]")
        return

    patterns_path = Path(__file__).parent / "rules" / "default_patterns.yaml"
    patterns = load_patterns(patterns_path)
    
    found_any = False
    for file_path in staged_files:
        findings = scan_file(file_path, patterns)
        if findings:
            _report(findings)
            found_any = True
            
    if found_any:
        console.print("[bold red]🛑 Secrets detected in staged files. Do not commit![/bold red]")
        raise typer.Exit(code=1)
    
    console.print("[green]✅ All staged files passed security audit.[/green]")

if __name__ == "__main__":
    app()