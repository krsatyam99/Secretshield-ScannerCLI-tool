from pathlib import Path
from dataclasses import dataclass
from secretshield.entropy import find_high_entropy_strings
from secretshield.patterns import Pattern


@dataclass
class Finding:
    file_path: str
    line_number: int
    pattern_name: str
    severity: str
    matched_text: str

def scan_file(file_path: Path, patterns: list[Pattern]) -> list[Finding]:
    """Scan a single file line-by-line against all patterns."""
    findings = []

    try:
        lines = file_path.read_text(errors="ignore").splitlines()
    except (UnicodeDecodeError, PermissionError, OSError):
        return findings

    for line_number, line in enumerate(lines, start=1):
        # 1. Regex pattern matching
        for pattern in patterns:
            match = pattern.regex.search(line)
            if match:
                findings.append(
                    Finding(
                        file_path=str(file_path),
                        line_number=line_number,
                        pattern_name=pattern.name,
                        severity=pattern.severity,
                        matched_text=_redact(match.group()),
                    )
                )

        # 2. Entropy check (only if no regex pattern matched this line)
        line_already_flagged = any(f.line_number == line_number for f in findings)
        if not line_already_flagged:
            for token, score in find_high_entropy_strings(line):
                findings.append(
                    Finding(
                        file_path=str(file_path),
                        line_number=line_number,
                        pattern_name=f"High entropy string (score: {score:.2f})",
                        severity="MEDIUM",
                        matched_text=_redact(token),
                    )
                )

    return findings

SKIP_DIRS = {"node_modules", ".git", "venv", ".venv", "env", "__pycache__", ".pytest_cache", "dist", "build"}

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".tar",
    ".gz", ".exe", ".dll", ".so", ".pyc", ".woff", ".woff2", ".ttf",
}


def scan_directory(dir_path: Path, patterns: list[Pattern]) -> tuple[list[Finding], int, int]:
    """Recursively scan a directory. Returns (findings, files_scanned, files_skipped)."""
    findings = []
    files_scanned = 0
    files_skipped = 0

    for file_path in dir_path.rglob("*"):
        if not file_path.is_file():
            continue

        if any(part in SKIP_DIRS for part in file_path.parts):
            files_skipped += 1
            continue

        if file_path.suffix.lower() in BINARY_EXTENSIONS:
            files_skipped += 1
            continue

        files_scanned += 1
        findings.extend(scan_file(file_path, patterns))

    return findings, files_scanned, files_skipped

def _redact(matched: str) -> str:
    """Show only a safe prefix of a matched secret, never the full value."""
    if len(matched) <= 8:
        return "*" * len(matched)
    return matched[:4] + "*" * (len(matched) - 4)